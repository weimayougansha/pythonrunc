import os.path
import pdb

from parameter import DOCKER_PS_FILE, docker_ps_mes
from datetime import datetime  # 导入 datetime 函数
from utils.logging_module import logger
import json
import signal


class DockerPsClass:

    def __init__(self, container_id, image, cmd, pid):
        self.container_id = container_id
        self.image = image
        self.cmd = cmd
        self.created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.pid = pid
        self.docker_ps_mes = docker_ps_mes
        self.DOCKER_PS_FILE = DOCKER_PS_FILE
        if not os.path.isfile(self.DOCKER_PS_FILE):
            os.system("touch %s" % self.DOCKER_PS_FILE)

    def add_mes_to_docker_ps(self):
        # pdb.set_trace()
        self.docker_ps_mes["CONTAINER_ID"] = self.container_id
        self.docker_ps_mes["IMAGE"] = self.image
        self.docker_ps_mes["COMMAND"] = self.cmd
        self.docker_ps_mes["CREATED"] = self.created  # date
        self.docker_ps_mes["STATUS"] = 'Running'    # Running Stop
        self.docker_ps_mes["PID"] = self.pid
        with open(self.DOCKER_PS_FILE, 'r+') as f:
            try:
                docker_ps_list = json.load(f)
            except Exception as e:
                print(str(e))
                docker_ps_list = []
            docker_ps_list.append(self.docker_ps_mes)
        with open(self.DOCKER_PS_FILE, 'w') as f:
            json.dump(docker_ps_list, f)
        logger.info(self.container_id + " add to docker ps json")

    @staticmethod
    def get_docker_ps():
        print("{: <20}{: <20}{: <20}{: <20}{: <20}{: <20}".format(*docker_ps_mes.keys()))
        if not os.path.isfile(DOCKER_PS_FILE):
            logger.info("have no DOCKER_PS_FILE")
            return None
        with open(DOCKER_PS_FILE, 'r') as f:
            try:
                docker_ps_list = json.load(f)
            except:
                logger.info("have no docker ps")
                return None
            for row in docker_ps_list:
                print("{: <20}{: <20}{: <20}{: <20}{: <20}{: <20}".format(*row.values()))
        return docker_ps_list

    def delete_docker_ps(self):
        with open(self.DOCKER_PS_FILE, 'r+') as f:
            try:
                docker_ps_list = json.load(f)
            except:
                return None
            for docker_ps in docker_ps_list:
                if docker_ps["CONTAINER_ID"] == self.container_id:
                    docker_ps_list.remove(docker_ps)
        if len(docker_ps_list) == 0:
            os.remove(DOCKER_PS_FILE)
            return None
        with open(self.DOCKER_PS_FILE, 'w') as fw:
            json.dump(docker_ps_list, fw)
        logger.info(self.container_id + " delete from docker ps json")


def get_current_ps():
    DockerPsClass.get_docker_ps()

def delete_docker_ps(container_id):
    docker_ps_list = DockerPsClass.get_docker_ps()
    if docker_ps_list is None:
        print("have no this docker ps")
    for docker_ps in docker_ps_list:
        if docker_ps["CONTAINER_ID"] == container_id:
            container_pid = docker_ps["PID"]
            try:
                os.kill(container_pid, signal.SIGKILL)
            except Exception as e:
                logger.info("the error for kill %s : is %s " % (container_id, str(e)))
            docker_ps_list.remove(docker_ps)
    with open(DOCKER_PS_FILE, 'w') as fw:
        json.dump(docker_ps_list, fw)


