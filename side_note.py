import pandas as pd
import networkx as nx
import pyvis
from pyvis.network import Network

cube_df = pd.read_csv("graph_csvs/cube.csv")

cube_network = nx.from_pandas_edgelist(cube_df, source = "Source", target = "Target", edge_attr = "weight")

colors_df = pd.read_csv("graph_csvs/colors.csv")

colors_network = nx.from_pandas_edgelist(colors_df, source = "Source", target = "Target", edge_attr = "weight")
print(cube_df)

print("hi")

print(colors_network.edges)
cube_net = Network()

cube_net.from_nx(cube_network)
cube_net.toggle_physics(False)

colors_net = Network()

colors_net.from_nx(colors_network)
colors_net.toggle_physics(False)


cube_net.show("index.html")

colors_net.show("index.html")

print("hi??")
