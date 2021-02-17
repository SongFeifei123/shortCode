import task_common
import json
import sys
class comparetask(task_common.task):
    def getconfig(self):
        self.name = "comparetask"
        root = self.getxml()
        #modules
        item = []
        group = []
        modules = root.getElementsByTagName('modules')
        # item : 0 modulesname 1-3 level 4-6 outfiles
        for module in modules:
            item[0] = module.getElementsByTagName('string')[0].nodeName
            levels  = module.getElementsByTagName('level')
            i = 1
            for level in levels:
                item[i] = level.nodeName
                i = i + 1

            while i < 4:
                item[i] = None

            outfiles = module.getElementsByTagName('outfile')
            for outfile in outfiles:
                item[i] = outfile.nodeName
                i = i + 1

            while i < 7:
                item[i] = None
            group.append(item)
        self.modules = group
        #比较文件
        errfiles = root.getElementsByTagName("errfile")
        self.errfiles = []
        for file in errfiles:
            self.errfiles.append(file.nodename)

        rightfiles = root.getElementsByTagName("rightfile")
        self.rightfiles = []
        for file in rightfiles:
            self.rightfiles.append(file.nodename)

    def cmdconfig(self):
        self.name = "compare task"
        if len(self.infiles) != 2:
            print("Compare task need 2 infile, curinfile:{}".format(len(self.infiles)))
            exit(0)

    def getDict(self, file):
        with open(file, 'r') as json_file:
            dic = json.load(json_file)
        return dic

    def strSimilar(self, str1, str2, similar):
        word1 = str1.split(' |(|)|,|.')
        word2 = str2.split(' |(|)|,|.')
        correct = 0
        error   = 0
        for i in range(len(word1)):
            if word1[i].isalpha():
                if word1[i] == word2[i]:
                    correct += 1
                else:
                    error += 1
        result = correct * 100 / (correct + error)
        if result >= similar:
            return True
        return False

    def getSameFuncInDict(self, dict, func, i):
        result = list()
        while True:
            if self.getFuncByline(dict[i][1]) == func:
                result.append(dict[i])
            else:
                return result
            i += 1

    def appendDiffLogs(self, clogs, elogs, result):
        for elog in elogs:
            eLogInfo = self.getLogInfoByLine(elog[1])
            isSimilar = False
            for clog in clogs:
                clogInfo = self.getLogInfoByLine(clog[1])
                if self.strSimilar(eLogInfo, clogInfo, 100):
                    isSimilar = True
                    break
            if not isSimilar:
                result.append(elog)

    def findDifferent(self, corr, err):
        corr = sorted(corr)
        err = sorted(err)
        reseult = []
        while True:
            cIdx = 0
            eIdx = 0
            if corr[cIdx] == None or None == err[eIdx]:
                break
            cfunc = self.getFuncByline(corr[cIdx])
            efunc = self.getFuncByline(err[eIdx])
            if cfunc == efunc:
                clogs = self.getSameFuncInDict(corr[cIdx])
                elogs = self.getSameFuncInDict(err[eIdx])
                self.appendDiffLogs(clogs, elogs, reseult)
                cIdx += len(clogs)
                eIdx += len(elogs)
            elif cfunc > efunc:
                reseult.append(err[eIdx])
                eIdx += 1
            else:
                cIdx += 1

        while eIdx < len(err):
            reseult.append(err[eIdx])
            eIdx += 1
        return  reseult

    def delSame(self, dict1, dict2):
        for item in dict1:
            if dict2.has_key(item.key):
                del dict1[item.key]
                del dict2[item.key]

    def dowork(self):
        if not self.useconfig:
            dict1 = self.getDict(self.infiles[0])
            dict2 = self.getDict(self.infiles[1])
            self.delSame(dict1, dict2)
            if self.outfiles[0] != 'screen':
                fd  = open(self.outfile[0], 'w+')
            else:
                fd = sys.stdout
            fd.writelines('file1:')
            json.dump(dict1, fd, indent=1)
            fd.writelines('file2:')
            json.dump(dict2, fd, indent=1)

        for idx in range(1,len(self.rightfiles)):
            correctDict = self.getDict(self.rightfiles[idx])
            errorDict   = self.getDict(self.errfiles[idx])
            result      = self.findDifferent(correctDict, errorDict)
            fd          = self.openoutfile(self.outfiles[idx])
            json.dump(result, fd, indent=1)
