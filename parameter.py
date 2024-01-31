import os

DOCKER_PS_FILE = './docker_ps_file.json'
docker_ps_mes = {
    "CONTAINER_ID": '',
    "IMAGE": '',
    "COMMAND": '',
    "CREATED": '',  # date
    "STATUS": '',    # Running Stop
    "PID": -1
}

NS_TYPE_LIST = [
        ('ipc', os.CLONE_NEWIPC),
        ('uts', os.CLONE_NEWUTS),
        ('net', os.CLONE_NEWNET),
        ('pid', os.CLONE_NEWPID),
        ('mnt', os.CLONE_NEWNS)
        ]

IP_file = "./ipbitmap.txt"

IPAM = "192.168.0.0/24"

# add_ip_to_container_file_path code by shell
add_ip_to_container_file_path = "./utils/create_network_for_container.sh"

# docker image dir path
docker_image_dir = './'