# strips excess spaces and lowercases the player names
def normalize_names(dataframe, col='player_name'):
    # Normalize the player names to lowercase, then title case
    dataframe[col] = dataframe[col].str.strip().str.lower().str.title()

    # Apply the abbreviation logic to names like "RJ" -> "R."
    def abbreviate_first_name(name):
        name_parts = name.split(" ")
        if len(name_parts) > 1 and len(name_parts[0]) == 2:  # Check if first name is 2 letters (e.g., "RJ")
            name_parts[0] = name_parts[0][0] + "."  # Abbreviate to the initial
        return " ".join(name_parts)

    # Apply the abbreviation function to the column
    dataframe[col] = dataframe[col].apply(abbreviate_first_name)

# sets player names as the indices for the dataframe
def set_idx(dataframe, col='player_name'):
        dataframe.set_index(col, inplace=True)