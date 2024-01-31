import os
from utils.logging_module import logger
from parameter import IP_file, IPAM, add_ip_to_container_file_path
import re
import pdb

class NetworkControllerClass:
    def __init__(self, driver_name):
        self.driver_name = driver_name
        self.IP_file = IP_file
        if not os.path.isfile(self.IP_file):
            os.system("echo 1 > %s" % self.IP_file)
        self.IPAM = IPAM
        self.add_ip_to_container_file_path = add_ip_to_container_file_path
        self.counter = self.__get_ip_from_IPAM()  # ip最后一位

    def create_veth(self, container_id, pid):
        ip_counter = self.counter + 2
        ip_str = self.__get_ip(ip_counter)
        system_cmd = f"sh {self.add_ip_to_container_file_path} {container_id} {pid} {ip_str} {self.IPAM}"
        if os.system(system_cmd) == 0:
            self.__return_ip_to_IPAM("ip_get", self.counter)
            logger.info("create network success for %s" % container_id)
            return None
        else:
            self.delete_veth(container_id)
            logger.error("create network failed for %s" % container_id)
            return None

    def __get_ip(self, counter):
        pattern = r"(?<=\.)[0-9]+(?=/24)"
        ip_str = re.sub(pattern, str(counter), self.IPAM)
        return ip_str

    def delete_veth(self, container_id):
        '''
        system_cmd = f"/bin/sh {self.delete_ip_from_container_file_path} {container_id}"
        logger.info(system_cmd)
        sys_res = os.system(system_cmd)
        logger.info(str(sys_res))
        logger.info("__return_ip_to_IPAM")
        self.__return_ip_to_IPAM("ip_return", self.counter)
        '''
        try:
            veth_name_host = "veth-" + container_id[-4:] + "-h"
            netns_container = "netns-" + container_id[-4:]
            # ip_list_res = os.popen("ip a")
            # logger.info("ip_list_res %s" % ip_list_res)
            # del_veth_res = os.popen("ip link delete %s" % veth_name_host)
            # logger.info("ip link delete veth %s result: %d" % (veth_name_host, del_veth_res))
            #del_veth_netns_res = os.popen("rm -f /var/run/netns/%s" % netns_container)
            #logger.info("ip link delete netns %s result: %d" % (netns_container, del_veth_netns_res))
            os.remove("/var/run/netns/%s" % netns_container)
            self.__return_ip_to_IPAM("ip_return", self.counter)
        except Exception as e:
            logger.error(str(e))


    def __get_ip_from_IPAM(self):
        with open(self.IP_file) as f:
            f_content = f.read()
        f_content = int(f_content)
        # 定义一个掩码变量
        mask = 1
        # 定义一个计数器变量
        counter = 0
        # 使用一个循环来遍历二进制变量的每一位
        while True:
            # 将二进制变量和掩码变量进行按位与运算
            result = f_content & mask
            # 如果结果为 0，说明当前位是 0，我们就找到了第一个 0 的位置，可以跳出循环
            if result == 0:
                break
            # 如果结果不为 0，说明当前位是 1，我们就需要继续检查下一位
            # 将掩码变量左移一位，也就是乘以 2，得到一个新的掩码变量
            mask = mask << 1
            # 将计数器变量加一，表示我们已经检查了一位
            counter = counter + 1
        # 打印第一个 0 的位置，从右往左数，也就是第 2 位
        print(f"The first 0 in {bin(f_content)} is at position {counter} from right.")

        # 使用按位或运算，将二进制变量的这一位置 1，得到一个新的二进制变量
        y = f_content | mask
        # 打印新的二进制变量的值
        print(f"The new binary variable is {bin(y)}.")
        return counter

    def __return_ip_to_IPAM(self, ip_type, ip_counter):
        with open(self.IP_file, 'r') as f:
            f_content = f.read()
        f_content = int(f_content)
        if ip_type == 'ip_get':
            mask = 1 << ip_counter
            f_content = f_content | mask
        elif ip_type == 'ip_return':
            mask = 0xffffffff ^ (1 << ip_counter)
            f_content = f_content & mask
        with open(self.IP_file, 'w') as f_w:
            f_w.write(str(f_content))



