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
def getDictStrings(data_dict):
    keys_string = ""
    vals_string = ""
    keys_list = []
    count = 0
    for key in data_dict.keys():
        # Don't want the ',' in the first one. There has to be a better way though.
        if count == 0:
            keys_add = str(key)
            vals_add = ":" + str(key)
        else:
            keys_add = ", " + str(key)
            vals_add = ", :" + str(key)
        keys_list.append(key)
        keys_string = keys_string + keys_add
        vals_string = vals_string + vals_add
        count += 1

    return keys_string, vals_string, keys_list

# Checks if there are any dict or lists for the values. Returns list of them or
def checkForDicts(data_dict):
    # Runs through the dictionary to see if any of the values contain a dictionary or a list. returnbit returns 'True' if so.
    temp_bit = False
    return_bit = True
    dict_list = []
    list_list = []
    good_list = []
    for key in data_dict.keys():
        if type(data_dict.get(key)) == dict:
            temp_bit = False
            dict_list.append(key)
        if type(data_dict.get(key)) == list:
            temp_bit = False
            list_list.append(key)
        else:
            temp_bit = True
            good_list.append(key)
        return_bit = return_bit and temp_bit

    return return_bit, dict_list, list_list, good_list

# Drop a given table
def tableDrop(table_title, db_file):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    query_table_title = '[' + str(table_title) + ']'
    query = "DROP TABLE IF EXISTS {0}".format(query_table_title)
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

    return

# Create a given table. Will overwrite if table already exists.
def tableCreate(table_title, db_file, data_dict):
    # Drops the table first if it exists.
    tableDrop(table_title, db_file)
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    # Data comes in as a dict. This function returns a string of the dict keys to use for the query.
    columns, *_ = getDictStrings(data_dict)
    query_table_title = '[' + str(table_title) + ']'
    query = "CREATE TABLE {0} ({1})".format(query_table_title, columns)
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

    return

# Insert data into a given table. Returns the rowid of the insert for use as key if called by a different table
def tableInsert(table_title, db_file, data_dict):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    column_headers, cell_data, _ = getDictStrings(data_dict)
    query_table_title = '[' + str(table_title) + ']'
    create_query = "CREATE TABLE IF NOT EXISTS {0} ({1})".format(query_table_title, column_headers)
    insert_query = "INSERT INTO {0} ({1}) VALUES ({2})".format(query_table_title, column_headers, cell_data)
    cur.execute(create_query)
    cur.execute(insert_query, data_dict)
    row_id = cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()

    return row_id

# Adds columns to a given table.
def addColumns(table_title, db_file, data_dict):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    column_headers, _ , columns_list = getDictStrings(data_dict)
    query_table_title = '[' + str(table_title) + ']'
    create_query = "CREATE TABLE IF NOT EXISTS {0} ({1})".format(query_table_title, column_headers)
    cur.execute(create_query)
    conn.commit()
    for column in columns_list:
        try:
            alter_query = "ALTER TABLE {0} ADD COLUMN {1} text".format(query_table_title, str(column))
            cur.execute(alter_query)
            conn.commit()
        except:
            pass
    cur.close()
    conn.close()

    return

# Adds a dictionary to a table.
def addRow(table_title, db_file, data_dict):
    addColumns(table_title, db_file, data_dict)
    row_id = tableInsert(table_title, db_file, data_dict)

    return row_id

# Builds the a dictionary given a list. Can assign a prefix for the column name and a count setpoint. Returns the new dictionary
def buildListDict(data_list, column_title="pos", count=1):
    new_dict = {}
    for data in data_list:
        key = column_title + str(count)
        value = str(data)
        new_dict[key] = value
        count += 1

    return new_dict

# Create Embededed List Table
def createEmbedListTable(initial_table_dict, initial_table_title, db_file, lists_list, dict_linkkey):
    for list_title in lists_list:
        new_table_title = str(list_title)
        data_list = initial_table_dict.get(list_title)
        new_dict = buildListDict(data_list)
        addEmbedItem(initial_table_dict, initial_table_title, db_file, new_dict, new_table_title, dict_linkkey, new_table_title)

    return

# Create Embededed List Table
def createEmbedDictTable(initial_table_dict, initial_table_title, db_file, dicts_list, dict_linkkey):
    for dict_title in dicts_list:
        new_table_title = str(dict_title)
        #new_table_title = str(initial_table_title) + '_' + str(dict_title)
        new_dict = initial_table_dict.get(str(dict_title))
        addEmbedItem(initial_table_dict, initial_table_title, db_file, new_dict, new_table_title, dict_linkkey, dict_title)

    return

# Adds a dictionary to a table. Replaces the key value pair in the initial dictionary with the new row id
def addEmbedRow(initial_table_dict, initial_table_title, db_file, data_dict, new_table_title, dict_linkkey, dict_title):
    data_dict[dict_linkkey] = initial_table_title
    row_id = addRow(new_table_title, db_file, data_dict)
    del initial_table_dict[dict_title]
    initial_table_dict[dict_title] = row_id

    return initial_table_dict

# Check and add embedded item
def addEmbedItem(initial_table_dict, initial_table_title, db_file, data_dict, new_table_title, dict_linkkey, dict_title=''):
    updated_dict = {}
    test_bit, dicts_list, lists_list, _ = checkForDicts(data_dict)
    if dicts_list:
        createEmbedDictTable(initial_table_dict, initial_table_title, db_file, dicts_list, dict_linkkey)
    elif lists_list:
        createEmbedListTable(initial_table_dict, initial_table_title, db_file, lists_list, dict_linkkey)
    elif test_bit:
        updated_dict = addEmbedRow(initial_table_dict, initial_table_title, db_file, data_dict, new_table_title, dict_linkkey, dict_title)
    else:
        print("Error. No Embedded item to add.")

    return updated_dict

# Check and add item
def addItem(initial_table_dict, initial_table_title, db_file, data_dict, new_table_title, dict_linkkey):
    # If testbit is True, then the item can be added without issue. When either list contains something, the addEmbedItem func is called to go a layer deeper. Then the new item is added with the tables linked.
    test_bit, dicts_list, lists_list, _ = checkForDicts(data_dict)
    if test_bit:
        addRow(new_table_title, db_file, data_dict)
    elif lists_list or dicts_list:
        addEmbedItem(initial_table_dict, initial_table_title, db_file, data_dict, new_table_title, dict_linkkey)
        addItem(initial_table_dict, initial_table_title, db_file, data_dict, new_table_title, dict_linkkey)
    else:
        print("Error. No item to add.")

    return

# Create Raw Table. Primary table type should be user, league, player, draft, etc.
def createRawTable(tables_list, db_file, primary_table_type):
    for table_dict in tables_list:
        # Needed for the addItem func. The dict key for the initial table will be xxx_id. This allow the initial table id to be used to link the tables in the new table
        dict_linkkey = str(primary_table_type) + '_id'
        raw_table_title = table_dict.get(dict_linkkey)
        # SQLite3 doesn't seem to like long strings of ints in the tablename. The brackets allow them to be used
        modified_table_title = str(raw_table_title)
        addItem(table_dict, modified_table_title, db_file, table_dict, modified_table_title, dict_linkkey)

    return

# Creates the Raw User Info Table
def createRawUserInfoTable(user_id, db_file, table_title=str(userid)):
    # The userid is a string of numbers. SQLite3 throws an error if that title isn't in brackets.
    modified_title = str(table_title)
    # Calls the Sleeper API to get the user info. Then parses the json response into a dictionary
    response = reqs.getUserInfo(user_id)
    user_dict = response.json()
    # Creates and closes SQLite3 connections in order to make and create a table with all user info from the Sleeper API
    tableCreate(modified_title, db_file, user_dict)
    tableInsert(modified_title, db_file, user_dict)

    return

# Create Raw User Leagues Table. primary table = 'user', 'league', 'draft'
def createRawUserLeaguesTable(user_id, db_file, sport='nfl', season='2023'):
    # Calls the Sleeper API. Parses the resones and creates the raw league table
    response = reqs.getUserLeagues(userid, season, sport)
    tables = response.json()
    # Need for a use with Sleeper. This is used in the createRawTable function to call addItem func
    primary_table_type = 'league'
    createRawTable(tables, dbfile, primary_table_type)

    return

# Create Raw League Users Table. primary table = 'user', 'league', 'draft'
def createRawLeagueUsersTable(league_id, db_file, sport='nfl', season='2023'):
    # Calls the Sleeper API. Parses the resones and creates the raw league table
    response = reqs.getLeagueUsers(league_id, season, sport)
    tables = response.json()
    # Need for a use with Sleeper. This is used in the createRawTable function to call addItem func
    primary_table_type = 'user'
    createRawTable(tables, db_file, primary_table_type)

    return

createRawUserInfoTable(userid, db_file=dbfile)
#createRawUserLeaguesTable(userid, season=season, db_file=dbfile)
createRawUserLeaguesTable(league, season=season, db_file=dbfile)

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
