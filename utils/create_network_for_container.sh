#! /bin/bash

##############################################
#
# args: contain_id, pid, ip/networkmask, port
#
##############################################

if [ $# -lt 4 ];then
  echo "args num are least 4"
  exit 1
fi

contain_id=$1
pid=$2
ip_mask=$3
IPAM=$4

# create veth
veth_name_host="veth-${contain_id: -4}-h"
veth_name_container="veth-${contain_id: -4}-cnt"
ip link add $veth_name_host type veth peer name $veth_name_container

# add veth_name_container to container
netns_container="netns-${contain_id: -4}"
if [ ! -d /var/run/netns ]; then
  mkdir -p /var/run/netns
fi
ln -s /proc/$pid/ns/net /var/run/netns/$netns_container
ip link set $veth_name_container netns $netns_container

# add ip/mask to container
ip netns exec $netns_container ifconfig $veth_name_container $ip_mask up
ip netns exec $netns_container route add default $veth_name_container
ip link set $veth_name_host up

# add bridge
# echo "add bridge"
ip link show type bridge | grep -q br0
if [ $? -eq 1 ];then
  ip link add name br0 type bridge
  ip link set br0 up
  # add host route
  route add -net $IPAM dev br0
  # ip link set eth0 master br0
fi

ip link set $veth_name_host master br0

echo "create ip success" >> delete_ip.log


