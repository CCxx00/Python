import time

class p(object):
    def __init__(self,name):
        self.name=name

class s1(p):
    def __init__(self,name,age):
        self.age=age
        p.__init__(self,name)

class s2(p):
    def __init__(self,name,gender):
        self.gender=gender
        p.__init__(self,name)

class gs(s1,s2):
    def __init__(self,name,age,gender):
        s1.__init__(self,name,age)
        s2.__init__(self,'c',gender)

def fb(n):
    if n==0:
        return 0
    elif n==1:
        return 1
    else:
        a=fb(n-1)+fb(n-2)
        # print(a)
        return a

for x in range(100):
    print(fb(x))
# sg=gs('a',111,'b')
# print(sg.name)
# print(sg.age)
# print(sg.gender)

# for i in range(101):
#     print("\r",i,end='')
#     time.sleep(0.1)
