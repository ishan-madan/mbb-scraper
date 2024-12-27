import requests
from bs4 import BeautifulSoup
import datetime
import re

# fetches player and game data from the ESPN website
def fetch_data(team_url, roster_url, headers, cutoff_date):
    # fetch from team page
    team_res = requests.get(team_url, headers=headers)
    team_res.raise_for_status()

    # fetch from roster page
    player_res = requests.get(roster_url, headers=headers)
    player_res.raise_for_status()

    # parse
    team_soup = BeautifulSoup(team_res.text, 'html.parser')
    player_soup = BeautifulSoup(player_res.text, 'html.parser')

    # get schedule table and roster table 
    schedule = team_soup.select('table tbody tr')
    roster = player_soup.find('table', class_='Table').find_all('tr')[1:]

    # get the list of players and numbers, as well as the list of games before the cutoff date
    players = get_player_data(roster)
    game_data = get_game_data(schedule, cutoff_date)

    return game_data, players


# grabs player data off the roster table
def get_player_data(roster):
    # array to store
    players = []

    # loop through all values in roster
    for row in roster:
        # get player name from the table
        cells = row.find_all('td')
        if len(cells) > 1:
            player_name_cell = cells[1]
            player_name = player_name_cell.get_text().strip()

            # extract name (in F. Last format so it works with cbbpy later) and number
            match = re.match(r"^(.+?)(\d+)$", player_name)
            if match:
                player_name = match.group(1).strip().split(" ")[0][0] + ". " + " ".join(match.group(1).strip().split(" ")[1:])
                player_number = match.group(2)
            else:
                print("No match found for roster:", player_name)
                player_name = "Unknown"
                player_number = "100"

            # append to array
            players.append([player_name, player_number])

    # manually append team and opp to the array with random numbers
    players.append(["team", 6999])
    players.append(["opp", 7000])

    return players


# grabs game data off the schedule table
def get_game_data(schedule, cutoff_date):
    # array to store game details
    game_data = []

    for row in schedule:
        # get date and parse
        date_cell = row.find('td', class_='Table__TD')
        if not date_cell or not date_cell.text.strip():
            continue

        game_date_str = date_cell.text.strip()
        try:
            game_date = datetime.datetime.strptime(game_date_str, '%a, %b %d')
            # add year manually
            game_date = game_date.replace(year=2024 if game_date.month >= 11 else 2025)
        except ValueError:
            continue

        # skip games after the cutoff date
        if game_date > cutoff_date:
            continue

        # find all <a> tags in current row
        game_links = row.find_all('a', href=True)
        if len(game_links) > 1:
            # get team and game link
            team_link = game_links[1]
            game_link = game_links[2]

            # extract team name from the url and format it
            team_name = " ".join(team_link['href'].split('/')[-1].split("-")).title()

            # extract the game ID from the url
            game_id = game_link['href'].split('/gameId/')[-1].split("/")[0]

            # set loc to home default and reset if away
            location = "v "
            if "@" in row.text:
                location = "@ "

            # append the game data with the correct game ID and date
            game_data.append([game_id, team_name, game_date.strftime('%m/%d'), location])

    return game_data