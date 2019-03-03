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

sg=gs('a',111,'b')
print(sg.name)
print(sg.age)
print(sg.gender)
