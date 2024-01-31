# 导入 time 和 uuid 模块
import time
import uuid
import random
#import pdb

# 定义一个函数，用于生成一个基于时间戳的唯一 id
def generate_id():
    #pdb.set_trace()
    # 获取当前时间的时间戳，单位是秒
    timestamp = time.time()
    # 将时间戳转换为 16 进制的字符串
    hex_timestamp = hex(int(timestamp))[2:]
    # 使用 uuid 模块的 uuid4() 函数生成一个随机的 uuid
    # random_uuid = uuid.uuid4()
    # hex_uuid = random_uuid.split("-")[1]
    # 将 uuid 转换为 16 进制的字符串，并去掉中间的横线
    #hex_uuid = random_uuid.hex
    # 将时间戳和 uuid 拼接起来，作为唯一 id
    hex_uuid = random.randint(1000, 9999)
    unique_id = hex_timestamp + str(hex_uuid)
    # 返回唯一 id
    return unique_id


