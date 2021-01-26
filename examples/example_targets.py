#coding=utf-8

'''
内容：演示如何创建一个target对象并演示target对象的一些基本函数

Created on Mar 17, 2019
@author: fred
'''

from cctf import gettarget


""" 
    通过gettarget工厂函数，获取远端设备相应的target对象 
    用户脚本可以同时创建许多个target对象，代表多个目标设备 
"""
t1 = gettarget('10.211.55.6', 'root', 'root', 'ssh', 36)
t2 = gettarget('10.211.55.7', 'root', 'root', 'ssh', 36)
t3 = gettarget('10.211.55.9', 'root', 'root', 'ssh', 36)


""" target对象可能有很多种，查看target对象的类型 """
print t1.__class__


""" 
    CCTF会自动检测目标设备类型，并返回不同的target对象
    例如安装了BD产品的目标设备，gettarget()会返回一个'bdtarget'对象 
"""
bdt = gettarget('192.168.103.85', 'root', 'password', 'ssh', 30)
print bdt.__class__


""" 
    target对象的reboot()方法，可以对目标设备进行重启 
"""
raw_input("\nPress ENTER to reboot targets...")
t1.reboot()
t2.reboot()
t3.reboot()
 
""" 
    reboot()方法中的“wait”参数，可以控制reboot()函数是否等待目标设备重新启动完成
    wait=True，默认值，reboot()函数会等待目标设备重启完成才返回；
    wait=False，reboot()函数立即返回，不阻塞用户脚本的执行，后续可以通过target.alive()检测目标设备是否重启完成 
"""
raw_input("\nPress ENTER to reboot targets CONCURRENTLY...")
t1.reboot(wait=False)
t2.reboot(wait=False)
t3.reboot(wait=False)
 
print "rebooting t1, t2, t3..."
for t in (t1,t2,t3):
    t.wait_down()
for t in (t1,t2,t3):
    t.wait_alive()
 
""" 
    target对象的 panicreboot() 方法，可以模拟目标系统崩溃的情况
    panicreboot() 同样支持'wait'参数
"""
raw_input("\nPress ENTER to panicreboot targets...")
t1.panicreboot(wait=False)
t2.panicreboot(wait=False)
t3.panicreboot(wait=False)
 
for t in (t1,t2,t3):
    t.wait_down()
for t in (t1,t2,t3):
    t.wait_alive()

""" 
    所有的target对象都从同一个父类继承而来，因此它们具有一些通用的方法例如reboot(), panicreboot()等。
    但不同的target对象可能支持不同的方法。
    例如'bdtarget'对象，代表一个安装了BD产品的目标设备，通过'bdtarget'对象可以获取一些BD集群的基本信息，例如pool信息。
"""
raw_input("\nPress ENTER to report pools on a bdtarget...")
print "pools on %s: \n%s" % (bdt, bdt.getpools())