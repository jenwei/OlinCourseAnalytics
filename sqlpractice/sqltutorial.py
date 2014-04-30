# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 13:46:31 2014

@author: ldavis
"""

#obviously, to use sql, you need to install sqlite3 and then import it.
import sqlite3 as lite
#we're also going to need access to a few functions from the sys package;
#these functions interact unusually strongly with the interpreter.
import sys
 
def tutorial1():
    '''this sample code opens a database, reads its sqlite version, and then
    releases the database resources. if an error occurs, it raises an 
    exception.'''    
    #con is a variable that will be used to signify a connection to the db.
    #initially, it is set to none. if the connection cannot be established,
    #con's value (None) will cause an error in the finally clause.
    con = None
    #if you haven't used try/except before, it's mostly just a nice way of
    #raising predictable and helpful errors when your code breaks
    try:
        #the method lite.connect returns an object of class 'connection'
        con = lite.connect('test.db')
        #cur is the sqlite cursor object, which is what does stuff in the db
        cur = con.cursor()
        cur.execute('SELECT SQLITE_VERSION()')
        #fetchone retrives one data point. later, we will need to get more
        data = cur.fetchone()    
        print "SQLite version: %s" % data    
    except lite.Error, e:    
        print "Error %s:" % e.args[0]
        sys.exit(1)    
    finally:
        #this is where the aforementioned error will occur.
        if con:
            con.close()
            
def tutorial2():
    '''this does the same thing as the above function, but in less space'''    
    con = lite.connect('test.db')    
    #use of the with operator automatically provides exception handling
    #and releases resources at the end, making code more compact
    with con:    
        cur = con.cursor()    
        cur.execute('SELECT SQLITE_VERSION()')    
        data = cur.fetchone()    
        print "SQLite version: %s" % data  
        
def tutorial3():
    '''this inserts some values into our test database.'''
    con = lite.connect('test.db')
    #with also automatically commits changes. if you don't use with, you'll
    #have to do that shit manually. so use with
    with con:
        cur = con.cursor()    
        #turns out that's what sql code looks like. pretty freaky
        #anyways, this creates a table in the database with some headers...
        cur.execute("CREATE TABLE Cars(Id INT, Name TEXT, Price INT)")
        #...and inserts a bunch of values into it.
        cur.execute("INSERT INTO Cars VALUES(1,'Audi',52642)")
        cur.execute("INSERT INTO Cars VALUES(2,'Mercedes',57127)")
        cur.execute("INSERT INTO Cars VALUES(3,'Skoda',9000)")
        cur.execute("INSERT INTO Cars VALUES(4,'Volvo',29000)")
        cur.execute("INSERT INTO Cars VALUES(5,'Bentley',350000)")
        cur.execute("INSERT INTO Cars VALUES(6,'Citroen',21000)")
        cur.execute("INSERT INTO Cars VALUES(7,'Hummer',41400)")
        #this is a pretty dumb way of inserting data points.
        #it should probably be a little bit more automated...
        #oh hey what's that function right down there below this
        cur.execute("INSERT INTO Cars VALUES(8,'Volkswagen',21600)")
        
def tutorial4():
    '''this is a more automated version of tutorial3.'''
    #the data is stored as a tuple of tuples. this is necessary for later
    cars = (
    (1, 'Audi', 52642),
    (2, 'Mercedes', 57127),
    (3, 'Skoda', 9000),
    (4, 'Volvo', 29000),
    (5, 'Bentley', 350000),
    (6, 'Hummer', 41400),
    (7, 'Volkswagen', 21600)
    )
    con = lite.connect('test.db')
    with con:
        cur = con.cursor()    
        #if there's already a table called cars, shit could get fucked.
        #this line of sql code checks to see if there's already a table,
        #and if there is one, deletes it.
        cur.execute("DROP TABLE IF EXISTS Cars")
        cur.execute("CREATE TABLE Cars(Id INT, Name TEXT, Price INT)")
        #executemany takes a tuple of tuples as its second argument, which
        #is why the data points were saved like that up above. 
        cur.executemany("INSERT INTO Cars VALUES(?, ?, ?)", cars)

def tutorial5():
    '''this version of tutorial3 inputs data with an actual sql script.'''
    con = None    
    #sadly, we must provide our own error handling for now.
    #ah... try/except/finally, my old friend. we meet again    
    try:
        con = lite.connect('test.db')
        cur = con.cursor()  
        #IT'S AN SQL SCRIPT AAAAAAAAH
        #actually this is shockingly easy to read; just look at tutorial3
        cur.executescript("""
        DROP TABLE IF EXISTS Cars;
        CREATE TABLE Cars(Id INT, Name TEXT, Price INT);
        INSERT INTO Cars VALUES(1,'Audi',52642);
        INSERT INTO Cars VALUES(2,'Mercedes',57127);
        INSERT INTO Cars VALUES(3,'Skoda',9000);
        INSERT INTO Cars VALUES(4,'Volvo',29000);
        INSERT INTO Cars VALUES(5,'Bentley',350000);
        INSERT INTO Cars VALUES(6,'Citroen',21000);
        INSERT INTO Cars VALUES(7,'Hummer',41400);
        INSERT INTO Cars VALUES(8,'Volkswagen',21600);
        """)
        #remember how we're not using with any more? 
        #yeah, it means we have to use the commit() method now
        con.commit()
    except lite.Error, e:
        #con.rollback is new. what it does is roll back changes to when the
        #connection was initially made.         
        if con:
            con.rollback()
        print "Error %s:" % e.args[0]
        sys.exit(1)
    finally:
        if con:
            con.close() 

def tutorial6():
    '''this function fills :memory: with a new table called friends. then
    it returns the id of the last row, i.e. the number of friends.'''
    #if you'd like to know what :memory: is, so the fuck would I. the
    #online tutorial is like super vauge
    con = lite.connect(':memory:')
    #this is just what we did before...
    with con:
        cur = con.cursor()    
        #in sqlite, INTEGER PRIMARY KEY autoincrements
        cur.execute("CREATE TABLE Friends(id INTEGER PRIMARY KEY, Name TEXT);")
        cur.execute("INSERT INTO Friends(Name) VALUES ('Tom');")
        cur.execute("INSERT INTO Friends(Name) VALUES ('Rebecca');")
        cur.execute("INSERT INTO Friends(Name) VALUES ('Jim');")
        cur.execute("INSERT INTO Friends(Name) VALUES ('Robert');")
        #but it spits out the id of the last row. could be useful for 
        #validating database-filling when you have to iterate many times
        lid = cur.lastrowid
        print "The id of the last inserted row is %d" % lid
        
def tutorial7():
    '''this function reads all data from a database file.'''
    con = lite.connect('test.db')
    with con:    
        cur = con.cursor()    
        cur.execute("SELECT * FROM Cars")
        #remember fetchone() from tutorial1()? fetchall() is like fetchone(),
        #except instead of fetching one it fetches all.
        rows = cur.fetchall()
        #fetchall() returns a list of tuples, not a tuple of tuples. odd
        for row in rows:
            print row

def tutorial8():
    '''this function reads some data from a database file.'''
    con = lite.connect('test.db')
    with con:
        cur = con.cursor()    
        cur.execute("SELECT * FROM Cars")
        #sometimes the db is huge and fetchall() is silly. for those times,
        #we can choose to iterate fetchone().        
        while True:
            row = cur.fetchone()
            #this is an unusual way to loop, but I guess it's necessary
            #seeing as we're ripping the data one row at a time
            if row == None:
                break
            #fetchone() returns a tuple
            print row[0], row[1], row[2]
            
def tutorial9():
    '''this is a version of tutorial8 that uses an sql dictionary cursor.'''
    con = lite.connect('test.db')
    with con:
        #this line of code establishes that we're using a dictionary cursor.
        #a dictionary cursor means that fetch functions let us access values
        #by their column names rather than just indices.
        con.row_factory = lite.Row
        cur = con.cursor() 
        cur.execute("SELECT * FROM Cars")
        rows = cur.fetchall()
        #otherwise, this is just the same exact thing as before.
        for row in rows:
            print "%s %s %s" % (row["Id"], row["Name"], row["Price"])
    
def tutorial10():
    '''this function introduces parameterized queries, which make mass
    modification of objects in the database easy'''
    uId = 1
    uPrice = 62100 
    con = lite.connect('test.db')
    with con:
        cur = con.cursor()
        #this is how you format inputting variables to sql code.
        cur.execute("UPDATE Cars SET Price=? WHERE Id=?", (uPrice, uId))  
        #the online tutorial has the commit statement below, but I'm pretty
        #sure that the with is handling the commit and removing it seems to
        #have no effect, so for now I've commented it.
        #con.commit()
        #cur.rowcount is new. it returns the number of updated rows.
        print "Number of rows updated: %d" % cur.rowcount
        
def tutorial11():
    '''this prints the name and price of a car using named placeholders.'''    
    uId = 4
    con = lite.connect('test.db')
    with con:
        cur = con.cursor()    
        #named placeholders have a colon in front of them. the second input
        #to the execute method must be a dictionary defining them
        cur.execute("SELECT Name, Price FROM Cars WHERE Id=:Id", 
            {"Id": uId})        
        #again, dunno why this commit is here. not even changing anything
        #con.commit()
        row = cur.fetchone()
        print row[0], row[1]

#next in the tutorial there's a bit about handling images in databases. that
#is a) an idea of questionable merit and b) not relevant to the task at hand,
#so I'm just gonna go ahead and skip to the section on metadata. 

def tutorial12():
    '''this uses the PRAGMA command to return some metadata, or information
    about the data in the database'''
    con = lite.connect('test.db')
    with con:
        cur = con.cursor()    
        #PRAGMA is the metadata-returning command
        #table_info() gives the column IDs, names, and types
        cur.execute('PRAGMA table_info(Cars)')
        data = cur.fetchall()
        for d in data:
            print d[0], d[1], d[2]

def tutorial13():
    '''this function prints out the data with column names above it'''
    con = lite.connect('test.db')
    with con:
        cur = con.cursor()    
        cur.execute('SELECT * FROM Cars')
        #get the names of each column. description is a cursor property
        col_names = [cn[0] for cn in cur.description]
        rows = cur.fetchall()
        #print the fetched column names
        print "%s %-10s %s" % (col_names[0], col_names[1], col_names[2])
        for row in rows:    
            print "%2s %-10s %s" % row
            
def tutorial14():
    '''this lists all of the tables in the database'''
    con = lite.connect('test.db')
    with con:
        cur = con.cursor()
        #sqlite_master is evidently the 'root' directory of sqlite
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        rows = cur.fetchall()
        for row in rows:
            print row[0]

def writeData(data):
    '''this function is attached to tutorial15'''
    f = open('cars.sql', 'w')
    with f:
        f.write(data)

def tutorial15():
    '''this creates a backup of a database by dumping to a .sql file.'''
    cars = (
    (1, 'Audi', 52643),
    (2, 'Mercedes', 57642),
    (3, 'Skoda', 9000),
    (4, 'Volvo', 29000),
    (5, 'Bentley', 350000),
    (6, 'Hummer', 41400),
    (7, 'Volkswagen', 21600)
    )
    con = lite.connect(':memory:')
    with con:
        cur = con.cursor()
        #delete any existing cars table, then recreate it from the tuples
        cur.execute("DROP TABLE IF EXISTS Cars")
        cur.execute("CREATE TABLE Cars(Id INT, Name TEXT, Price INT)")
        cur.executemany("INSERT INTO Cars VALUES(?, ?, ?)", cars)
        #delete all of the cars with low prices
        cur.execute("DELETE FROM Cars WHERE Price < 30000")
        #con.iterdump returns an iterator to dump the database in sql format.
        #join() takes the iterator and the indicated line break character
        #and joins all the iterator strings, separating with newlines.
        data = '\n'.join(con.iterdump())
        #writeData() is the function up above.
        writeData(data)
        #in a terminal window, run 'cat cars.sql' to see what the backup
        #looks like.
        
def readData():
    '''just as tutorial15 needed writeData, tutorial16 needs readData'''
    f = open('cars.sql', 'r')
    with f:
        data = f.read()
        return data
    
def tutorial16():
    '''this function is the opposite of tutorial15; it reads a .sql file.'''
    #oh shit we're in the memory again    
    con = lite.connect(':memory:')
    with con:   
        cur = con.cursor()
        sql = readData()
        #read the data with the cursor and the function up above
        cur.executescript(sql)
        cur.execute("SELECT * FROM Cars")
        rows = cur.fetchall()
        for row in rows:
            print row  
            
def tutorial17():
    '''now we're getting to the good stuff. this function deals with 
    transactions, the core unit of database operations in sql'''
    #in sqlite, any command not named SELECT will begin an implicit
    #transaction. within a transaction, most other commands autocommit
    #recent changes before executing.
    try:
        con = lite.connect('test.db')
        cur = con.cursor()    
        cur.execute("DROP TABLE IF EXISTS Friends")
        cur.execute("CREATE TABLE Friends(Id INTEGER PRIMARY KEY, Name TEXT)")
        cur.execute("INSERT INTO Friends(Name) VALUES ('Tom')")
        cur.execute("INSERT INTO Friends(Name) VALUES ('Rebecca')")
        cur.execute("INSERT INTO Friends(Name) VALUES ('Jim')")
        cur.execute("INSERT INTO Friends(Name) VALUES ('Robert')")
        #we aren't using with here, so changes don't autocommit. we can
        #create this whole darn table, but if it doesn't commit at the
        #end the transaction won't do anything.
        #con.commit()
    except lite.Error, e:    
        if con:
            con.rollback()
            print "Error %s:" % e.args[0]
            sys.exit(1)
    finally:    
        if con:
            con.close() 

def tutorial18():
    '''this function is like tutorial17, but with commitment'''
    try:
        con = lite.connect('test.db')
        cur = con.cursor()    
        cur.execute("DROP TABLE IF EXISTS Friends")
        cur.execute("CREATE TABLE Friends(Id INTEGER PRIMARY KEY, Name TEXT)")
        cur.execute("INSERT INTO Friends(Name) VALUES ('Tom')")
        cur.execute("INSERT INTO Friends(Name) VALUES ('Rebecca')")
        cur.execute("INSERT INTO Friends(Name) VALUES ('Jim')")
        cur.execute("INSERT INTO Friends(Name) VALUES ('Robert')")
        #this is the key line. remember how within a transaction, CREATE
        #TABLE will autocommit previous changes? yep        
        cur.execute("CREATE TABLE IF NOT EXISTS Temporary(Id INT)")
    except lite.Error, e:
        if con:
            con.rollback()
            print "Error %s:" % e.args[0]
            sys.exit(1)    
    finally:
        if con:
            con.close()
            
def tutorial19():
    '''this function introduces autocommitment'''
    try:
        #setting isolation_level to "None" will start autocommit mode
        con = lite.connect('test.db', isolation_level=None)
        cur = con.cursor()    
        cur.execute("DROP TABLE IF EXISTS Friends")
        cur.execute("CREATE TABLE Friends(Id INTEGER PRIMARY KEY, Name TEXT)")
        cur.execute("INSERT INTO Friends(Name) VALUES ('Tom')")
        cur.execute("INSERT INTO Friends(Name) VALUES ('Rebecca')")
        cur.execute("INSERT INTO Friends(Name) VALUES ('Jim')")
        cur.execute("INSERT INTO Friends(Name) VALUES ('Robert')")
    except lite.Error, e:    
        print "Error %s:" % e.args[0]
        sys.exit(1)
    finally:    
        if con:
            con.close()

#...and we're done! hopefully this is helpful to you.