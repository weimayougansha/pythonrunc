#!/bin/sh
##############################################
#
# args: contain_id
#
##############################################


echo "delete ip1" >> /root/git/delete_ip.log

if [ $# -lt 1 ];then
  echo "args num are least 1"
  exit 1
fi
echo "delete ip2" >> /root/git/delete_ip.log
contain_id=$1

echo "delete ip3" >> /root/git/delete_ip.log
#  veth
veth_name_host="veth-${contain_id: -4}-h"
veth_name_container="veth-${contain_id: -4}-cnt"

echo "ip link delete $veth_name_host" >> /root/git/delete_ip.log
ip link delete $veth_name_host || echo "failed" >> /root/git/delete_ip.log

netns_container="netns-${contain_id: -4}"
echo $netns_container >> /root/git/delete_ip.log
rm -f /var/run/netns/$netns_container || echo "failed" >> /root/git/delete_ip.log

