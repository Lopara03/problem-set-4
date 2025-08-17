'''
PART 1: ETL the dataset and save in `data/`

Here is the imbd_movie data:
https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true

It is in JSON format, so you'll need to handle accordingly and also figure out what's the best format for the two analysis parts. 
'''

import os
import pandas as pd
import json

def etl():

# Create '/data' directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)

    # Load datasets and save to '/data'
    url = "https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true"
    df = pd.read_json(url, lines=True)

    #cleaning: drop duplicates, reset index
    df = df.drop_duplicates().reset_index(drop=True)

# seeing if unique ID column exists
    if "movie_id" not in df.columns:
            df["movie_id"] = df.index + 1

# saving cleaned data for later analysis
    cleaned_path = os.path.join(data_dir, "imdb_movies_cleaned.csv")
    df.to_csv(cleaned_path, index=False)

    print(f" ETL complete. Cleaned dataset saved to {cleaned_path}")

    return df
