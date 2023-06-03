import sleeperreqs as reqs
import json
import sqlite3
#import traceback

# Test Variables

username = 'ilikeikers'
userid = '571487366985555968'
league = '786647570763137024' # 2022 Superflex Dynasty
league2 = '784553434551558144' # 2022 10 Man (Rocky Mountain High)
league3 = '864592401434628096' # 2022 10 Man Superflex Redraft League
draft = '786647570763137025' # 2022 Superflex Dynasty Draft
trend = 'add' # could also be 'drop'
#trend = 'drop' # could also be 'add'
season = 2022 # 2020-2023 is range for this user
week = 2
dbfile = 'test.db'
table = 'personalUserInfo'

# Creates the strings needed for queries from the dictionary. Also returns a list of the columns to cycle through in other functions.
def getDictStrings(data=dict):
    colsstring = ""
    valsstring = ""
    colslist = []
    count = 0
    for col in data.keys():
        # Don't want the ',' in the first one. There has to be a better way though.
        if count == 0:
            colsadd = str(col)
            valsadd = ":" + str(col)
        else:
            colsadd = ", " + str(col)
            valsadd = ", :" + str(col)
        colslist.append(col)
        colsstring = colsstring + colsadd
        valsstring = valsstring + valsadd
        count += 1

    return colsstring, valsstring, colslist

# Checks if there are any dict or lists for the values. Returns list of them or
def checkForDicts(data=dict):
    # Runs through the dictionary to see if any of the values contain a dictionary or a list. returnbit returns 'True' if so.
    tempbit = False
    returnbit = True
    dictlist = []
    listlist = []
    goodlist = []
    for key in data.keys():
        if type(data.get(key)) == dict:
            tempbit = False
            dictlist.append(key)
        if type(data.get(key)) == list:
            tempbit = False
            listlist.append(key)
        else:
            tempbit = True
            goodlist.append(key)
        returnbit = returnbit and tempbit

    return returnbit, dictlist, listlist, goodlist

# Drop a given table
def tableDrop(table=str, dbfile=str):
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    query = "DROP TABLE IF EXISTS {0}".format(table)
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

    return

# Create a given table. Will overwrite if table already exists.
def tableCreate(table=str, dbfile=str, data=dict):
    # Drops the table first if it exists.
    tableDrop(table, dbfile)
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    # Data comes in as a dict. This function returns a string of the dict keys to use for the query.
    colsstring, *_ = getDictStrings(data)
    createquery = "CREATE TABLE {0} ({1})".format(table, colsstring)
    cur.execute(createquery)
    conn.commit()
    cur.close()
    conn.close()
    #insertquery = "INSERT INTO {0} ({1}) VALUES ({2})".format(table, str(colsstring), str(valsstring))

    return

# Insert data into a given table. Returns the rowid of the insert for use as key if called by a different table
def tableInsert(table=str, dbfile=str, data=dict):
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    colsstring, valsstring, _ = getDictStrings(data)
    createquery = "CREATE TABLE IF NOT EXISTS {0} ({1})".format(table, colsstring)
    insertquery = "INSERT INTO {0} ({1}) VALUES ({2})".format(table, colsstring, valsstring)
    cur.execute(createquery)
    cur.execute(insertquery, data)
    rowid = cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()

    return rowid

# Adds columns to a given table.
def addColumns(table=str, dbfile=str, data=dict, vartype="TEXT", default=""):
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    colsstring, _ , collist = getDictStrings(data)
    createquery = "CREATE TABLE IF NOT EXISTS {0} ({1})".format(table, colsstring)
    cur.execute(createquery)
    for col in collist:
        try:
            alterquery = "ALTER TABLE {0} ADD COLUMN {1} text".format(table, str(col))
            cur.execute(alterquery)
            conn.commit()
        except:
            pass
    conn.commit()
    cur.close()
    conn.close()

    return

# Adds a dictionary to a table.
def addRow(newtable=str, dbfile=str, data=dict):
    addColumns(newtable, dbfile, data)
    newvalue = tableInsert(newtable, dbfile, data)

    return newvalue

# Adds a dictionary to a table. Adds the rowid to initial table dict and returns it
def addEmbedRow(initialtable, initialtableid=str, dbfile=str, data=dict, newtable=str, linkkey=str):
    data[linkkey] = initialtableid
    newvalue = addRow(newtable, dbfile, data)
    del initialtable[newtable]
    initialtable[newtable] = newvalue

    return initialtable

# Create Embededed List Table
def createEmbedDictTable(initialtable, initialtableid=str, dbfile=str, dictlist=list, newtable=str, linkkey=str):
    for item in dictlist:
        title = str(item)
        newdict = initialtable.get(title)
        addEmbedItem(initialtable, initialtableid, dbfile, newdict, item, linkkey)

    return

# Builds the a dictionary given a list. Can assign a prefix for the columnname and a count setpoint. Returns the new dictionary
def buildListDict(listname=list, colname="pos", count=1):
    newdict = {}
    #count = 1
    for item in listname:
        key = colname + str(count)
        value = str(item)
        newdict[key] = value
        count += 1

    return newdict

# Create Embededed List Table
def createEmbedListTable(initialtable, initialtableid=str, dbfile=str, listlist=list, newtable=str, linkkey=str):
    for item in listlist:
        title = str(item)
        newlist = initialtable.get(title)
        newdict = buildListDict(newlist)
        addEmbedItem(initialtable, initialtableid, dbfile, newdict, item, linkkey)

    return

# Check and add embedded item
def addEmbedItem(initialtable, initialtableid=str, dbfile=str, data=dict, newtable=str, linkkey=str):
    testbit, dictlist, listlist, collist = checkForDicts(data)
    if dictlist:
        createEmbedDictTable(initialtable, initialtableid, dbfile, dictlist, newtable, linkkey)
    elif listlist:
        createEmbedListTable(initialtable, initialtableid, dbfile, listlist, newtable, linkkey)
    elif testbit:
        initialtable = addEmbedRow(initialtable, initialtableid, dbfile, data, newtable, linkkey)
    else:
        print("Error. No Embedded item to add.")

    return initialtable

# Check and add item
def addItem(initialtable, initialtableid=str, dbfile=str, data=dict, newtable=str, linkkey=str):
    # If testbit is True, then the item can be added without issue. When either list contains something, the addEmbedItem func is called to go a layer deeper. Then the new item is added with the tables linked.
    testbit, dictlist, listlist, _ = checkForDicts(data)
    if testbit:
        addRow(newtable, dbfile, data)
    elif listlist or dictlist:
        addEmbedItem(initialtable, initialtableid, dbfile, data, newtable, linkkey)
        addItem(initialtable, initialtableid, dbfile, data, newtable, linkkey)
    else:
        print("Error. No item to add.")

    return

# Create Raw Table
def createRawTable(tables, dbfile=str, primarytable=str):
    for table in tables:
        # Needed for the addItem func. The dict key for the initial table will be xxx_id. This allow the initial table id to be used to link the tables in the new table
        linkkey = str(primarytable) + '_id'
        initialtableid = table.get(linkkey)
        # SQLite3 doesn't seem to like long strings of ints in the tablename. The brackets allow them to be used
        tablename = '[' + str(initialtableid) + ']'
        addItem(table, initialtableid, dbfile, table, tablename, linkkey)

    return

# Creates the Raw User Info Table
def createRawUserInfoTable(userid=str, tabletitle=str(userid), dbfile=str):
    # The userid is a string of numbers. SQLite3 throws an error if that title isn't in brackets.
    modifiedtitle = '[' + tabletitle + ']'
    # Calls the Sleeper API to get the user info. Then parses the json response into a dictionary
    response = reqs.getUserInfo(userid)
    userdict = response.json()
    # Creates and closes SQLite3 connections in order to make and create a table with all user info from the Sleeper API
    tableCreate(modifiedtitle, dbfile, userdict)
    tableInsert(modifiedtitle, dbfile, userdict)

    return

# Create Raw User Leagues Table. primary table = 'user', 'league', 'draft'
def createRawUserLeaguesTable(userid=str, dbfile=str, sport='nfl', season='2023'):
    # Calls the Sleeper API. Parses the resones and creates the raw league table
    response = reqs.getUserLeagues(userid, season, sport)
    tables = response.json()
    # Need for a use with Sleeper. This is used in the createRawTable function to call addItem func
    primarytable = 'league'
    createRawTable(tables, dbfile, primarytable)

    return

# Create Raw League Users Table. primary table = 'user', 'league', 'draft'
def createRawLeagueUsersTable(leagueid=str, dbfile=str, sport='nfl', season='2023'):
    # Calls the Sleeper API. Parses the resones and creates the raw league table
    response = reqs.getLeagueUsers(leagueid, season, sport)
    tables = response.json()
    # Need for a use with Sleeper. This is used in the createRawTable function to call addItem func
    primarytable = 'user'
    createRawTable(tables, dbfile, primarytable)

    return

createRawUserInfoTable(userid, dbfile=dbfile)
createRawUserLeaguesTable(userid, season=season, dbfile=dbfile)
createRawUserLeaguesTable(league, season=season, dbfile=dbfile)

""" TEST CALLS """

# Responses
# GET User Leagues is pretty powerful
#response = reqs.getUserLeagues(userid, season)
#response2 = reqs.getDraftInfo(draft)
#response = reqs.getLeagueInfo(league)
#response2 = reqs.getLeagueInfo(league2)
#response3 = reqs.getLeagueInfo(league3)
#response4 = reqs.getUserInfo(userid)
#response5 = reqs.getUserInfo('richasian')
#userdata = response4.json()
#userdict2 = response5.json()
#print(userdata.keys())
#print(userdict2.keys())
#json = response.json()
#json2 = response2.json()
#json3 = response3.json()

#json = json.get('roster_positions')
#json2 = json2.get('roster_positions')
#json3 = json3.get('roster_positions')
#print(json3)
#print(json3)
#print(set(json.keys()) ^ set(json2.keys()))
#print(set(json.keys()) ^ set(json3.keys()))
#print(set(json2.keys()) ^ set(json3.keys()))
#print(json, json2, json3)
#print(set(json.keys()) ^ set(json2.keys()) ^ set(json3.keys()))
#json4 = response4.json()

# Practice Infoset primary
#tableCreate('tester3', dbfile, userdict)
#tableInsert('tester3', dbfile, userdict2)

""" Legacy. Keeping for backup for a few more runs """
"""
# Check that all keys exist in table as columns. Adds them if not
def checkColumns(table=str, dbfile=str, data=dict):
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    colsstring, valsstring, colslist = getDictStrings(data)
    print(colsstring)
    for col in colslist:
        print(col)
        #searchquery = "SELECT * AS CNTREC FROM pragma_table_info({0}) WHERE name={1}".format(table, col)
        searchquery = "SELECT INSTR(sql, {0}) FROM sqlite_master WHERE type='table' AND name={1}".format(col, table)
        #searchquery = "PRAGMA table_info ({0})".format(table)
        try:
            check = cur.execute(searchquery)
            print(check)
        except:
            print('Error')
        else:
            print('Success')
    table = '[' + str(table) + ']'
    createquery = "CREATE TABLE IF NOT EXISTS {0} ({1})".format(table, colsstring)
    insertquery = "INSERT INTO {0} ({1}) VALUES ({2})".format(table, str(colsstring), str(valsstring))
    #cur.execute(createquery)
    #cur.execute(insertquery, data)
    #conn.commit()
    cur.close()
    conn.close()

# Create Raw User Leagues Table
def createRawUserLeaguesTableOld(userid=str, sport='nfl', season='2023', table="", dbfile=str):
    table = str(userid) + str(sport) + str(season)
    response = reqs.getUserLeagues(userid, season, sport)
    leagues = response.json()
    for league in leagues:
        returnbit, dictlist, listlist, collist = checkForDicts(league)
        linkkey = 'league_id'
        leagueid = league.get(linkkey)
        tablename = '[' + str(leagueid) + ']'
        for table in dictlist:
            title = str(table)
            newdict = league.get(title)
            testbit, *_ = checkForDicts(newdict)
            if testbit:
                addEmbedRow(league, leagueid, dbfile, newdict, title, linkkey)
        for table in listlist:
            title = str(table)
            rosterlist = league.get(title)
            newdict = buildListDict(rosterlist)
            testbit, *_ = checkForDicts(newdict)
            if testbit:
                addEmbedRow(league, leagueid, dbfile, newdict, title, linkkey)
        testbit, *_ = checkForDicts(league)
        if testbit:
            addRow(tablename, dbfile, league)
"""
