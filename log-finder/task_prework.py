import task_common
import os


outdir = os.getcwd() + '/prework'

class preworktask(task_common.task):

    def getconfig(self):
        self.name = "preworktask"
        root = self.getxml()
        self.infiles = self.getInfilesByXml(root)
        #modules
        items = []
        group = []
        modules = root.getElementsByTagName('module')
        # item : 0 modulesname 1-3 level 4-6 outfiles
        for module in modules:
            items = []
            item = module.getElementsByTagName('string')[0].firstChild.data
            items.append(item)
            levels  = module.getElementsByTagName('level')
            i = 1
            for level in levels:
                items.append(level.firstChild.data)
                i = i + 1

            while i < 4:
                items.append(None)
                i += 1

            outfiles = module.getElementsByTagName('outfile')
            for outfile in outfiles:
                items.append(outfile.firstChild.data)
                i = i + 1

            while i < 7:
                items.append(None)
                i += 1
            group.append(items)
        self.modules = group
        # end modules
        self.next = task_common.task(self.getSubTaskCfg(root))

    def filterAndWrite(self, line):
        for module in self.modules:
            if module[0] in line:
                for i in [1, 2, 3]:
                    if module[i] in line:
                        self.outfds[i].write(line)
                        return

    def dowork(self):
        infd = self.openinfile(self.infiles[1])
        self.openoutfile()
        while True:
            lines = infd.readlines(task_common.readline)
            if lines[0] == '':
                break
            for line in lines:
                self.filterAndWrite(line)

        self.closeoutfile()
