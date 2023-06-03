import requests


""" GET all players in a league.
USE SPARINGLY (once per day) to keep players updated.
Query is approx 5MB. """
def getAllPlayers(sport='nfl'):
    response = requests.get('https://api.sleeper.app/v1/players/' + sport)

    return response

# GET current state info for a given sport (default to NFL)
def getSportState(sport='nfl'):
    response = requests.get('https://api.sleeper.app/v1/state/' + sport)

    return response

# GET trending player list. Trend is either 'add' or 'drop'  Uses nfl default, as well as Sleeper defaults for loopback_hours and results limit (24 hours and 25 results, respectively)
def getTrendingPlayers(trend, sport='nfl', loopback_hours=24, limit=25):
    hours = str(loopback_hours)
    limit = str(limit)
    response = requests.get('https://api.sleeper.app/v1/players/' + sport + '/trending/' + trend + '?loopback_hours=' + hours + '&limit=' + limit)

    return response

# GET user info. Can be pulled with either a username or user_id
def getUserInfo(userid):
    response = requests.get('https://api.sleeper.app/v1/user/' + userid)

    return response

# GET full size avatar url
def getFullSizeAvatar(avatarid):
    response = requests.get('https://seepercdn.com/avatars/' + avatarid)

    return response

# GET thumbnail size avatar url
def getThumbnailSizeAvatar(avatarid):
    response = requests.get('https://seepercdn.com/avatars/thumbs/' + avatarid)

    return response

# GET all leagues a user is in for a given year
def getUserLeagues(userid, seasonint=2023, sport='nfl'):
    season = str(seasonint)
    response = requests.get('https://api.sleeper.app/v1/user/' + userid + '/leagues/' + sport + '/' + season)

    return response

# GET all leagues a user is in for a given year
def getUserDrafts(userid, seasonint=2023, sport='nfl'):
    season = str(seasonint)
    response = requests.get('https://api.sleeper.app/v1/user/' + userid + '/drafts/' + sport + '/' + season)

    return response

# GET all info for a given league
def getLeagueInfo(leagueid):
    response = requests.get('https://api.sleeper.app/v1/league/' + leagueid)

    return response

# GET all rosters in a given league (ownerID = userID in the response)
def getLeagueRosters(leagueid):
    response = requests.get('https://api.sleeper.app/v1/league/' + leagueid + '/rosters')

    return response

# GET all users in a given league
def getLeagueUsers(leagueid):
    response = requests.get('https://api.sleeper.app/v1/league/' + leagueid + '/users')

    return response

# GET all drafts for a given league
def getLeagueDrafts(leagueid):
    response = requests.get('https://api.sleeper.app/v1/league/' + leagueid + '/drafts')

    return response

# GET winners bracket for a given league
def getLeagueWinnersBracket(leagueid):
    response = requests.get('https://api.sleeper.app/v1/league/' + leagueid + '/winners_bracket')

    return response

# GET losers bracket for a given league
def getLeagueLosersBracket(leagueid):
    response = requests.get('https://api.sleeper.app/v1/league/' + leagueid + '/losers_bracket')

    return response

# GET all traded picks for a given league
def getLeagueTradedPicks(leagueid):
    response = requests.get('https://api.sleeper.app/v1/league/' + leagueid + '/traded_picks')

    return response

# GET weekly matchups in a league
def getWeeklyMatchups(leagueid, week):
    week = str(week)
    response = requests.get('https://api.sleeper.app/v1/league/' + leagueid + '/matchups/' + week)

    return response

# GET weekly transactions in a league
def getWeeklyMatchups(leagueid, week):
    week = str(week)
    response = requests.get('https://api.sleeper.app/v1/league/' + leagueid + '/transactions/' + week)

    return response

# GET all info for a given draft
def getDraftInfo(draftid):
    response = requests.get('https://api.sleeper.app/v1/draft/' + draftid)

    return response

# GET all picks for a given draft
def getDraftPicks(draftid):
    response = requests.get('https://api.sleeper.app/v1/draft/' + draftid + '/picks')

    return response

# GET all traded picks for a given draft
def getDraftTradedPicks(draftid):
    response = requests.get('https://api.sleeper.app/v1/draft/' + draftid + '/traded_picks')

    return response
