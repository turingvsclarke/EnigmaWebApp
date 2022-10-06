import random
import pdb

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# We are going to have a class that describes the current overall state of the Enigma machine and its size. This number will determine the states 
# of the individual rotors, so we are going to define a rotors attribute that will be a list of rotors.
class Enigma():

    def __init__ (self,state = 0, size = 0, rotors = [],reflector = ""):
        object.__init__(self)
        self.setState(state)
        self.setSize(size)
        self.setrotors(rotors)
        self.setReflector(reflector)

    def setState(self,state):
        self._state = state
    def getState(self):
        return self._state
    def setrotors(self,rotors):
        self._rotors = rotors
    def getrotors(self):
        return self._rotors
    def setSize(self,size):
        self._size = size
    def getSize(self):
        return self._size
    def setReflector(self,reflector):
        self._reflector = reflector.upper()
    def getReflector(self):
        return self._reflector
    # This is a huge problem. Currently, we are creating new rotors each time we try to get the rotors of the Enigma.
    # We need to instead pass the list of rotor objects to the Enigma as an attribute.
    # We send it a string of strings as an attribute and it populates its Rotors objects to have all these strings
    # as their individual values.

    def getRotors(self):

        Rotors = []
        for x in range(len(self.getrotors())):
            Rotors.append(Rotor(x,self.getrotors()[x]))

        return Rotors

    # Since our rotor state depends upon the Enigma state, we update the rotors of the Enigma through the Enigma class, using a getState method in the
    # Rotor object
    def updateRotors(self):
        #pdb.set_trace()
        for i in range(self.getSize()):
            # For the ith rotor we update the state
            self.getRotors()[i].getState(self.getState())
        
    # A rotation (really of the first rotor but amounts to the same thing) is really just an addition to the overall Enigma state
    def Rotate(self,rotations):

        self.setState(self.getState()+rotations)

    def getRotorKey(self,rotor_number):

        key = self.getRotors()[rotor_number].getKey(self.getState())
        return key
          
class Rotor():
    # This is my class of rotor objects. It has three attributes: state, position, and rotor (the string of letters defining it)
    # Let's initialize the object. Note that its not passed a state because it doesn't really have its own state. Its state is dependent upon 
    # the state of the Enigma
    def __init__ (self,position = 0,rotor = ""):
            object.__init__(self)
            self.setPosition(position)
            self.setrotor(rotor)

    # Each state is determined by the overall state of the Enigma and its position. Each state is whole divisor of the Enigma state when divided by 26^position
    def getState(self,state):
        return ((state%(26**(self.getPosition()+1)))//(26**self.getPosition()))

    def setPosition(self, position):
        self._position = position

    def getPosition(self):
        return self._position

    def setrotor(self,rotor):
        self._rotor = rotor.upper()

    def getrotor(self):
        return self._rotor

    def getKey(self,state):

        # We chop off the first state letters (1st state=only one letter) and put it at the front of the string
        return self.getrotor()[(26-state):26] + self.getrotor()[0:(26-state)]
          
    # Each rotor is going to be used as a key, which is determined by its rotor string and its state.
      
# For each rotor, we need to have a state. These states will change each time we call the rotateRotor method. The state will be a number from 0 through 25 indicating how many 
# letters the rotor has rotated through. The state at each point should be changed from x to (x+1)%26. 
# When a rotor's state reaches 0 (after rotation), it will switch the state of the rotor to the left (rotor r+1). This will continue for however many rotors we have.
# Each rotor will also need to have a position attribute, 0 through n. This should be immutable.
# Take input from the user

def createRotor():

    # Take each letter in the alphabet and randomly generate a new collection of these letters. This collection will be an iterable string.
    newrotor = ""
    global alphabet

    # Store the alphabet string locally so that we don't destroy the global variable for future use
    # alphabet1 = alphabet

    for i in range(26):

        index = random.randint(0,25)
        letter = alphabet[index]

        # Make sure that the letter isn't already in the rotor string
        while letter in newrotor:
            letter = alphabet[random.randint(0,25)]
        newrotor = newrotor + letter
    
    return newrotor

def createReflector():

    global alphabet

    # Create a reflector by picking a random string of paired letters (ath letter is b and bth letter is a for example)
    # Initiate a 26 character string
    Reflector = "0"*26

    # Take each letter from the alphabet and stick it in a random place. Aka lets say 'a' goes to the kth spot. Then
    # find a's place in the alphabet and put 
    for x in alphabet:
        if x not in Reflector:
            index = random.randint(0,25)
            # Make sure there is no other letter already there
            while Reflector[index] != "0":
                index = random.randint(0,25)
            Reflector = Reflector[0:index] + x + Reflector[(index+1):26]
            index2 = alphabet.index(x)
            Reflector = Reflector[0:index2] + alphabet[index] + Reflector[(index2+1):26]

    return Reflector

def encrypt(message,enigma):
    # Initialize an empty string that will eventually hold the fully encrypted text
    encryption = ""
    global alphabet
    message = message.upper()

    # If the value isn't in the alphabet, don't encrypt it
    # Iterate through each message, encrypting one letter at a time
    for x in range(len(message)):

        letter = message[x]
        # For each letter, we loop through the cryptography encryption function r times, r being the number of rotors, passing it the current
        # rotor key and the new encryption message, which switches each time. At the end of the for loop we should have the correct letter
        
        if letter in alphabet:
            rotors = enigma.getRotors()
            #pdb.set_trace()
            for y in range(len(enigma.getRotors())):
                # Find the letter's place in the alphabet
                index = alphabet.index(letter)
                # Assign the letter to the value of the xth rotor key at that index and then start over. Each time its then encrypting an encryption
                key = enigma.getRotorKey(y)
                letter = key[index]

            # Match to the correct letter via the reflector
            index = alphabet.index(letter)
            letter = enigma.getReflector()[index]

            # We now go backwards, finding which original letter would have given us the letter that pairs with the letter we actually got out of the reflector
            while y>=0:
                key=enigma.getRotorKey(y)
                index = key.index(letter)
                letter = alphabet[index]
                y-=1
            encryption = encryption + letter

            # Rotate the Enigma after each letter has been translated
            enigma.Rotate(1)
            enigma.updateRotors()

    return encryption

def main():

    keepgoing = True
    # We are going to want to intialize the rotors only once so that they stay with the Enigma the whole time.
    # To do this, we need to know if the user wants to use a previous rotor string or create his own
    # Create an Enigma object each time the program runs, not each time it loops. 
    # Each Enigma machine has a random reflector built in that can't be moved.
    numberofRotors = int(input("Number of Rotors: "))
    rotor_decision = input("Do you have a list of rotor strings?(y/n)\n")
    
    Rotors = []

    if rotor_decision == "y":

        for i in range(numberofRotors):
            Rotors.append(input("Next rotor string:"))

    else:
        
        for i in range(numberofRotors):
            # We are generating a list of rotor strings since the user didn't pass us such a list
            rotor = createRotor()
            Rotors.append(rotor)

    enigma = Enigma(0,numberofRotors,Rotors,createReflector())
    while keepgoing:

        user_choice = input("Do you want to 1. Encrypt 2. Quit 3. Change the rotor states 4. Display Enigma state\n")

        if user_choice == "1":

            message = input("Plaintext: ")

            # Create however many rotors the user wanted 
            # encrypt the message

            encryption = encrypt(message,enigma)
            print(encryption)

        elif user_choice == "2":

            keepgoing = False

        elif user_choice == "3":

            rotor_position = int(input("State:\n"))
            enigma.setState(rotor_position)

        elif user_choice == "4":
            print(enigma.getState())

        else:

            print("Please try again")

# create as many rotors as we need
# We need to be able to initiate an object for each of these rotors. That's tough.

# Assuming we have all these rotors, we now look at rotor number 26 at the
 
if __name__=="__main__":

    main()
