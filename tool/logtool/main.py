# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import re
filename = "./new.log"
targetfile = "./tmp.log"
dictionary = [
    "INFO"
]
def openFiles():
    srcfd = open(filename, 'r')
    tarfd = open(targetfile, 'w')
    return srcfd, tarfd

def lineINdictionary(str):
    for item in dictionary:
        if item in str:
            return True
    return False

def filterLinesbyConfig(lines):
    result = []
    for line in lines:
        if lineINdictionary(line):
            continue
        result.append(line)
    return result

def shortLogline(lines):
    result = []
    for line in lines:
        sline = re.split("[\]\[]",line)
        result.append(sline[len(sline) - 1])
    return result

def showLog(fd, lines):
    fd.writelines(lines)

def closeFiles(fd1, fd2):
    fd1.close()
    fd2.close()

def openinVIM():
    cmd = "vim {}".format(targetfile)
    os.system(cmd)

def clearLog():
    srcfd, resultfd = openFiles()
    while 1:
        lines = srcfd.readlines(1000)
        if len(lines) == 0:
            break
        lines = filterLinesbyConfig(lines)
        lines = shortLogline(lines)
        showLog(resultfd, lines)
    closeFiles(srcfd, resultfd)
    openinVIM()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    clearLog()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
