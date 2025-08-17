'''
PART 2: SIMILAR ACTROS BY GENRE

Using the imbd_movies dataset:
- Create a data frame, where each row corresponds to an actor, each column represents a genre, and each cell captures how many times that row's actor has appeared in that column’s genre 
- Using this data frame as your “feature matrix”, select an actor (called your “query”) for whom you want to find the top 10 most similar actors based on the genres in which they’ve starred 
- - As an example, select the row from your data frame associated with Chris Hemsworth, actor ID “nm1165110”, as your “query” actor
- Use sklearn.metrics.DistanceMetric to calculate the euclidean distances between your query actor and all other actors based on their genre appearances
- - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.DistanceMetric.html
- Output a CSV continaing the top ten actors most similar to your query actor using cosine distance 
- - Name it 'similar_actors_genre_{current_datetime}.csv' to `/data`
- - For example, the top 10 for Chris Hemsworth are:  
        nm1165110 Chris Hemsworth
        nm0000129 Tom Cruise
        nm0147147 Henry Cavill
        nm0829032 Ray Stevenson
        nm5899377 Tiger Shroff
        nm1679372 Sudeep
        nm0003244 Jordi Mollà
        nm0636280 Richard Norton
        nm0607884 Mark Mortimer
        nm2018237 Taylor Kitsch
- Describe in a print() statement how this list changes based on Euclidean distance
- Make sure your code is in line with the standards we're using in this class
'''

#Write your code below

import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances
from datetime import datetime

# read the JSON dataset directly from the URL
file_url = "https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true"
df = pd.read_json(file_url, lines=True)

# build the actor-genre matrix
actor_genre = {}

for _, row in df.iterrows():
    genres = row['genres']  # list of genres for this movie
    actors = row['actors']  # list of tuples (actor_id, actor_name)
    
    for actor_id, actor_name in actors:
        if actor_id not in actor_genre:
            actor_genre[actor_id] = {'name': actor_name}
        # count genres
        for genre in genres:
            actor_genre[actor_id][genre] = actor_genre[actor_id].get(genre, 0) + 1

# convert to DataFrame
actor_genre_df = pd.DataFrame.from_dict(actor_genre, orient='index').fillna(0)

# keep a mapping of actor_id to name
actor_names = actor_genre_df.pop('name')

# select query actor
query_actor_id = 'nm1165110'  # Chris Hemsworth
query_vector = actor_genre_df.loc[query_actor_id].values.reshape(1, -1)

# compute cosine distances
distances = pairwise_distances(actor_genre_df.values, query_vector, metric='cosine').flatten()

# combine with actor IDs
results_df = pd.DataFrame({
    'actor_id': actor_genre_df.index,
    'actor_name': actor_names.values,
    'cosine_distance': distances
})

# sort by smallest distance (most similar)
top_10 = results_df.sort_values('cosine_distance').iloc[1:11]  # skip the query itself

# save to CSV
current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'data/similar_actors_genre_{current_datetime}.csv'
top_10.to_csv(output_file, index=False)

print(f"Top 10 most similar actors to Chris Hemsworth saved to {output_file}")

