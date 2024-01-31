
# a lightweight container runtime coding by Python
# 开发版本: Python 3.12.1

# 实现命令
python main.py [-h] {run,ps,delete,exec} ...

# run
usage: main.py run [-h] [--ti] [--cmd CMD] [--m MEM] [--cpu CPU] [--v VOLUME] [--img IMG]
options:
  -h, --help  show this help message and exit
  --ti        interactive execution
  --cmd CMD   command
  --m MEM     memory, the unit is byte
  --cpu CPU   cpushare, eg: 1024 2048    
eg:
  python main.py run --cmd "/bin/top -b" --cpu 2048 --m 2000000000 --img busybox.tar

# exec
usage: main.py exec [-h] [--id CONTAINER_ID] [--cmd CMD]

options:
  -h, --help         show this help message and exit
  --id CONTAINER_ID  exec docker command in container_id
  --cmd CMD          command  
eg:
  python main.py exec --id 65b9ceb06589 --cmd /bin/sh

# delete
usage: main.py delete [-h] [--id CONTAINER_ID]

options:
  -h, --help         show this help message and exit
  --id CONTAINER_ID  delete docker ps with container_id  
eg:
  python main.py delete --id 65b9a6c31495

# ps
python main.py ps



# 未完成
1) 镜像仓库管理  
2) dockerfile解析




