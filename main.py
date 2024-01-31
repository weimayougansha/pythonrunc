from utils.logging_module import logger
import argparse
from main_command import run
from ps import get_current_ps, delete_docker_ps
from exec import exec_command


def main():
    # 定义一个对象
    parser = argparse.ArgumentParser(description="mydocker")
    # 定义 sub 子对象
    sub_parser = parser.add_subparsers(dest="command")
    parser_run = sub_parser.add_parser("run")
    parser_run.add_argument("--ti", action="store_true", dest="tty", default=False, help="interactive execution")
    parser_run.add_argument("--cmd", dest="cmd", help="command")
    parser_run.add_argument("--m", dest="mem", help="memory, the unit is byte")
    parser_run.add_argument("--cpu", dest="cpu", help="cpushare, eg: 1024 2048")
    parser_run.add_argument("--v", dest="volume", help="local dir as persistent volume")
    parser_run.add_argument("--img", dest="img", help="img name,endswith .tar eg: xxx.tar")

    # ps
    ps_sub_parser = sub_parser.add_parser("ps")

    # delete
    delete_sub_parser = sub_parser.add_parser("delete")
    delete_sub_parser.add_argument("--id", dest="container_id", help="delete docker ps with container_id")


    # exec
    exec_sub_parser = sub_parser.add_parser("exec")
    exec_sub_parser.add_argument("--id", dest="container_id", help="exec docker command in container_id")
    exec_sub_parser.add_argument("--cmd", dest="cmd", help="command")

    cgroup_dict = {}

    args = parser.parse_args()
    if args.command == "run":
        cgroup_dict["memory"] = args.mem
        cgroup_dict["cpu"] = args.cpu
        # 下面判断各个变量格式是否正常 比如 value = xxx:xxx格式,先不考虑给容器挂nas
        logger.info("begin run %s %s " % (args.tty, args.cmd))
        run(args.command, args.tty, args.cmd, cgroup_dict, args.volume, args.img)
    elif args.command == "ps":
        get_current_ps()
    elif args.command == "delete":
        container_id = args.container_id
        delete_docker_ps(container_id)
    elif args.command == "exec":
        container_id = args.container_id
        cmd = args.cmd
        exec_command(container_id, cmd)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
