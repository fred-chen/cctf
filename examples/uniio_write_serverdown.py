#coding=utf-8

'''
内容：演示在11台目标主机上同时执行55条命令

Created on Mar 17, 2019
@author: fred
'''
import time
from cctf import gettarget
import random
from cctf import Command


ts = []

ts.append(gettarget('192.168.101.1', 'root', '123456'))
ts.append(gettarget('192.168.101.2', 'root', '123456'))
ts.append(gettarget('192.168.101.3', 'root', '123456'))
ts.append(gettarget('192.168.101.4', 'root', '123456'))
ts.append(gettarget('192.168.101.5', 'root', '123456'))
ts.append(gettarget('192.168.101.6', 'root', '123456'))

shs = []
for t in ts:
    for i in range(1):
        sh = t.newshell()
        shs.append(sh)
cos = []
for sh in shs:
    co = sh.exe('ls /', wait=False)
    cos.append(co)
     
print "+" * 80
 
for co in cos:
    print co.getlist()


     
print "*" * 80
 
 
# print co.stdout + " " + co.exit