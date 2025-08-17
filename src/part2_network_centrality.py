'''
PART 2: NETWORK CENTRALITY METRICS

Using the imbd_movies dataset
- Build a graph and perform some rudimentary graph analysis, extracting centrality metrics from it. 
- Below is some basic code scaffolding that you will need to add to
- Tailor this code scaffolding and its stucture to however works to answer the problem
- Make sure the code is inline with the standards we're using in this class 
'''

import numpy as np
import pandas as pd
import networkx as nx
import json
from datetime import datetime


# Build the graph
g = nx.Graph()


# i had to change up the code completely because i didnt know  how to download the JSON file to use 'with open()'

# url of the JSON
file_url = "https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true"

# read the JSON lines directly using pandas
df = pd.read_json(file_url, lines=True)

# tterate through movies
for _, this_movie in df.iterrows():
    # add nodes for every actor
    for actor_id, actor_name in this_movie['actors']:
        g.add_node(actor_name)

    # add edges for every pair of actors
    actors = this_movie['actors']
    for i, (left_actor_id, left_actor_name) in enumerate(actors):
        for right_actor_id, right_actor_name in actors[i+1:]:
            if g.has_edge(left_actor_name, right_actor_name):
                g[left_actor_name][right_actor_name]['weight'] += 1
            else:
                g.add_edge(left_actor_name, right_actor_name, weight=1)

# print info
print("Nodes:", len(g.nodes))

# top 10 central nodes
degree_centrality = nx.degree_centrality(g)
top_10 = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 most central nodes:")
for actor, centrality in top_10:
    print(actor, centrality)

# save edge list to CSV
current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'data/network_centrality_{current_datetime}.csv'

edge_list = [{'left_actor_name': u, '<->': data['weight'], 'right_actor_name': v} 
             for u, v, data in g.edges(data=True)]

pd.DataFrame(edge_list).to_csv(output_file, index=False)
print(f"Network data saved to {output_file}")
