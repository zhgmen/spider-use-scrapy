import threading
import random
import time
Gmoney = 1000
Glock = threading.Lock()

totaltime = 10
gtime = 0
class Product(threading.Thread):
    def run(self):
        global Gmoney
        global gtime
        while True:
            money = random.randint(100,1000)
            Glock.acquire()
            print(threading.current_thread())
            
            if gtime >= 10:
                print('生产够用！')
                Glock.release()
                break
            Gmoney += money
            gtime += 1
            print('挣了 %s 元钱！' % str(money))
            Glock.release()
            time.sleep(0.5)
            

class Consumer(threading.Thread):
    def run(self):
        global Gmoney
        global gtime
        
        while True: 
            print(threading.current_thread())
            money = random.randint(100,1000)              
            Glock.acquire()

            if Gmoney < money:
                
                if gtime >= 10:
                    print('没钱了')
                    Glock.release()
                    break
                
                print('余额不足！')
            else:
                
            
                Gmoney -= money
                print('花费了 %s 元钱！' % str(money))
            Glock.release()
            time.sleep(0.5)
            

def main():
    for i in range(5):
        p = Product(name='生产者线程%d' % i)
        p.start()

    for i in range(3):
        
        c = Consumer(name='消费者线cheng%d' % i)
    
    
        c.start()
main()
