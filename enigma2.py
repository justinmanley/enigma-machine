import string
from collections import deque

"""
This module defines Rotor and Enigma classes.
Useful attributes and methods for the Enigma class are:
Enigma.rotors
Enigma.reflector
Enigma.remember()
Enigma.reset()

Strings are encoded via the function encode(), which takes a string and an Enigma machine.  encode() calls map_char() which in turn calls map_char_once() and many of the methods of Rotor and Enigma.

"""


"""--Classes--------------------------------------------"""

class Rotor(object):                                  # Rotors are constructed from a list of tuples and a single integer representing
    def __init__(self,mapping,offset):                # the offset of the rotor.
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
    def rstep(self):                              # increase the phase between the two lists that make up the rotor by 1.
        xs,ys = zip(*self.mapping)                # useful for creating test rotors
        xs_d,ys_d = deque(xs),deque(ys) 
        a = ys_d.pop()
        ys_d.appendleft(a)
        return Rotor(zip(xs_d,ys_d),self.offset)

class Enigma(object):                               # An enigma machine is a list of rotors, with the last rotor being the reflector
    def __init__(self,rotors):                      # by convention.  The reflector can also be accessed via the reflector attribute.
        self.rotors = rotors                        # a list of Rotor objects
        self.reflector = rotors[-1]                 # a single Rotor object which is symmetrical - that is, if a -> b, then b -> a.
    def __str__(self):
        return "Rotors:\n%s\nReflector: %s" % (self.rotors[:-1],self.reflector) 
    def __repr__(self):
        return "Rotors:\n%s\nReflector: %s" % (self.rotors[:-1],self.reflector)
    def remember(self):             # store the state of the offsets so that the machine can be reset later
        offsets = []
        for rotor in self.rotors:
            offsets.append(rotor.offset)
        self.config = offsets        
    def step(self,i):       # steps the i^th rotor in the machine, indexed in the conventional way from 0 to n
        if self.rotors[i].offset==25:
            self.rotors[i].offset = 0
            self.step(i+1 % len(self.rotors))
        else:
            self.rotors[i].offset += 1
        return self
    def flip(self):                                 # returns a machine with the rotors flipped.  Reflector remains unmoved.
        backwards = []                              # Have to do this so that our machine is not modified in place.
        for element in self.rotors[:-1]:            # We want our machine to remain the same so that
            backwards.append(element)               # we can run encode() twice to return to the original string.
            backwards.reverse()
            backwards.append(self.reflector)
        return Enigma(backwards)
    def reset(self):                                # reset the offsets to their orientation the last time remember() was called.
        try:
            for i in range(len(self.rotors)):
                 self.rotors[i].offset = self.config[i]
        except AttributeError:
            print("You have to save the state of the Enigma machine before you can reset it.")

"""--Utilities--------------------------------------------"""

def map_char_once(c,rotor):              # map a character through a list of relationships among characters.  no offsets.
    for pair in rotor.mapping:
        x,y = pair
        if x == c:
            target = y
        else:
            pass
    return target

def chartonum(c):                                      # maps character to a number so that we can do arithmetic
    alphabet = [ a for a in string.ascii_lowercase ]       
    numbers = range(0,26)
    mapping = Rotor(zip(alphabet,numbers),0)
    return map_char_once(c,mapping)

def numtochar(n):                                      # maps number back to character once arithmetic is done.
    alphabet = [ a for a in string.ascii_lowercase ]       
    numbers = range(0,26)
    mapping = Rotor(zip(numbers,alphabet),0)
    return map_char_once(n,mapping)

"""--Functions---------------------------------------------"""

def map_char(c,machine):                    # map a character through the entire machine, taking the offsets into account.

    c = chartonum(c) # map the character to a number.  This is so we can do math with the offsets.

    for rotor in machine.rotors[:-1]:
        c = (c + rotor.offset) % 26
        c = map_char_once(c,rotor)
        c = (c - rotor.offset) % 26

    reflector = machine.reflector
    c = (c + reflector.offset) % 26
    c = map_char_once(c,reflector)
    c = (c - reflector.offset) % 26
                                     
    for rotor in machine.flip().rotors[:-1]:            # Flip the list of rotors around, so that we go back through the last rotor first.
        c = (c + rotor.offset) % 26
        c = map_char_once(c,rotor.rflip())  # Make sure each rotor itself is flipped before we map through it.
        c = (c - rotor.offset) % 26
    c = numtochar(c)    
    return c

def encode(x,machine):            # encode a string.
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

"""--Test----------------------------------------"""

def test(): 
    encode("hello",sample_machine)