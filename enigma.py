import string
from collections import deque

"""--Utilities--------------------------------------------"""

class Rotor(object):
    def __init__(self,mapping,offset):
        self.mapping = mapping
        self.offset = offset
    def __repr__(self):
        return "Rotor: %s\nOffset: %d\n" % (self.mapping, self.offset)
    def __str__(self):
        return "Rotor: %s\nOffset: %d\n" % (self.mapping, self.offset)
    def rflip(self):
        flipped = []                       # I do this so that I don't 
        for pair in self.mapping:
            x,y = pair
            flipped.append((y,x))
        return Rotor(flipped,self.offset)
    def rstep(self):
        xs,ys = zip(*self.mapping)
        xs_d,ys_d = deque(xs),deque(ys) 
        a = ys_d.pop()
        ys_d.appendleft(a)
        return Rotor(zip(xs_d,ys_d),self.offset)

class Enigma(object):
    def __init__(self,rotors):
        self.rotors = rotors         # a list of Rotor objects
        self.reflector = rotors[-1]   # a single Rotor object which is symmetrical - that is, if a -> b, then b -> a.
    def __str__(self):
        return "Rotors:\n%s\nReflector: %s" % (self.rotors[:-1],self.reflector) 
    def __repr__(self):
        return "Rotors:\n%s\nReflector: %s" % (self.rotors[:-1],self.reflector)
    def savestate(self):             # store the state of the offsets so that the machine can be reset later
        offsets = []
        for rotor in self.rotors:
            offsets.append(rotor.offset)
        self.config = offsets        
    def step(self,i):
        if self.rotors[i].offset==25:
            self.rotors[i].offset = 0
            self.step(i+1 % len(self.rotors))
        else:
            self.rotors[i].offset += 1
        return self
    def flip(self):
        backwards = []                              # Have to do this so that our machine is not modified in place.
        for element in self.rotors[:-1]:         # We want our machine to remain the same so that
            backwards.append(element)               # we can run encode() twice to return to the original string.
            backwards.reverse()
        return backwards
    def reset(self):
        try:
            for i in range(len(self.rotors)):
                 self.rotors[i].offset = self.config[i]
        except AttributeError:
            print("You have to save the state of the Enigma machine before you can reset it.")

"""  # Now included in the Rotor class.
def flip_rotor(rotor):
    flipped = []
    for pair in rotor:
        x,y = pair
        flipped.append((y,x))
    return flipped

def internal_step(rotor):
    xs,ys = zip(*rotor)
    xs_d,ys_d = deque(xs),deque(ys) 
    a = ys_d.pop()
    ys_d.appendleft(a)
    return zip(xs_d,ys_d)


def step(i,rotors):       # Now included in the Enigma class.
    if rotors[i][1]==25:
        rotors[i][1] = 0
        step(i+1 % (len(rotors)-1),rotors)
    else:
        rotors[i][1] += 1 """

def map_char_once(c,rotor):
    for pair in rotor.mapping:
        x,y = pair
        if x == c:
            target = y
        else:
            pass
    return target

def chartonum(c):
    alphabet = [ a for a in string.ascii_lowercase ]       
    numbers = range(0,26)
    mapping = Rotor(zip(alphabet,numbers),0)
    return map_char_once(c,mapping)

def numtochar(n):
    alphabet = [ a for a in string.ascii_lowercase ]       
    numbers = range(0,26)
    mapping = Rotor(zip(numbers,alphabet),0)
    return map_char_once(n,mapping)

"""--Functions---------------------------------------------"""

def map_char(c,machine):

    c = chartonum(c) # map the character to a number.  This is so we can do math with the offsets.

    for rotor in machine.rotors[:-1]:
        c = (c + rotor.offset) % 26
        c = map_char_once(c,rotor)
        c = (c - rotor.offset) % 26

    reflector = machine.reflector
    c = (c + reflector.offset) % 26
    c = map_char_once(c,reflector)
    c = (c - reflector.offset) % 26
                                     
    for rotor in machine.flip():            # Flip the list of rotors around, so that we go back through the last rotor first.
        c = (c + rotor.offset) % 26
        c = map_char_once(c,rotor.rflip())  # Make sure each rotor itself is flipped before we map through it.
        c = (c - rotor.offset) % 26
    c = numtochar(c)    
    return c

def encode(x,machine):
    encoded_list = []
    for character in x:
        encoded_list.append(map_char(character,machine))
        machine.step(0)
    return ''.join(encoded_list)

"""--Tests--------------------------------------------------"""

alphabet = [ a for a in string.ascii_lowercase ]
numbers = range(0,26)
rev_alphabet = [ a for a in string.ascii_lowercase ]
rev_alphabet.reverse()
rev_numbers = range(0,26)
rev_numbers.reverse()

sample_rotor1 = Rotor(zip(numbers,rev_numbers),0)
sample_rotor2 = Rotor(zip(numbers,numbers),0).rstep()
sample_rotor3 = sample_rotor1.rstep()

def make_sample_reflector():
    alphabet_pt1 = []
    alphabet_pt2 = []
    for i in numbers:
        if ( numbers.index(i) < 13 ):
            alphabet_pt1.append(i)
        else:
            pass
    for i in rev_numbers:
        if ( rev_numbers.index(i) < 13 ):
            alphabet_pt2.append(i)
        else:
            pass
    reflector = Rotor(zip(alphabet_pt1,alphabet_pt2),0).rstep()
    reflector.mapping.extend(reflector.rflip().mapping)
    return reflector

reflector = make_sample_reflector()

sample_machine = Enigma([sample_rotor1,sample_rotor2,sample_rotor3,reflector])

#"""    Test Output        """
#print(map_char_once('y',sample_rotor1))
#print(flip_rotor(sample_rotor1))
#rotors,reflectorp = sample_machine
#for rotor in rotors:
#    print("Begin rotor.")
#    for pair in rotor[0]:
#        print(pair)
#    print("End rotor")
#for pair in reflectorp[0]:
#    print(pair)
#print(map_char('y', sample_machine ))
#print(encode('omagnummysterium',sample_machine))
def test(): encode("hello",sample_machine)
