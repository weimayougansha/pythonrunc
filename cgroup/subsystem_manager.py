import os.path
from utils.logging_module import logger

class SubsystemManager:

    cgroup_path = "/sys/fs/cgroup"

    cgroup_file_dict = {
        "memory": "memory.limit_in_bytes",
        "cpu": "cpu.shares"
    }

    def __init__(self, subsystem_name, subsystem_value, this_cgroup_name, pid, container_id):
        self.subsystem_name = subsystem_name
        self.this_cgroup_name = this_cgroup_name
        self.subsystem_value = subsystem_value
        self.subsystem_path = os.path.join(self.cgroup_path, self.subsystem_name, self.this_cgroup_name, str(container_id))
        self.pid = pid
        self.container_id = container_id

    def name(self):
        return self.name

    def set(self):
        if not os.path.isdir(self.subsystem_path):
            os.makedirs(self.subsystem_path)
        cgroup_file = os.path.join(self.subsystem_path, self.cgroup_file_dict.get(self.subsystem_name))
        with open(cgroup_file, 'w') as f:
            f.write(self.subsystem_value)
        logger.info("create cgroup file for %s" % self.subsystem_name)
        return True

    def apply(self):
        """
        将pid追加到 sybsystem新建的子目录task文件中
        :return:
        """
        this_subsystem_task_path = os.path.join(self.subsystem_path, "tasks")
        with open(this_subsystem_task_path, "a+") as f:
            # pid = os.getpid()
            f.write(str(self.pid))

        return True

    def remove(self):
        """
        删除子目录，即删除cgroup
        :return:
        """
        if not os.path.isdir(self.subsystem_path):
            return False
        os.rmdir(self.subsystem_path)
        return True

    def get_subsystem_path(self):
        subsystem_path = os.path.join(self.cgroup_path,self.subsystem_name,self.this_cgroup_name)
        return subsystem_path