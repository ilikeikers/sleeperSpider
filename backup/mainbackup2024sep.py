import helpers as api


def getUserID(username):
    id = None
    try:
        res = api.getUserInfo(username)
        id = res.get('user_id')
    except:
        print("Failed to get User ID")

    return id

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

id = getUserID('ilikeikers')
getLastDrafted(id)
