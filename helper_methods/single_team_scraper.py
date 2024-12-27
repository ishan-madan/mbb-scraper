import cbbpy.mens_scraper as s
import pandas as pd
import os
from helper_methods import helpers


# scrapes the requested statistic from the ESPN website
def scrape_rel_stats(team_name, game_data, players, stat_type):

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
        helpers.normalize_names(game_bs, 'player')
        helpers.normalize_names(stat_df)

        # set indices for the dataframes
        helpers.set_idx(game_bs, 'player')
        helpers.set_idx(stat_df)

        # get relevant stats out of main DF
        stats = game_bs[[stat_type]]

        # set opp score if points is stat type
        if stat_type == 'pts':
            stats = stats.copy()
            stats.loc['Opp'] = opp_score

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
    print(f'Successfully scraped "{stat_type}" stats for {team_name}.')