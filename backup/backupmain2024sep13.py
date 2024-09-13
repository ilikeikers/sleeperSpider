from libs import dbutils as db
from libs import helpers as do

db.buildPlayerTables("players.json", "sleeperSpider.db")
db.insertPlayersData("players.json", "sleeperSpider.db")
do.storeFavorites(do.getUserID("richasian1044"), "test.txt")

# TESTS
#print(mostCommonMates(id))
#league_mates = mostCommonMates(id)
#favorite_players = getMostRosteredPlayers(id)
#print(favorite_players)
#getLastDrafted(id)
#leagues = getUsersLeagueIds(id)
#users = getAllUserIds(leagues)
#drafts = getAllCompletedDraftIds(users)
#picks = getPicks(drafts, id)
