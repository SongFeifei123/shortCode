import task_common
import json
import sys

class statistictask(task_common.task):
    def getconfig(self):
        self.name = "statisitctask"
        root = self.getxml()
        infiles = root.getElementsByTagName('infile')
        for infile in infiles:
            self.infiles.append(infile.firstChild.data)

        outfiles = root.getElementsByTagName('outfile')
        for outfile in outfiles:
            self.outfiles.append(outfile.firstChild.data)

        self.genSubTask(root)

    def cmdconfig(self):
        self.name = "statistictask"
        if len(self.infiles) != 1:
            print("Statistic task need 1 infile, curinfile:{}".format(len(self.infiles)))
            exit(0)

    def getFileAndLine(self, line):
        words = line.split()
        if len(words) > 2:
            return words[1]+words[2]
        return None

    def statisticLine(self, infd, outfd):
        countdict = dict()
        while True:
            lines = infd.readlines(task_common.readline)
            if len(lines) == 0:
                break
            for line in lines:
                fileAndLine = self.getFileAndLine(line)
                if fileAndLine == None:
                    continue
                item = countdict.get(fileAndLine)
                if item == None:
                    countAndLine=[1, line]
                    countdict[fileAndLine] = countAndLine
                else:
                    countdict[fileAndLine][0] += 1
        json.dump(countdict, outfd, indent=1)

    def dowork(self):
        for i in range(1, len(self.infiles)):
            infd = self.openinfile(self.infiles[i])
            if not self.useconfig and self.outfiles[0] == 'screen':
                outfd = sys.stdout
            else:
                outfd = openwritefile(self.outfiles[i])
            self.statisticLine(infd, outfd)


