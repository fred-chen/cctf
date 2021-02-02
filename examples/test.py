#coding=utf-8

'''
内容：演示在11台目标主机上同时执行55条命令

Created on Mar 17, 2019
@author: fred
'''

from cctf import caseunit
from widgets import *
from cctf import gettarget
from orcabd import bdoperator
import time, sys

# t = gettarget('10.211.55.6', 'root', 'root')
# w = widget(t, 'widwriter', '-d /tmp -n 5 -r 5 -k 10240')
# print "w started"
# # time.sleep(15)
# # print "stopping w"
# # w.stop()
# print "stopped"
# print w.exitcode()
# print w.stdout()
# print w.stderr()
# time.sleep(5)


# class a(caseunit):
#     counter = 0
#     def body(self):
#         self.counter += 1
#         print self.counter
#         return caseunit.SUCC
#             
# 
# b=a()
# b.start(113086)
# time.sleep(1)
# b.pause()
# time.sleep(2)
# b.resume()
# # time.sleep(1)
# # b.stop()
# print b.getresult()
# 
# time.sleep(6)
# 
# exit()

# exit()

from cctf import gettarget
from widgets.widcpuloadgen import widcpuloadgen

""" 定义多个目标设备的信息 """
nodes = [
    ('192.168.103.253', 'root', 'password', 'ssh'),
    # ('10.211.55.6', 'root', 'root', 'ssh'),
    # ('10.211.55.7', 'root', 'root', 'ssh'),
#     ('192.168.100.166', 'root', 'admin', 'ssh'),
#     ('192.168.100.102', 'ssh', 'root', 'cobbler'),
#     ('192.168.100.103', 'ssh', 'root', 'cobbler'),
#     ('192.168.100.104', 'ssh', 'root', 'cobbler'),
#     ('192.168.100.106', 'ssh', 'root', '1'),
#     ('192.168.100.107', 'ssh', 'root', '1'),
#     ('192.168.100.108', 'ssh', 'root', '1'),
#     ('192.168.100.170', 'ssh', 'root', 'admin'),
#     ('192.168.100.174', 'ssh', 'root', 'admin'),
#     ('192.168.100.170', 'ssh', 'root', 'admin'),
#     ('192.168.100.172', 'ssh', 'root', 'xxxx'),
#     ('192.168.100.171', 'ssh', 'root', 'xxxx'),
    ]

ts = []
for node in nodes:
    """ 为每个目标设备创建一个target对象 """
    ts.append(gettarget(node[0],node[1],node[2],node[3], 3))

# wids = []
# for t in ts:
#     wid = widcpuloadgen(t)
#     wids.append(wid)
#     wid = widmemloadgen(t)
#     wids.append(wid)

# time.sleep(30)

# print "stopping..."
# for wid in wids:
#     wid.stop()

# print "stopped..."
# time.sleep(5)
# print "exit."


# for t in ts:
#     bdop = t.newshell()
#     bdop.createpool('abc')
#     print "pools: %s" % bdop.getpools()
#     t.shutdown()
     
# exit()


shs = []
for t in ts:
    """ 为每个target对象创建5个shell对象（共55个连接） """
    for i in range(1): 
        shs.append(t.newshell())

cos = []
for sh in shs:
    """
        在每个连接上执行一个“hostname”命令（共55条命令）
        wait=False 表示不等待执行结果，并发执行
    """
    for i in range(10):
        cos.append(sh.exe("hostname", wait=False)) 
        cos.append(sh.exe("date", wait=False)) 

print "waiting for results"
for co in cos:
    """ 逐个命令检查执行结果 """
    co.wait()

# for i in range(3):
#     for t in ts:
#         t.reboot()

# for i in range(3):
#     for t in ts:
#         t.reboot(wait=False)
#     for t in ts:
#         t.wait_alive()



# for t in ts:
#     t.panicreboot(wait=False)
# time.sleep(0.5)
# 
# i = 0
# while ts[:]:
#     for t in ts[:]:
#         if t.wait_alive(1):
#             print "%s rebooted." % (t)
#             ts.remove(t)
#         else:
#             print "waiting for %s..." % (t)