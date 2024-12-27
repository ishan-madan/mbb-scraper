from helper_methods import scrape_game_and_player_data, scrape_team_ids, single_team_scraper, generate_urls, get_input_data

# get input data
teams_to_scrape, cutoff_date, stats_to_pull = get_input_data.get_input_data()

# add headers to avoid 403 errors
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# scrape all teams and their ids
team_ids = scrape_team_ids.get_team_ids(headers)

# loop through all teams
for team in teams_to_scrape:
    # get urls for team
    if team in team_ids:
        team_url, roster_url = generate_urls.generate_urls(team_ids[team])
    else:
        print(f"Cannot find team by name: {team}")
        continue

    # get game and player data for this team
    game_data, players = scrape_game_and_player_data.fetch_data(team_url, roster_url, headers, cutoff_date)

    # loop through and get each stat for this team
    for stat in stats_to_pull:
        single_team_scraper.scrape_rel_stats(team, game_data, players, stat)