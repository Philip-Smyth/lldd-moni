#!/bin/sh
sudo lldpad -d
sleep 30
sudo lldptool set-lldp -i enp0s3 adminStatus=rxtx

#lldp_tlv={'sysname', 'portDesc', 'sysDesc', 'sysCap'}
#for i in $lldp_tlv
#    do echo "Enabling lldp for enp0s3";
#    lldptool -T -i enp0s3 -V $i enableTx=yes;
#done
sudo lldptool -T -i enp0s3 -V sysname enableTx=yes
sudo lldptool -T -i enp0s3 -V portDesc enableTx=yes
sudo lldptool -T -i enp0s3 -V sysDesc enableTx=yes
sudo lldptool -T -i enp0s3 -V sysCap enableTx=yes
