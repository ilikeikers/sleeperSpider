import helpers as api
import json


"""
Sleeper stores their players in a database indexed with a number. This is a pretty large file to download (like 12 MB).
They request that that API endpoint is only called once per day. I call that endpoint manually and store it in a file.

Example commands in a terminal:
cd ~/path/to/working/directory
curl "https://api.sleeper.app/v1/players/nfl" -o players.json

This saves that data in a file that I can use at will.
"""
with open("players.json") as player_data:
    PLAYERS = json.load(player_data)
    player_data.close()

# A global player map is created so that player full names can replace their assigned number as needed
def buildPlayerMap(players):
    player_map = {}
    for player in players:
        full_name = players[player].get('full_name')
        if full_name is not None:
            player_map[player] = full_name
        else:
            player_map[player] = "DEF " + str(player)
    return player_map
PLAYERS_MAP = buildPlayerMap(PLAYERS)


def getUserID(username):
    id = None
    try:
        res = api.getUserInfo(username)
        id = res.get('user_id')
    except:
        print("Failed to get User ID")

    return id

# Prints the last person drafted if a draft is happening
def getLastDrafted(user_id):
    drafts = api.getUserDrafts(user_id)
    for draft in drafts:
        if draft.get('status') == 'drafting':
            league_metadata = draft.get('metadata')
            league_name = league_metadata.get('name')
            picks = api.getDraftPicks(draft.get('draft_id'))
            last_pick = picks[-1]
            last_drafter = last_pick.get('picked_by')
            pick_num = last_pick.get('pick_no')
            player_metadata = last_pick.get('metadata')
            drafter_info = api.getUserInfo(last_drafter)
            username = drafter_info.get('username')

            player_first_name = player_metadata.get('first_name')
            player_last_name = player_metadata.get('last_name')
            player_pos = player_metadata.get('position')
            print(f"{username} drafted {player_pos} {player_first_name} {player_last_name} with pick number {pick_num} in {league_name}")

    return

# Gets leagues a user is in
def getLeagues(user_id):
    leagues = []
    drafts = api.getUserDrafts(user_id)
    for draft in drafts:
        if draft.get('league_id') not in leagues:
            leagues.append(draft.get('league_id'))
    return leagues

# Gets users in a league
def getUsers(leagues):
    users = []
    for league_id in leagues:
        league_users = api.getLeagueUsers(league_id)
        for league_user in league_users:
            if league_user.get('user_id') not in users:
                users.append((league_user.get('user_id'), league_user.get('display_name')))
    return users

# Gets completed drafts
def getDrafts(users):
    drafts = []
    for user_id, _ in users:
        user_drafts = api.getUserDrafts(user_id)
        for user_draft in user_drafts:
            if user_draft.get('status') == 'complete' and user_draft.get('draft_id') not in drafts:
                drafts.append(user_draft.get('draft_id'))
    return drafts

# Prints pretty stuff. Useless function right now
def getPicks(drafts, user_id):
    picks = {}
    print(drafts)
    for draft in drafts:
        draft_info = api.getDraftInfo(draft)
        print(draft_info)
        #print(api.getDraftPicks(draft))

    return

# Find and sort your most common league mates
def mostCommonMates(user_id):
    league_mates = {}
    leagues = getLeagues(user_id)
    for league in leagues:
        league_users = api.getLeagueUsers(league)
        for league_user in league_users:
            league_user_id = league_user.get('user_id')
            league_user_name = league_user.get('display_name')
            if league_user_id in league_mates:
                _, count = league_mates.get(league_user_id)
                league_mates[league_user_id] = (league_user_name, count + 1)
            else:
                league_mates[league_user_id] = (league_user_name, 1)

    sorted_dict = dict(reversed(sorted(league_mates.items(), key=lambda item: item[1][1])))

    return sorted_dict

# Get your favorite players.
# Only returns if the player is owned in more than one league
def getFavoritePlayers(user_id):
    favorite_players = {}
    leagues = getLeagues(user_id)
    for league in leagues:
        rosters = api.getLeagueRosters(league)
        if rosters:
            for roster in rosters:
                if user_id != roster.get('owner_id'):
                    continue
                players = roster.get('players')
                if players:
                    for player in players:
                        count = favorite_players.get(player, 0)
                        favorite_players[player] = count + 1

    sorted_dict = dict(reversed(sorted(favorite_players.items(), key=lambda item: item[1])))

    # Own function?
    favorites = {}
    for player in sorted_dict:
        if sorted_dict[player] <= 1:
            continue
        player_name = PLAYERS_MAP[player]
        count = sorted_dict[player]
        favorites[player_name] = count

    return favorites

def getLeagueMatesFavorites(user_id):
    all_favorite_players = {}
    league_mates = mostCommonMates(user_id)
    for mate in league_mates:
        username, _ = league_mates[mate]
        favorite_players = getFavoritePlayers(mate)
        all_favorite_players[username] = favorite_players

    return all_favorite_players

id = getUserID("ilikeikers")
favs = getLeagueMatesFavorites(id)
with open("ikesFavs.txt", "w") as out:
    for fav in favs:
        out.write(fav + "\n")
        out.write(str(favs[fav]) + "\n")
    out.close()

# TESTS
#print(mostCommonMates(id))
#league_mates = mostCommonMates(id)
#favorite_players = getFavoritePlayers(id)
#print(favorite_players)
#getLastDrafted(id)
#leagues = getLeagues(id)
#users = getUsers(leagues)
#drafts = getDrafts(users)
#picks = getPicks(drafts, id)
