
def a(lyst):
    b(lyst[2:5])
def b(lyst):
    for i in range(len(lyst)):
        lyst[i]*=2
c=[1,3,5,7,9,18,36]
a(c)
print(c)