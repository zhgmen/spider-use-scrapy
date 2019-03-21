from queue import Queue
import time
import threading



#q.qsize()

def put_value(q):
    value = 0
    while True:
        q.put(value)
        value += 1
        time.sleep(2)


def get_value(q):
    while True:
        print(q.get())

def main():
    q = Queue(4)
    #for i in range(2):
    t2 = threading.Thread(target=put_value,args=[q])
    
    t1 = threading.Thread(target=get_value,args=[q])
    t1.start()
    t2.start()
    

main()
