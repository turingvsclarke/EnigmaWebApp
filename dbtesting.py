import sqlite3
from Enigma import*
import pdb

# We're going to connect to the enigmas database and test some

enigmaDB = sqlite3.connect("enigmas.db")

# This sets the cursur so that it will select individual items within a row
enigmaDB.row_factory = sqlite3.Row
c = enigmaDB.cursor()

# Time to test checking if there is already a machine of a certain name in our database
def checkforname(name):
    copycat=False
    result = c.execute("SELECT * FROM enigmas WHERE name = ?",(name,))
    for x in result:
        copycat = True

    return copycat

copycat = checkforname("eggsalad")
print(copycat)