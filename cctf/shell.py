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
import re, datetime, time, uuid

class shell(common.common, threading.Thread):
    def __init__(self, target, conn=None, timeout=300):
        threading.Thread.__init__(self)
        self.q = Queue()
        self.t = target
        self.conn = conn
        self.timeout = timeout
        self.id = str(uuid.uuid4()).split('-')[0]
        self.connect()
        self.setDaemon(True)
        self.start()
        
    def connect(self):
        if (self.conn is None):
            self.conn = connect(self.t.address, self.t.username, self.t.password, self.t.svc, self.t.timeout, self.t.newline)
        if self.conn: self.setshell()
        return self.conn
    def setshell(self):
        self.conn.write("set +H")
        self.conn.nl()
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
            start = datetime.datetime.now()
            for i in range(1, 6):
                broken = False
                if self._sendcmd(cmdobj) is None:
                    broken = True
                start = datetime.datetime.now()
                cmdobj.start = start
                if self._getresults(cmdobj) is None:  # connection broken
                    broken = True
                if broken:
                    dur = 0; alive = False
                    timeout = self.timeout if self.timeout else 300
                    self.log("connection broken. resending command '%s'. timeout %d secs, attempt %d ..." % (cmdobj.cmdline, timeout, i), 2)
                    while True:
                        if self.t.alive():
                            alive = True
                            break
                        else:
                            time.sleep(1)
                            dur += 1
                            if dur > timeout: break
                    if alive: self.reconnect()
                    continue
                else:
                    break
            diff = datetime.datetime.now() - start
            cmdobj.dur = diff.total_seconds() * 1000
            cmdobj.setdone()
    
    def _sendcmd(self, cmdobj):
        cmdline = cmdobj.cmdline.replace('"', r'\"')
        cmd  = "FN=/tmp/%s;" % (cmdobj.reserve)
        cmd += 'eval "%s" > >(tee ${FN}.out) 2> >(tee ${FN}.err >&2); echo $?>${FN}.exit; sync;' % (cmdline)
        cmd += "echo ==${FN}START==;"
        cmd += "cat ${FN}.out;echo ==OUTEND==;"
        cmd += "cat ${FN}.err;echo ==ERREND==;"
        cmd += "cat ${FN}.exit;echo ==EXITEND==;"
        cmd += "echo ==${FN}END==;"
        cmd += "rm -f ${FN}.out ${FN}.err ${FN}.exit"
        if (not self.conn) or self.conn.write(cmd) is None:
            return None
        return self.conn.nl()
    
    def _getresults(self, cmdobj):
        txt = None
        regScreen = re.compile("==/tmp/%sSTART==(.+)==OUTEND==(.+)==ERREND==(.+)==EXITEND==.+==/tmp/%sEND==" % (cmdobj.reserve, cmdobj.reserve), re.DOTALL)
        if self.conn:
            while True:
                txt = self.conn.waitfor("==/tmp/%sEND==" % (cmdobj.reserve), 3)
                if txt is None:   # connection broken
                    cmdobj.stdout = None
                    cmdobj.stderr = None
                    cmdobj.exit = None
                    return txt
                cmdobj.screentext += txt.replace(self.UNIQIDENTIFIER, "")
                m = regScreen.search(cmdobj.screentext)
                if m:   # command finished
                    break
        m = regScreen.search(cmdobj.screentext)
        cmdobj.stdout     = m.group(1)
        cmdobj.stderr     = m.group(2)
        cmdobj.exit       = m.group(3)
        return txt
        
