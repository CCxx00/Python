import threading
import time

def s():
    for i in range(3):
        print(i)
        print(threading.enumerate())
        time.sleep(1)

def main():
    for i in range(3):
        t=threading.Thread(target=s)
        t.start()
        # print(threading.enumerate())

    # while True:
    #     if len(threading.enumerate())<=1:
    #         break
    #     print(threading.enumerate())

if __name__=="__main__":
    main()
