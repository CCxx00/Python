import multiprocessing

def a(q):
    for i in range(100):
        q.put(i)

def b(q):
    while True:
        print(q.get())
        if q.empty():
            break

def main():
    q=multiprocessing.Queue()
    p1=multiprocessing.Process(target=a,args=(q,))
    p2=multiprocessing.Process(target=b,args=(q,))
    p1.start()
    p2.start()

if __name__=="__main__":
    main()
