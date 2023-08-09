"""
run this script with: python case_test.py -t root:password@localhost
"""

import sys
from cctf import Case, gettarget

# 创建一个case对象
tc = Case(sys.argv[0])
print(tc.params)
print(tc.targets)

tc.step(f"Created a case object. targets: {tc.targets}, params: {tc.params}")

# 通过case对象的参数创建target列表
ts = []
for addr in tc.targets: # (user, pass, address)
    ts.append(gettarget(addr[2], addr[0], addr[1]))

tc.step(f"Created a target list: {ts}")

# 从列表中的每个target对象获取其shell对象
shs = []
for t in ts:
    shs.append(t.newshell())

tc.step(f"Created a shell list: {shs}")

# 通过shell对象在target上执行命令
cos = []
for sh in shs:
    co = sh.exe("hostname", wait=True, log=True)
    cos.append(co)

tc.step(f"Executed a series of command on each shell: {cos}")

tc.fail()
