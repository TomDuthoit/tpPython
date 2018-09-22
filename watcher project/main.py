#C:\Users\Henri Hoyez\PycharmProjects\Watcher

#---------------------------
#import liraries.
#---------------------------

import argparse         #Argument parsing library.
import logging
import threading

#---------------------------
#Variables
#---------------------------

output = "raport.log"   #Default log file location. Where the program is executed.

#---------------------------
#functions
#---------------------------



def callback(logger:logging.Logger):
    logging.debug("bonjour")


def setInterval(logger:logging.Logger,func,time):
    e = threading.Event()
    while not e.wait(time):
        func(logger)


def my_main():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='Find modification of two Directories.')
    parser.add_argument("-v","--verbose",help="increase the verbosity",action="store_true")
    parser.add_argument("location_1",type=str,help="first location.")
    parser.add_argument("location_2",type=str ,help="second location")
    parser.add_argument("-i","-interval",type=int,help="specify Interval")
    parser.add_argument("-o","--output",type=str,help="set OutputFile")

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(levelname)s] %(message)s')

    stream_handler = logging.StreamHandler()


    args = parser.parse_args()

    if args.verbose is None:
        stream_handler.setLevel(logging.WARNING)
    else:
        stream_handler.setLevel(logging.DEBUG)

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.debug("Verbose Mode")

    if args.output is not None:
        logger.debug("Output specified:"+ args.output)
    else:
        logger.debug("default Output : rapport.log.")

    if args.i is not None:
        logger.debug("Interval set to :")
        setInterval(logger,callback,args.i)
        return
    else:
        logger.debug("Interval diabled")
#---------------------------
#main
#---------------------------

if __name__ == '__main__':
    """MAIN """
    my_main();
