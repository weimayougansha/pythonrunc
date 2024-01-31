import subprocess
import os
from utils.logging_module import logger
from fs.init_fs import init_fs, get_overlayfs_from_file, rm_fs, add_persistent_volume
from cgroup.subsystem_manager import SubsystemManager
from ps import DockerPsClass
from utils.generate_id import generate_id
import signal
from network.network_controller import NetworkControllerClass
from parameter import docker_image_dir
import pdb


def unshare_cmd(cmd_list):
    org_cmd = ["sudo", "unshare", "-uipm -f --mount-proc"]
    org_cmd.extend(cmd_list)
    return org_cmd


def join_new_namespace(pid):
    namespace = [
        ('ipc', os.CLONE_NEWIPC),
        ('uts', os.CLONE_NEWUTS),
        ('net', os.CLONE_NEWNET),
        ('pid', os.CLONE_NEWPID),
        ('mnt', os.CLONE_NEWNS)
    ]
    for ns_type, ns_flag in namespace:
        fd = os.open('/proc/{0}/ns/{1}'.format(pid, ns_type), os.O_RDONLY)
        ret = os.setns(fd, ns_flag)
        os.close(fd)
        if ret == -1:
            print
            'libc.setns failed'
            exit(1)


def run(cgroup_name, tty, cmd, cgroup_dict, volume, img):

    python_pid = os.fork()
    if python_pid > 0:
        try:
            if tty:
                os.waitid(os.P_PID, python_pid, os.WEXITED)
            os._exit(0)
        except:
            os._exit(0)
        # return None
    #become_daemon(tty)
    '''
    try:
        os.setsid()
    except OSError as e:
        print(e)
    '''
    #unshare_cmd_str = unshare_cmd(cmd)
    #subprocess.run(unshare_cmd_str)

    # os.unshare(os.CLONE_NEWPID)只会在子系统中才会加入新的pid namespace 所以这里单独创建
    # 在4.18的内核中有个新的namespace /proc/pid/ns/pid_for_children
    # /proc/pid/ns/pid_for_children 表示该进程创建的子进程所属的PID命名空间，它可能和该进程自身的PID命名空间不同，
    # 如果该进程使用了os.unshare()函数或者clone()系统调用来创建新的PID命名空间。

    tar_path = os.path.join(docker_image_dir, img)  # image file 后期再完善
    if not os.path.isfile(tar_path):
        logger.error("docker image %s is not exists" % tar_path)
    os.unshare(os.CLONE_NEWPID)
    container_id = generate_id()
    pid = os.fork()
    if pid == 0:
        # logger.info("begin create childen pid")
        try:
            if not tty:
                become_daemon(tty)
            cmd_path = cmd.split()[0]
            cmd_args_list = cmd.split()
            """
            os.CLONE_NEWNS：挂载命名空间
            os.CLONE_NEWUTS：UTS命名空间
            os.CLONE_NEWIPC：IPC命名空间
            os.CLONE_NEWUSER：用户命名空间
            os.CLONE_NEWPID：PID命名空间
            os.CLONE_NEWNET：网络命名空间
            """
            #logger.info("begin create namespace for childen pid")
            os.unshare(
                os.CLONE_NEWNS |
                os.CLONE_NEWUTS |
                os.CLONE_NEWIPC |
                # os.CLONE_NEWPID |
                os.CLONE_NEWNET
            )
            os.system("mount --make-rprivate /")
            logger.info("begin init fs")
            # pdb.set_trace()
            init_fs_path = get_overlayfs_from_file(tar_path, container_id)
            #logger.info(init_fs_path)
            init_fs(init_fs_path, volume)

            logger.info("begin execv childen command")
            os.execv(cmd_path, cmd_args_list)
            os._exit(0)
            # return os.getpid()
        except KeyboardInterrupt:
            os._exit(0)
    else:
        # join_new_namespace(pid) 这个func废弃了
        # container_id
        # container_id = generate_id()
        logger.info("pid %d begin join_new_cgroup named %s " % (pid, container_id))
        subsystemManager_list = create_cgroup(cgroup_dict, cgroup_name, pid, container_id)
        docker_ps = DockerPsClass(container_id, tar_path, cmd, pid)
        docker_ps.add_mes_to_docker_ps()
        network_controller = NetworkControllerClass("bridge")
        network_controller.create_veth(container_id, pid)

        try:
            os.waitid(os.P_PID, pid, os.WEXITED)
        except:
            os.kill(pid, signal.SIGTERM)
            os.waitid(os.P_PID, pid, os.WEXITED)

        # 异常关闭的情况后续处理

        #logger.info(os.environ)

        remove_cgroup(subsystemManager_list)
        rm_fs(tar_path, container_id)
        docker_ps.delete_docker_ps()
        logger.info("begin delete veth")
        network_controller.delete_veth(container_id)

        return pid


def create_cgroup(cgroup_dict, cgroup_name, pid, container_id):
    subsystemManager_list = []
    for subsystem_name, subsystem_value in cgroup_dict.items():
        subsystemManager = SubsystemManager(subsystem_name, subsystem_value, cgroup_name, pid, container_id)
        subsystemManager.set()
        subsystemManager.apply()
        subsystemManager_list.append(subsystemManager)
    return subsystemManager_list


def remove_cgroup(subsystemManager_list):

    for subsystemManager in subsystemManager_list:
        subsystemManager.remove()


def become_daemon(tty):
    if tty:
        return None
    logger.info("tty = %s " % tty)
    try:
        os.setsid()
    except OSError as e:
        print(e)

    # 重定向标准输入/输出和标准错误到 /dev/null
    devnull = open(os.devnull, 'w')
    os.dup2(devnull.fileno(), 0)
    os.dup2(devnull.fileno(), 1)
    os.dup2(devnull.fileno(), 2)
    # 关闭不需要的文件描述符
    devnull.close()
    logger.info("now become a daemon")
    return True








