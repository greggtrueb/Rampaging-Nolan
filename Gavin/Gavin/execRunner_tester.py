import sys
import threading
import time
import random
from execRunner import execRun
import os

def run_consumer():
    e1 = execRun("python execRunner_tester.py {0}".format("e1"))
    e2 = execRun("python execRunner_tester.py {0}".format("e2"))

    execRun.runAsync(e1)
    execRun.runAsync(e2)

    e1Combined = ""
    e2Combined = ""

    while not e1.has_exited():
        e1Out = e1.get_next_output()
        e2Out = e2.get_next_output()

        output = None
        if(e1Out is not None):
            e1Combined = e1Combined + e1Out
            output = e1Out

        if(e2Out is not None):
            e2Combined = e2Combined + e2Out
            if output is not None:
                output = output + e2Out
            else:
                output = e2Out

        if output is not None:
            sys.stdout.write(output)
            sys.stdout.flush()
            output = None
        time.sleep(15)

    e1Out = e1.get_next_output()
    e2Out = e2.get_next_output()

    if(e1Out is not None):
        e1Combined = e1Combined + e1Out
        output = e1Out

    if(e2Out is not None):
        e2Combined = e2Combined + e2Out
        output = output + e2Out

    if output is not None:
        sys.stdout.write(output)
        sys.stdout.flush()
        output = None

    print(e1Combined == e1.get_output())
    print(e2Combined == e2.get_output())


def run_producer(arg):
    out = arg
    if arg is None:
        out = "Sample output"
    
    terminate = 20
    while terminate > 0:
        os.system("echo " + out + ": Thread {0} : time {1}".format(threading.get_ident(), time.time()))
        terminate = terminate - 1
        
        time.sleep(random.randint(1,20))

    sys.exit(random.randint(10,20))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        run_consumer()
    else:
        run_producer(sys.argv[1])

