'''
Created on Aug 25, 2018

@author: fred
'''

import common
from Queue import Queue
from connfactory import connect
import threading
import random
from command import command
import re
import datetime

class shell(common.common, threading.Thread):
    def __init__(self, target, conn=None):
        threading.Thread.__init__(self)
        self.q = Queue()
        self.t = target
        self.conn = conn
        self.connect()
        self.setDaemon(True)
        self.start()
        
    def connect(self):
        if (self.conn is None):
            self.conn = connect(self.t.address, self.t.username, self.t.password, self.t.svc, self.t.timeout, self.t.newline)
        return self.conn
    def reconnect(self):
        self.disconnect()
        return self.connect()
    def disconnect(self):
        if self.conn:
            self.conn.disconnect()
        self.conn = None
    
    def exe(self, cmdline, wait=True, log=True):
#         if not self.conn.connected():
#             self.connect()
        cmdobj = command(cmdline, log)
        cmdobj.shell = self
        self.q.put(cmdobj)
        if wait:
            cmdobj.wait()
        return cmdobj
    
    def getconn(self):
        return self.conn
    
    def run(self):
        while True:
            cmdobj = self.q.get()
            filename = "%s_%s" % (threading.current_thread().ident, random.randrange(1000000000))
            cmdobj.reserve = filename
            self._sendcmd(cmdobj)
            start = datetime.datetime.now()
            self._getresults(cmdobj)
            diff = datetime.datetime.now() - start
            cmdobj.dur = diff.total_seconds() * 1000
            cmdobj.setdone()
    
    def _sendcmd(self, cmdobj):
        cmdline = cmdobj.cmdline.replace('"', r'\"')
        cmd  = "FN=/tmp/%s;" % (cmdobj.reserve)
        cmd += 'eval "%s" > ${FN}.out 2>${FN}.err;echo $?>${FN}.exit;' % (cmdline)
        cmd += "echo ==${FN}START==;"
        cmd += "cat ${FN}.out;echo ==OUTEND==;"
        cmd += "cat ${FN}.err;echo ==ERREND==;"
        cmd += "cat ${FN}.exit;echo ==EXITEND==;"
        cmd += "echo ==${FN}END==;"
        cmd += "rm -f ${FN}.out ${FN}.err ${FN}.exit"
        self.conn.write(cmd)
        self.conn.nl()
        # print (cmd)
    
    def _getresults(self, cmdobj):
        txt = self.conn.waitfor("==/tmp/%sEND==" % (cmdobj.reserve))
        reg = re.compile("==/tmp/%sSTART==(.+)==OUTEND==(.+)==ERREND==(.+)==EXITEND==.+==/tmp/%sEND==" % (cmdobj.reserve, cmdobj.reserve), re.DOTALL)
        m = reg.search(txt)
        cmdobj.stdout = m.group(1)
        cmdobj.stderr = m.group(2)
        cmdobj.exit = m.group(3)
        
