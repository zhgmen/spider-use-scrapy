import threading
import random
import time
Gmoney = 1000
condition = threading.Condition()


gtime = 0
class Product(threading.Thread):
    def run(self):
        global Gmoney
        global gtime
        while True:
            money = random.randint(100,1000)
            condition.acquire()
            print(threading.current_thread())
            
            if gtime >= 10:
                print('生产够用！')
                condition.release()
                break
            Gmoney += money
            gtime += 1
            print('挣了 %s 元钱！' % str(money))
            condition.notify_all()
            condition.release()
            time.sleep(0.5)
            

class Consumer(threading.Thread):
    def run(self):
        global Gmoney
        global gtime
        
        while True: 
            print(threading.current_thread())
            money = random.randint(100,1000)
            condition.acquire()
            while money >= Gmoney:
                if gtime >= 10:
                    print('不生产了')
                    condition.release()
                    return
                condition.wait()
            Gmoney -= money
            print('花费 %d 元钱！' % money)
            condition.release()
            time.sleep(0.5)
            

def main():
    for i in range(5):
        p = Product(name='生产者线程%d' % i)
        p.start()

    for i in range(3):
        
        c = Consumer(name='消费者线cheng%d' % i)
    
    
        c.start()
main()
