BACKGROUND: This project is a bottle.py app. It is a simple Enigma Machine emulator, demonstrating basic Object Oriented Design principles in python and Database Management using sqlLite. The Enigma machines were used by the Germans to encrypt military messages in World War II with great success. This form of encryption utilized cutting edge technology to hide messages in plain site. Each machine consisted of a typewriter and a backlit text display. Within the machine was a collection of rotors that rotated each time a letter was entered. This changed the means of encryption every time. 

DESCRIPTION: This site allows a user to create an Enigma machine with any number of rotors(more rotors decreases the probability of codebreaking via brute force). Once a machine has been stored in the database, the user may use it to encrypt messages. In order to decrypt a message, you must have the setting number that it was encrypted with. For instance, the machine Mach1 has 65 rotors. The word "hello" encrypts to "wtpbo" using setting 45. To encrypt, we must know the setting to use is 45, and then enter "wtpbo", generating "hello" as output. Any other setting fails to decrypt the initial message.

Look here to see a demonstration: 

Running the program: Download the repository and run "python3 app.py" from the command line. The project will then be hosted at http://localhost:8080/.
