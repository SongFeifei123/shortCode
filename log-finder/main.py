# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import task_common
import task_compare
import task_prework
import task_statistic
import argparse

def printhelper():
    print("used ERR")


# Press the green button in the gutter to run the script.

if __name__ == "__main__":
    parse = argparse.ArgumentParser(description='aikv log tool')
    parse.add_argument('-pwork', action='store_const', default='statistic', dest='work', const='prework', help='Pre work only')
    parse.add_argument('-stat', action='store_const', default='statisitc', dest='work', const='statistic', help='Statistic work only')
    parse.add_argument('-cmp', action='store_const', default='statistic', dest='work', const='compare', help='statistic work only')
    parse.add_argument('-infile', nargs='+', help='infile,default: infile.log', default='infile.log')
    parse.add_argument('-outfile', nargs=1, help='outfile, default: screen', default='screen')
    parse.add_argument('-thread', nargs=1, type=int, default=1, help='multi thread')

    args = parse.parse_args()
    worktype = args.work
    if worktype == 'xml':
        task = task_prework.preworktask('prework.xml')
    elif worktype == 'prework':
        task = task_prework.preworktask(args.infile, args.outfile[0])
    elif worktype == 'statistic':
        task = task_statistic.statistictask(args.infile[0], args.outfile[0])
    elif worktype == 'compare':
        task = task_compare.comparetask(args.infile, args.outfile[0])
    task.exec()




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
