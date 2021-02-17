import argparse

if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("N", nargs='*', help = "default input")
    parse.add_argument('--foo', nargs=1 ,help = "foo help")
    parse.add_argument('--prework', dest = 'worktype', action='store_const', const = 'prework', default = 'prework')
    parse.add_argument('--cmp', dest = 'worktype',action='store_const', const = 'cmp', default = 'prework')
    parse.add_argument('--statistic', dest = 'worktype', action='store_const', const = 'statistic', default = 'prework')
    args =  parse.parse_args()
    print(args)
    print(parse.parse_args().foo[0])
