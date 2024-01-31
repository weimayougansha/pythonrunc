import os
import json
from utils.logging_module import logger
from parameter import NS_TYPE_LIST, DOCKER_PS_FILE


# 定义一个函数，用于修改某个进程的 namespace
def change_namespace(pid, ns_type, ns_type_value):
    # 参数 pid 是进程的 ID，ns_type 是要修改的 namespace 的类型，如 "net", "pid", "user" 等
    # 打开进程的 namespace 文件
    ns_file = "/proc/%s/ns/%s" % (pid, ns_type)
    print(ns_file)
    # 使用 os.open() 函数以只读模式打开文件，并返回文件描述符
    fd = os.open(ns_file, os.O_RDONLY)
    # 使用 os.setns() 函数将当前进程加入到指定的 namespace
    os.setns(fd, ns_type_value)
    # 关闭文件描述符
    os.close(fd)
    # 打印成功信息
    print(f"Successfully changed {ns_type} namespace of process {pid}")

# 示例：修改进程 1234 的网络 namespace
# current_pid = os.getpid()


def exec_command(container_id, cmd_str):
    with open(DOCKER_PS_FILE, 'r') as f:
        try:
            docker_ps_list = json.load(f)
        except:
            logger.info("have no docker ps")
            return None
    pid = -1
    for docker_ps in docker_ps_list:
        if docker_ps["CONTAINER_ID"] == container_id:
            pid = docker_ps["PID"]
            break
    if pid == -1:
        logger.info("have no container: %s" % container_id)
        return None
    ns_type_list = NS_TYPE_LIST
    for ns_type, ns_type_value in ns_type_list:
        change_namespace(pid, ns_type, ns_type_value)
    os.system(cmd_str)