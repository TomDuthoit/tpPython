#C:\Users\Henri Hoyez\PycharmProjects\Watcher

#---------------------------
#import liraries.
#---------------------------

import argparse         #Argument parsing library.
import logging
import threading
from logging.handlers import RotatingFileHandler
import os
import platform


#---------------------------
#Variables
#---------------------------

separator = None



#---------------------------
#functions
#---------------------------



def tree(logger:logging.Logger,path, depth):
    current_depth = path.count(separator)
    maxDepth = current_depth + depth

    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            try:
                fileToString(os.path.join(root, name))
            except Exception as e:
                logger.debug("not a text file")

            logger.debug(os.path.join(root, name))

        for name in dirs:
            logger.debug(os.path.join(root, name))
            current_depth = os.path.join(root, name).count(separator)
            logger.debug(current_depth)
        if current_depth >= maxDepth:
            logger.debug("breakpoint")
            return


def fileToString(file):
    myFile = open(file, "r")
    tab = myFile.readlines()
    myFile.close()

def callback(logger:logging.Logger):
    logging.debug("bonjour")


def setInterval(logger:logging.Logger,path,deep,func,time):
    e = threading.Event()
    while not e.wait(time):
        func(logger,path,deep)



def compare(file1,file2, logger:logging.Logger):
    del_text = list()       #the deleted text,
    add_text = list()       #the added text,
    diff_a = dict()         #in a, not in b ; the rest = the deleted file
    diff_b = dict()         #in b, not in a ; the rest = the added file
    dict_a = file1
    dict_b = file2



    for key in dict_b.keys():
        if  key in dict_a.keys():           #same keys
            if dict_b[key] == dict_a[key]:  #file unchanged
                print('file',key,'did not change')
            else:                          #file changed
                del_text = list(set(dict_a[key])-set(dict_b[key]))     #Deleted Value
                add_text = list(set(dict_b[key])-set(dict_a[key]))     #Added Value
                if len(del_text):
                    print('text',key,'deleted',del_text)
                if len(add_text):
                    print('text',key,'added',add_text)

            #after logger these two should initialize
    else:                               #different keys
        diff_b[key] = dict_b[key]


    for key in dict_a.keys():
        if not key in dict_b.keys():        #different keys
            diff_a[key] = dict_a[key]

    for key1 in list(diff_a.keys()):
        for key2 in list(diff_b.keys()):
            if diff_a[key1] == diff_b[key2]:
                del(diff_a[key1])
                del(diff_b[key2])
                print('file',key1,'changed name to',key2)
                break

    for key in diff_a.keys():
        print('file',key,'have been deleted')

    for key in diff_b.keys():
        print('file',key,'have been created')


def my_main():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='Find modification of two Directories.')
    parser.add_argument("-v","--verbose",help="increase the verbosity",action="store_true")
    parser.add_argument("location_1",type=str,help="first location.")
    parser.add_argument("-d","-deep",type=int,help="specify the deeeeeeeep.")
    parser.add_argument("-i","-interval",type=int,help="specify Interval")
    parser.add_argument("output",type=str,help="set OutputFile")

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(levelname)s] %(message)s')

    stream_handler = logging.StreamHandler()
    file_handler = None

    args = parser.parse_args()
    print(args)

    if args.verbose is None:
        stream_handler.setLevel(logging.WARNING)
    else:
        stream_handler.setLevel(logging.DEBUG)

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.debug("Verbose Mode")

    if args.output is not None:
        logger.debug("Output specified:"+ args.output)
        file_handler = RotatingFileHandler(args.output, 'a', 1000000, 1)
    else:
        logger.debug("default Output : rapport.log.")
        file_handler = RotatingFileHandler("rapport.log", 'a', 1000000, 1)

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s'))
    logger.addHandler(file_handler)


    if args.i is not None:
        logger.debug("Interval set to :")
        setInterval(logger,"C:\\",3,tree,args.i)    # Set a interval of <args.i> seconds and call the "callback" function
                                                     # just put "compare" if you want to call the compare function
        return
    else:
        logger.debug("Interval diabled")

#---------------------------
#main
#---------------------------

if __name__ == '__main__':
    """MAIN """
    if platform.system() == "Windows":
        separator = '\\'
    else:
        separator = "/"

    my_main();
