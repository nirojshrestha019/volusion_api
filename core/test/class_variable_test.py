

class test:
    c_v = 1
    def __init__(self):
        self.a = 'aaa_'
        print("{}{}".format(self.a, test.c_v))
        print(test.c_v)
        print(type(test.c_v))

        test.c_v+=1


# for i in range(0, 5):
o1 = test()
o2 = test()
