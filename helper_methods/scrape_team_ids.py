import requests
from bs4 import BeautifulSoup

# base urls
all_teams_url = "https://www.espn.com/mens-college-basketball/teams"

def get_team_ids(headers):
    # fetch from teams page
    response = requests.get(all_teams_url, headers=headers)
    response.raise_for_status()

    # parse
    soup = BeautifulSoup(response.text, "html.parser")

    # dictionary to store team names and ids
    team_links = {}

    # scrape all links on the page
    links = soup.find_all("a", class_="AnchorLink")

    # cycle through all links
    for link in links:
        # set team name and link based on link text and href
        team_name = link.text.strip()
        team_url = link.get("href")


        # filter for urls that are to teams
        if team_url and "/team/_/id/" in team_url and team_name:
            # grab id out of url
            team_id = team_url.split("/")[-2]
            team_links[team_name] = team_id



    return team_links