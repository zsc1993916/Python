# output
print ("hello python")

# input
#name = raw_input()
# print ("name ="),(name)


word="abcdefg"
a=word[2]
print "a is: "+a
b=word[1:3]
print "b is: "+b # index 1 and 2 elements of word.
c=word[:2]
print "c is: "+c # index 0 and 1 elements of word.
d=word[0:]
print "d is: "+d # All elements of word.
e=word[:2]+word[2:]
print "e is: "+e # All elements of word.
f=word[-1]
print "f is: "+f # The last elements of word.
g=word[-4:-2]
print "g is: "+g # index 3 and 4 elements of word.
h=word[-2:]
print "h is: "+h # The last two elements.
i=word[:-2]
print "i is: "+i # Everything except the last two characters
l=len(word)
print "Length of word is: "+ str(l)


Word=['a','b','c','d','e','f','g']
print (Word)
Word.append('hehe')
print (Word)

for x in Word:
    print x, len(x)

def sum(a, b):
    return a + b

func = sum
res = func(1, 2)
print ("function sum return:"),(res)

# The range() function
ranA =range(5,10)
print ranA
ranA = range(-2,-7)
print ranA
ranA = range(-7,-2)
print ranA
ranA = range(-2,-11,-3) # The 3rd parameter stands for step
print ranA



spath="D:\python\in.txt"
f=open(spath,"w") # Opens file for writing.Creates this file doesn't exist.
f.write("First line 1.\n")
f.writelines("First line 2.")
f.close()

f=open(spath,"r") # Opens file for reading

for line in f:
    print line
f.close()


s=raw_input("Input your age:")
if s =="":
    raise Exception("Input must no be empty.")

try:
    i=int(s)
except ValueError:
    print "Could not convert data to an integer."
except:
    print "Unknown exception!"
else: # It is useful for code that must be executed if the try clause does not raise an exception
    print "You are %d" % i," years old"
finally: # Clean up action
    print "Goodbye!"


class Base:
    def __init__(self):
        self.data = []
    def add(self, x):
        self.data.append(x)
    def addtwice(self, x):
        self.add(x)
        self.add(x)

# Child extends Base
class Child(Base):
    def plus(self,a,b):
        return a+b

oChild =Child()
oChild.add("str1")
print oChild.data
print oChild.plus(2,3)

raw_input("Press enter key to close this window")
