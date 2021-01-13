# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import task_common
import task_compare
import task_prework
import task_statistic

def printhelper():
    print("used ERR")

def maketask(argv):
    if (argv[0] == "prework"):
        return task_common.task("prework", )


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    task = task_statistic.statistictask('statistic.xml')
    task.exec()

if __name__ == 'noth':
    if (len(sys.argv) <= 1):
        printhelper()
    task = maketask(sys.argv)
    task.exec()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
