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
intervalTime = 2
maxDepth = 5



#---------------------------
#functions
#---------------------------

##################################################################

def tree(logger:logging.Logger,buffer,path, depth):
    current_depth = path.count(separator)
    maxDepth = current_depth + depth
    my_tree = dict()
    i = 0
    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            try:
                tab = fileToString(os.path.join(root, name))
                my_tree[os.path.join(root, name)] = (tab)
                i = i+1

            except Exception as e:
                my_tree[os.path.join(root, name)] = (None)
                i = i + 1
                logger.debug("not a text file")

            #logger.debug(os.path.join(root, name))

        for name in dirs:
            logger.debug(os.path.join(root, name))
            current_depth = os.path.join(root, name).count(separator)
            logger.debug(current_depth)
        if current_depth >= maxDepth:
            logger.debug("breakpoint")
            compare(buffer,my_tree,logger)
            return my_tree

    compare(buffer,my_tree,logger)
    return my_tree


def fileToString(file):
    myFile = open(file, "r")
    tab = myFile.readlines()
    myFile.close()
    return tab

##################################################################



def setInterval(logger:logging.Logger,path,deep,func,time):
    e = threading.Event()
    fileBuffer = None
    while not e.wait(time):
        fileBuffer = func(logger,fileBuffer,path,deep)




def compare(file1,file2 ,logger:logging.Logger):
    del_text = list()       #the deleted text,
    add_text = list()       #the added text,
    diff_a = dict()         #in a, not in b ; the rest = the deleted file
    diff_b = dict()         #in b, not in a ; the rest = the added file
    dict_a = file1
    dict_b = file2




    if file1 is None:
        print("mdr None.")
        return



    for key in dict_b.keys():
        if  key in dict_a.keys():           #same keys
            if dict_b[key] != dict_a[key]:  #file changed
                a_b = list(set(dict_a[key])-set(dict_b[key]))
                b_a = list(set(dict_b[key])-set(dict_a[key]))

                for i in range(len(b_a)):   #delete \n
                   if '\n' in b_a[i]:
                        b_a[i] = b_a[i][:-1]
                        print(b_a[i])

                for i in range(len(a_b)):   #delete \n
                   if '\n' in a_b[i]:
                        a_b[i] = a_b[i][:-1]
                        print(a_b[i])

                for i in range(len(b_a)):
                    for j in range(len(a_b)):
                        if a_b[j] in b_a[i]:
                            print('text',a_b[j],'changed to',b_a[i])
                            b_a[i] = a_b[j]
                            break
                        if b_a[i] in a_b[j]:
                            print('text',b_a[i],'changed to',a_b[j])
                            b_a[i] = a_b[j]
                            break

                m1=list(set(a_b)-set(b_a))
                m2=list(set(b_a)-set(a_b))

                for j in range(len(m1)):
                    del_text.append(m1[j])
                for i in range(len(m2)):
                    add_text.append(m2[i])

                if len(del_text):
                    print('text',key,'deleted',del_text)
                if len(add_text):
                    print('text',key,'added',add_text)
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
    parser.add_argument("-i","-interval",action="store_true",help="specify Interval")
    parser.add_argument("output",type=str,help="set OutputFile")

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(levelname)s] %(message)s')

    stream_handler = logging.StreamHandler()
    file_handler = None

    args = parser.parse_args()
    print(args)

    if args.verbose:
        print("GOOD")
        stream_handler.setLevel(logging.DEBUG)
    else:
        stream_handler.setLevel(logging.INFO)

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
        setInterval(logger,args.location_1,maxDepth,tree,intervalTime)    # Set a interval of <args.i> seconds and call the "callback" function
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
