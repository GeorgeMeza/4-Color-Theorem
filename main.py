import pandas as pd
import networkx as nx
import pyvis
from pyvis.network import Network

df = pd.read_csv("graph_csvs/triangular_pyramid.csv")

network = nx.from_pandas_edgelist(df, source = "Source", target = "Target", edge_attr = "weight")

planar_embedding = nx.algorithms.check_planarity(network)[1]

embedding_data = planar_embedding.get_data()

clockwise_edges = []

for entry in embedding_data.items():
  u = entry[0]# starting node for edge
  for v in entry[1]:
    clockwise_edges.append([u,v]) # ending node for edge

def find_new_edge(starting_edge, planar_embedding, traveled_nodes, traveled_edges):
  old_starting_node, new_starting_node = starting_edge[0], starting_edge[1]
  node_neighbors = planar_embedding[new_starting_node]
  new_index = (node_neighbors.index(old_starting_node) + 1) % len(node_neighbors)
  new_edge = [new_starting_node, node_neighbors[new_index]]
  if new_edge not in traveled_edges:
    traveled_edges.append(new_edge)
  return new_edge

def travel_through_edge(edge, planar_embedding, traveled_nodes, traveled_edges):
  traveled_nodes.append(edge[1])
  next_edge = find_new_edge(edge, planar_embedding, traveled_nodes, traveled_edges)
  return next_edge

def get_face(starting_edge, planar_embedding, traveled_nodes, traveled_edges):
  starting_node = starting_edge[0]
  next_edge = travel_through_edge(starting_edge, planar_embedding, traveled_nodes, traveled_edges)
  while starting_node != next_edge[1]:
    next_edge = travel_through_edge(next_edge, planar_embedding, traveled_nodes, traveled_edges)
  return traveled_nodes
  
def find_faces(edges, planar_embedding):
  face_list = []
  traveled_edges = []
  for edge in edges:
    if edge not in traveled_edges:
      face = get_face(edge, planar_embedding, [edge[0]], traveled_edges)
      face_list.append(face)
  return face_list

def return_edges(face):
  face_edges = []
  for u,v in zip(face, face[1:]):
    face_edges.append([u,v])
  face_edges.append([face[0], face[-1]])
  return face_edges

def convert_faces_to_dict(faces):
  edge_dict = {}
  for face in faces:
    face_name = "face_" + str(faces.index(face))
    edges = return_edges(face)
    for edge in edges:
      if tuple(edge) in edge_dict:
        edge = [edge[1], edge[0]]
      edge_dict[tuple(edge)] = face_name
  return edge_dict

def convert_dict_to_df(edge_dict):
  csv_dict = {"Source": [], "Target": [], "Type": [], "weight": []}
  edges_used = []
  for edge in edge_dict:
    if edge not in edges_used:
      edges_used.append(edge)
      edge_array = [edge[0], edge[1]]
      reversed_edge = edge_array[::-1]
      if tuple(reversed_edge) in edge_dict:
        edges_used.append(tuple(reversed_edge))
        face_one = edge_dict[edge]
        face_two = edge_dict[tuple(reversed_edge)]
        csv_dict["Source"].append(face_one)
        csv_dict["Target"].append(face_two)
        csv_dict["Type"].append("Undirected")
        csv_dict["weight"].append(1)
  return pd.DataFrame.from_dict(csv_dict)

cube_faces = find_faces(clockwise_edges, embedding_data)
print(cube_faces)

dual_graph_dict = convert_faces_to_dict(cube_faces)
print(dual_graph_dict)

dual_df = convert_dict_to_df(dual_graph_dict)
print(dual_df)

dual_network = nx.from_pandas_edgelist(dual_df, source = "Source", target = "Target", edge_attr = "weight")

net = Network()

net.from_nx(dual_network)

for node in net.nodes:
  node['color'] = "red"

print(net.nodes)

net.show("index.html")

print("hi??")
