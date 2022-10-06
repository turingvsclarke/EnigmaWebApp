from bottle import route, run, template, request, post, get, error

# Set up our database connection
import sqlite3

# We are going to create three tables. One of them stores the Enigma name and its id, one stores the rotors and their ids, the last one bridges between them
enigmaDB = sqlite3.connect("enigmas.db")

# This sets the cursur so that it will select individual items within a row
enigmaDB.row_factory = sqlite3.Row
c = enigmaDB.cursor()
'''c.execute("DROP TABLE IF EXISTS enigmas")
c.execute("DROP TABLE IF EXISTS rotors")
c.execute("DROP TABLE IF EXISTS enigma_rotors")'''

# Create a rotor and enigma table

c.execute("""CREATE TABLE IF NOT EXISTS enigmas (id integer PRIMARY KEY, name text NOT NULL, reflector text NOT NULL)""")
c.execute("""CREATE TABLE IF NOT EXISTS rotors (id integer PRIMARY KEY, value text NOT NULL)""")
c.execute("""CREATE TABLE IF NOT EXISTS enigma_rotors (id integer PRIMARY KEY, enigma_id integer,
 rotor_id integer, FOREIGN KEY (enigma_id) REFERENCES enigmas (id), FOREIGN KEY (rotor_id) REFERENCES rotors (id))""")

enigmaDB.commit()

@get('/')
def EnigmaMenu():
    return template('Menu.html')

# This page will take us to a page that will get input from the user for encrypting the message.
@get('/Encryption')
def Encryption():
    return template('Encryption.html',c=c,engimaDB=enigmaDB)

# This page will display the results of the Enigma machine decryption. It is being passed data so needs a @post method
@post('/EncryptionResult')
def EncryptionResult():
    return template('EncryptionResult.html',c=c,enigmaDB = enigmaDB)

# At the end we want to have a login page, so the table page will be dependent upon that page. Eventually, the route will depen
@get('/MachineTable')
def EnigmaTable():
    return template('MachineTable.html',c=c,enigmaDB=enigmaDB)

@post('/RotorTable')
def RotorTable():
    return template('RotorTable.html',c=c,enigmaDB=enigmaDB)

@get('/addMachine')
def Addmachine():
    return template('addMachine.html')

@post('/addingMachine')
def AddingMachine():
    return template('addingMachine.html', c = c, enigmaDB = enigmaDB)

@get('/DeleteMachine')
def deleteMachine():
    return template('DeleteMachine.html',c=c,enigmaDB=enigmaDB)

@post('/DeletingMachine')
def deletingMachine():
    return template("DeletingMachine.html",c=c,enigmaDB=enigmaDB)

run(host='localhost',port = 8080,debug = True, reloader = True)
