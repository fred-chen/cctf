#coding=utf-8

'''
内容：演示如何通过一个target对象的newshell()方法获取目标设备的“shell”对象，
     并通过“shell”对象的exe()方法在远端设备上执行一条命令

Created on Mar 17, 2019
@author: fred
'''

from cctf import gettarget

""" 
    通过gettarget工厂函数，获取远端设备相应的target对象 
"""
t = gettarget('192.168.100.154', 'root', 'password', 'ssh', 10)
sh = t.newshell()
sh.exe("echo hello cctf!'")  # a buggy command will cause shell blocked
