# base urls
base_team_url = "https://www.espn.com/mens-college-basketball/team/schedule/_/id/"
base_roster_url = "https://www.espn.com/mens-college-basketball/team/roster/_/id/"

def generate_urls(id):
    # set team urls
    team_url = base_team_url + id
    roster_url = base_roster_url + id

    return team_url, roster_url