import time
import datetime
import sys
import subprocess
import argparse
import os.path

def main(args):
    
    workers = []
    NoRun = 0
    StartRequestNo = args.min
    Increase = args.increase
    KeepCycle = True
    NoWorker = None
    try:

        while KeepCycle:
            NoRun += 1 #the number of run
            NoWorker = StartRequestNo + Increase * (NoRun-1) #the number of workers in the current run
            if args.max and NoWorker >= args.max: #if arg max is not None and the NoWorker is greater then it
                NoWorker = args.max
                KeepCycle = False #this is going to end the cycle at the current run
            print("Run" + str(NoRun))
            OriginalTime = int(time.mktime((datetime.datetime.now()+datetime.timedelta(seconds=3)).timetuple()))
            # this keeps when the instanciated workers should start wokring 3 seconds from the current time
            intervall = 1000000/NoWorker #the interwall is supposed to balance the loads in the second

            print("Initializing "+str(NoWorker) + " workers")
            for i in range(NoWorker): #initializing workers with 3 parameters: max wait time, URL, exact time to start
                StartTime = str(OriginalTime) + "." + str(intervall*i)
                workers.append(subprocess.Popen(["python", "./worker.py", str(args.time), args.webpage, StartTime], stdout=subprocess.PIPE))
            print("Waiting for workers to finish")
            errors = []
            for i in range(NoWorker): #going trough all workers and checking for a non 0 exis status
                stdout = workers[i].communicate()
                ErrorLevel = workers[i].poll()
                if ErrorLevel != 0:
                    errors.append((stdout, ErrorLevel, "worker"+str(i+1)))
            if len(errors) > 0: #logging the output of non 0 status workers
                print "Found Error:"
                for i in errors:
                    print "----------------------------------" + i[2] + "----------------------------------"
                    print i[0][0]
                    print i[1]
                print str(len(errors))+"/"+str(NoWorker) + " Failed to connect to URL:" + args.webpage
                sys.exit(NoWorker)
            del errors[:]
            del workers[:]
    except KeyboardInterrupt:
        print "Keyboard Interrupt: Exiting with " + str(NoWorker) + " workers"
        time.sleep(2)
        (i.kill() for i in workers)
        del workers[:]



if __name__=="__main__":

    description = """This tool is created to test a certain URL under load.
    In each run the test starts a number of workers to connect to a given URL.
    Balancing the load every worker connects in he same second but even.
    In each run the number of workers is increased.
    The test stops when the maximum number of workers is reached or one of the connections fail.

    The run of the test can be Interrupted with Ctrl + C.

    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("webpage", help="The url to the webpage to test")
    parser.add_argument("-i", "--increase", help="The amount of new connecions in new testruns. Default is 10", default=10, type=int)
    parser.add_argument("-m", "--max", help="Max number of connections. Default is 100", default=100, type=int)
    parser.add_argument("-l", "--min", help="Minimum number of connections. Default is 10", default=10, type=int)
    parser.add_argument("-t", "--time", help="The maximum amount of time [s] a worker waits for and answer from the server", default=5, type=int)
    args = parser.parse_args()
    main(args)
    sys.exit(0)
