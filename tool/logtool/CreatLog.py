# -*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
        filename='new.log',
        filemode='w',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
        format=
        '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
        )
logger = logging.getLogger(__name__)
def CreateLog(type):
    if type == 0:
        logger.info("Start print log")
    elif type == 1:
        logger.debug("Do something")
    elif type == 2:
        logger.warning("Something maybe fail.")
    else:
        logger.info("Finish")

for i in range(400000):
    CreateLog(i % 4)
