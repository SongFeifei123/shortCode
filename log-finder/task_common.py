import xml.dom.minidom
import tarfile
import re
import memctl
import os

readline = 1000

def openwritefile(file):
    return open(file, 'w+')

class task:
    def __init__(self, configfile):
        self.next = None
        self.xml = configfile
        self.infiles = []
        self.outfiles = []
        self.results = None
        self.useconfig = True

    def __init__(self, infile, outfile):
        self.next = None
        self.infiles = infile
        self.outfiles = [outfile]
        self.useconfig = False

    def getFuncByline(self, line):
        return line.split()[3]

    def getLogInfoByLine(self, str):
        i = 0
        for t in range(3):
            i = str.find(']')
            i += 1
        return str[i:]

    def openfile(self, file):
        return open(file)

    def opentar(self, file):
        with tarfile.open(file, 'r') as t:
            for member_info in t.getmembers():
                if re.match('.*dsware_idx.*', member_info.name, re.I):
                    f = t.extractfile(member_info.name)
                    return f

    def openinfile(self, file):
        if re.match('.*.tar.bz', file, re.I) != None:
            return self.opentar(file)
        else:
            return self.openfile(file)

    def openoutfile(self):
        self.outfds = [0]  #第一个字符填0,目的是跳过第一个元素，以匹配modules的level
        self.outlines = [""]
        lines = list()
        for module in self.modules:
            for i in [1, 2, 3]:
                fd = None
                if module[i] != None:
                    for j in range(1,i):
                        if module[j] == module[i]:
                            fd = self.outfds[j - 1]
                    if fd == None:
                        fd = open(module[i + 3])
                self.outfds.append(fd)
                self.outlines.append(lines)

    def closeoutfile(self):
        for fd in self.outfds:
            if fd != None:
                fd.close()

    def genSubTask(self, root):
        subtask = root.getElementsByTagName('subtask')
        if len(subtask) == 0:
            self.subtask = None
            return
        subtaskname = subtask[0].getElementsByTagName('name').firstChild.data
        config = subtask[0].getElementsByTagName('config').firstChild.data
        cmd = 'self.subtask = {}({})'.format(subtaskname, config)
        eval(cmd)

    def getxml(self):
        if self.xml == None:
            assert(0)
        dom = xml.dom.minidom.parse(self.xml)
        root = dom.documentElement
        return root

    def getInfilesByXml(self, root):
        group = root.getElementsByTagName('infile')
        infiles = []
        for item in group:
            infiles.append(item.nodeName)
        return infiles

    def getSubTaskCfg(self, root):
        subtask = root.getElementsByTagName('subtaskcfg')
        if len(subtask) != 0:
            return subtask[0].nodeName
        else:
            return None

    def addsubTask(self, task):
        tmp = self.next
        while tmp.next != None:
            tmp = tmp.next
        tmp.next = task

    def getconfig(self):
        pass

    def cmdconfig(self):
        pass

    def dowork(self):
        pass

    def dosubtask(self):
        if self.next != None:
            self.next.exec()

    def exec(self):
        if self.useconfig:
            self.getconfig()
        else:
            self.cmdconfig()
        self.dowork()
        self.dosubtask()


