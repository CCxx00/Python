import multiprocessing

def a(c):
    for i in range(2):
        c.append('a')

def b(c):
    while True:
        print(c)

def main():
    c=list()
    p1=multiprocessing.Process(target=a,args=(c,))
    p2=multiprocessing.Process(target=b,args=(c,))
    p1.start()
    p2.start()

if __name__=="__main__":
    main()
