class Base(object):
    def __init__(self):
        print "Constructor without an argument"
    def __init__(self, id):
        print "I was called from Base with an id", id

    def aMethod(self):
        print "a Method was called"

class Child(Base):
    def __init__(self, id):
        #super(Child, self).__init__(id)
        print "I was called from Child"



child = Child(2)
child.aMethod()