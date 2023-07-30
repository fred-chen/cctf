#coding=utf-8

'''
内容: 演示CCTF最基本的功能: 通过一个target对象的newshell()方法获取目标设备的“shell”对象，
     并通过“shell”对象的 exe() 方法在远端设备上执行一条命令

Created on Mar 17, 2019
@author: fred
'''

from cctf import gettarget
# gettarget('10.211.55.6', 'root', 'root').newshell().exe("banner Hello CCTF!")
# gettarget('10.211.55.7', 'root', 'root').newshell().exe("banner Hello CCTF!")
# gettarget('10.211.55.9', 'root', 'root').newshell().exe("banner Hello CCTF!")
# 
# gettarget('ns.chenp.net', 'root', 'Secure myself.1').newshell().exe("banner Hello CCTF!")
gettarget('192.168.96.79', 'root', 'password').newshell().exe("banner Hello CCTF!")
gettarget('192.168.96.51', 'root', 'password').newshell().exe("banner Hello CCTF!")


#.newshell().exe("banner Hello CCTF!")

exit()










""" 分解步骤 """

""" 1. 创建一个target对象 """
raw_input("\nStep 1: create a target object.\n")
t = gettarget('10.211.55.6', 'root', 'root')


""" 2. 获取一个shell对象 """
raw_input("\nStep 2: create a shell object.\n")
sh = t.newshell()

""" 3. 通过shell对象执行一个命令 """
raw_input("\nStep 3: execute a command through the shell object.\n")
sh.exe("banner Hello CCTF!")

