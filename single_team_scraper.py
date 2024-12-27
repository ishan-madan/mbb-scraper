import cbbpy.mens_scraper as s
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import re
import os

# TODO: update these URLs if you want to use it for a different school or if the Duke MBB links change
team_url = "https://www.espn.com/mens-college-basketball/team/schedule/_/id/150"
player_url = "https://www.espn.com/mens-college-basketball/team/roster/_/id/150"

# TODO: update the team name if doing for another team (make sure it is the official name on ESPN)
team_name = "Duke Blue Devils"

# TODO: update the cutoff date for data you want to scrape
cutoff_date = datetime.datetime(2025, 1, 8)

# TODO: select the numerical stats you want to pull and add them to the stats_to_pull array. Options listed below:
# min, fgm, fga, 2pm, 2pa, 3pm, 3pa, ftm, fta, oreb, dreb, reb, ast, stl, blk, to, pf, pts
stats_to_pull = ['3pm', 'pts', 'ast', 'reb', 'min']


# add headers to avoid 403 errors
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# fetches player and game data from the ESPN website
def fetch_data(team_url, player_url):
    # fetch from team page
    team_res = requests.get(team_url, headers=headers)
    team_res.raise_for_status()
    
    # fetch from roster page
    player_res = requests.get(player_url, headers=headers)
    player_res.raise_for_status()
    
    # parse
    team_soup = BeautifulSoup(team_res.text, 'html.parser')
    player_soup = BeautifulSoup(player_res.text, 'html.parser')

    # get schedule table and roster table 
    schedule = team_soup.select('table tbody tr')
    roster = player_soup.find('table', class_='Table').find_all('tr')[1:]

    # get the list of players and numbers, as well as the list of games before the cutoff date
    players = get_player_data(roster)
    game_data = get_game_data(schedule)
    
    return players, game_data
    
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
            match = re.match(r"([a-zA-Z\s]+)(\d+)$", player_name)
            player_name = match.group(1).strip().split(" ")[0][0] + ". " + match.group(1).strip().split(" ")[1]
            player_number = match.group(2)

            # append to array
            players.append([player_name, player_number])

    # manually append team and opp to the array with random numbers
    players.append(["team", 6999])
    players.append(["opp", 7000])

    return players

# grabs game data off the schedule table
def get_game_data(schedule):
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

# strips excess spaces and lowercases the player names
def normalize_names(dataframe, col='player_name'):
    dataframe[col] = dataframe[col].str.strip().str.lower()

# sets player names as the indices for the dataframe
def set_idx(dataframe, col='player_name'):
        dataframe.set_index(col, inplace=True)

# scrapes the requested statistic from the ESPN website
def scrape_rel_stats(game_data, stat_type):
    # create stat dataframe
    stat_df = pd.DataFrame(players, columns=['player_name', 'player_number'])

    # loop through all games
    for game in game_data:
        # grab info off the game data
        game_id, opponent_team, game_date, location = game

        # get box score
        game_bs = s.get_game_boxscore(game_id)

        # initialize opp score (only gets used for pts)
        opp_score = 0

        # get opponent score if stat type is points and the game has been played
        if stat_type == 'pts' and 'team' in game_bs.columns:
            opp_score = game_bs[game_bs['team'] == opponent_team][game_bs['player'] == 'TEAM']['pts'].values

            if len(opp_score) >= 1:
                opp_score = opp_score[0]
            else:
                opp_score = 0

        # filter out data for other teams. skip if the game has not been played
        if 'team' in game_bs.columns:
            game_bs = game_bs[game_bs['team'] == team_name]
        else:
            continue

        # if there is no data for our team, skip
        if game_bs.empty:
            continue

        # create the column name with the correct format
        column_name = f"{location}{opponent_team} ({game_date})"

        # normalize the names in our dataframes
        normalize_names(game_bs, 'player')
        normalize_names(stat_df)

        # set indices for the dataframes
        set_idx(game_bs, 'player')
        set_idx(stat_df)

        # get relevant stats out of main DF
        stats = game_bs[[stat_type]]

        # set opp score if points is stat type
        if stat_type == 'pts':
            stats = stats.copy()
            stats.loc['opp'] = opp_score

        # fill empty cells with 0
        stat_df = stat_df.fillna(0)

        # merge into main dataframe
        stat_df = stat_df.join(stats[[stat_type]], how='left', rsuffix=f'_{column_name}')

        # rename columns
        stat_df.rename(columns={stat_type: column_name}, inplace=True)

        # reset index
        stat_df.reset_index(inplace=True)

    # generate folder naming convention
    folder_name = "_".join(team_name.lower().split(" ")) + "_stats"

    # create directory if it doesn't exit
    os.makedirs(folder_name, exist_ok=True)

    # export to csv
    stat_df.to_csv(f'{folder_name}/player_{stat_type}.csv', index=False)

    # print to terminal to alert user to completed action
    print(f'Successfully scraped {stat_type} stats.')


# get the player and game data
players, games = fetch_data(team_url, player_url)

# loop through all desired stats
for stat in stats_to_pull:
    scrape_rel_stats(games, stat)