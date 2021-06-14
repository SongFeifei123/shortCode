import openpyxl
import time
import math
import sys
import os

NoCol = 0
DescriptCol = 5
FunctionCol = 1

def openExcel():
    # 打开工作簿
    rb = openpyxl.load_workbook('errDictionary.xlsx')
    return rb

def openLogFile(filename):
    if os.path.isfile(filename):
        return open(filename, 'r')
    else:
        print("log file not exist")
        exit(0)

class errFilter:
    def __init__(self, logfile):
        self.rb = openExcel()
        self.log = openLogFile(logfile)
        self.errindex = 1
        self.out = sys.stdout
        self.logfilename = logfile

    def printLastResult(self):
        if self.lastStatus == False:
            return
        printInfo  = str(self.errindex) +':[' + self.errCode + ']' + self.errInfo
        self.out.write(printInfo)
        self.errindex = self.errindex + 1

    def isLineNotExist(self, row):
        cmdSnippit = "\" | grep \""
        cmd = "grep \""
        cmd = cmd + str(row[FunctionCol].value)
        wordBeg = FunctionCol + 1
        for elem in row[wordBeg:DescriptCol - 1]:
            if elem.value == None or elem.value.isspace():
                break
            cmd = cmd + cmdSnippit + elem.value

        cmd = cmd + "\" " + self.logfilename + "| wc -l"
        # result = os.popen(cmd).read()
        result = '0'
        print(cmd)
        return result == '0'


    def getBugDiscript(self, row):
        self.errCode = row[NoCol].value
        if len(row) >= DescriptCol:
            self.errInfo = row[DescriptCol].value
        else:
            self.errInfo = "没有描述"

    def filterData(self):
        sh = self.rb['Sheet1']
        self.lastStatus = False
        self.getBugDiscript(list(sh.rows)[0])
        for row in sh.rows:
            if row[0].value != None :
                self.printLastResult()
                self.lastStatus = True
                self.getBugDiscript(row)

            if self.lastStatus == False:
                continue

            if self.isLineNotExist(row):
                self.lastStatus = False

if __name__ == "__main__":
    #logfile = sys.argv[1]
    logfile = "sblog.txt"
    errFilter = errFilter(logfile)
    errFilter.filterData()
