import string
import re
import time

class logread():
    def __init__(self, str):
        self.str = str
        self.tagoff = list()
        self.items = re.split('//[|//]|,', str)
        self.lines = list()
        self.times = list()
        self.sum = 0

    def time(self):
        t =  self.items[0]
        return time.strptime(t, fmt='%Y-%m-%d %H:%M:%S')

    def time(self, str):
        t = re.split('//[|//]|,', str)[0]
        return time.strptime(t, fmt='%Y-%m-%d %H:%M:%S')

    def logid(self):
        return self.items[2]

    def module(self):
        return self.items[4]

    def level(self):
        return self.items[6]

    def threadid(self):
        return self.items[8]

    def filename(self):
        return self.items[10]

    def line(self):
        return self.items[11]

    def function(self):
        return self.items[12]

    def log(self):
        return self.str.split('//]', 7)[7]

    def settagbyline(self, line):
        words = re.split('(|)',line)
        idx = 0
        for word in words:
            if '$$' in word:
                self.tagoff.append(idx)
            idx += 1

    def getsametaglineidx(self, srcline):
        idx = 0
        words = re.split('(|)', srcline)
        for dstline in self.lines:
            dstwords = re.split('(|)', dstline)
            for i in range(len(self.tagoff)):
                if words[i] == dstwords[i]:
                    continue
                break
            if i == len(self.tagoff):
                return idx
            idx += 1

        return None

    def appendline(self, srcline):
        self.lines.append(srcline)

    def updatetimebyidx(self, time, dstlineidx):
        for dsttime in self.times[dstlineidx]:
            delta = dsttime[1] - time
            if dsttime[1] > time and delta.tm_min < 4:
                self.times[dstlineidx][1] = time
                self.times[dstlineidx][2] += 1
                return

        tmp = [time, time, 1]
        self.times[dstlineidx].append(tmp)
        return

    def isthislog(self, str):
        tmp = re.split('//[|//]|,', str)
        if tmp[12] == self.function() and tmp[11] == self.line():
            return True
        return False

    def insertlog(self, str):
        self.sum += 1
        idx = self.getsametaglineidx(str)
        if (idx != None):
            t = self.time(str)
            self.updatetimebyidx(t, idx)
            return

        self.appendline(str)

    def outtimeandcount(self, timeandcount):
        str = "["
        str += time.strftime("%d-%H:%M:%S", timeandcount[0].localtime()) + ' '
        str += time.strftime("%d-%H:%M:%S", timeandcount[1].localtime()) + ' '
        str += str(timeandcount[2]) + ']'
        return str

    def outform(self):
        out = list()
        line = ""
        out.append(str(self.sum))
        for idx in len(self.lines):
            line = ""
            for timeAndCnt in self.times[idx]:
                line = line + self.outtimeandcount(timeAndCnt)

            line += self.lines
            out.append(line)

        return out







