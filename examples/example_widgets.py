#coding=utf-8

'''
内容：演示如何通过 widget api 在多台目标设备上启动和停止 widget

Created on Mar 17, 2019
@author: fred
'''

from cctf import gettarget
from widgets import widcpuloadgen, widmemloadgen
import time

""" 
    定义多个目标设备的信息. 格式：(IP Address, Username, Password, Connection_type) 
"""
nodes = (
            ('10.211.55.6', 'root', 'root', 'ssh'),
            ('10.211.55.7', 'root', 'root', 'ssh'),
            ('10.211.55.9', 'root', 'root', 'ssh'),
        )

""" 
    为每个目标设备创建一个target对象并放入 ts 列表中 
"""
ts = []
for node in nodes:
    t = gettarget(node[0],node[1],node[2],node[3], 3)
    ts.append(t)

""" 
    在每个目标设备（target）上启动一个 CPU widget，一个 MEMORY widget 
"""
wids = []
for t in ts:
    wid = widcpuloadgen(t)
    wids.append(wid)
    wid = widmemloadgen(t)
    wids.append(wid)

""" 
    等待 30 秒后，停止所有 widget 
"""
time.sleep(30)
for wid in wids:
    print "Stopping %s" % (wid)
    wid.stop()
print "All widgets are stopped."

time.sleep(5)
print "exit."
