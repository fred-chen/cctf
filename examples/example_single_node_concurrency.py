#coding=utf-8

'''
内容：演示如何在一个目标设备上创建多个连接，生成多个“shell”对象，
     通过多个“shell”对象让目标设备并发地执行多条命令。

Created on Mar 17, 2019
@author: fred
'''

from cctf import gettarget

""" 
    为目标设备创建一个target对象，通过target对象创建5个'shell'对象，并放入 shs 列表中 
"""
t = gettarget('10.211.55.6', 'root', 'root', 'ssh', 3)
shs = []
for i in range(5):
    sh = t.newshell()
    shs.append(sh)

""" 
    通过每个 'shell' 对象的 exe() 函数，非阻塞地发送一条命令给目标设备，并将返回的command对象保存在'cos'列表中。
    由于5个'shell'对象会同时给目标设备发送命令，意味着同时会有5条命令并发地在目标设备执行。
    exe() 函数中的 'wait=True/False' 控制 exe() 的行为：
        wait = True, 函数会等待命令在目标设备上执行完成才返回；
        wait = False，函数会立即返回。
        exe() 的返回值，是一个 'command' 对象，用户脚本可以通过 command 对象检查命令在目标设备上的执行结果。
"""
cos = []
for sh in shs:
    co = sh.exe("find / -name 'abc'", wait=False)
    cos.append(co)

""" 
    等待每条命令执行完成, 并打印每条命令的输出，返回值
"""
for co in cos:
    co.wait()
    print co.stdout
    print co.exit

print "All commands are done."
