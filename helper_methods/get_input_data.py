import datetime
import yaml

def get_input_data():
    # load the YAML data from the file
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    # Accessing the data
    teams_to_scrape = config['teams_to_scrape']
    cutoff_date_split = config['cutoff_date'].split("/")
    cutoff_date = datetime.datetime(int(cutoff_date_split[2]), int(cutoff_date_split[0]), int(cutoff_date_split[1]))
    stats_to_pull = config['stats_to_pull']

    return teams_to_scrape, cutoff_date, stats_to_pull
