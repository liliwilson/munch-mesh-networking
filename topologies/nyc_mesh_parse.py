import json
import pyproj as proj

with open('./map_data/links.json', 'r') as f:
    links_data = json.load(f)

with open('./map_data/nodes.json', 'r') as f:
    nodes_data = json.load(f)

node_ids = {node['id']: node for node in nodes_data}

user_nodes = set()
supernodes = set()
hubs = set()

# go through every link that is real (not a "planned" link)
for link in links_data:
    if link['status'] != 'planned':
        # if both sides of link are valid nodes
        if link['from'] in node_ids and link['to'] in node_ids:
            if "status" in node_ids[link['to']]:
                # check that the node is installed and not planned
                if node_ids[link['to']]['status'] == 'Installed':
                    if 'notes' in node_ids[link['to']]:
                        notes = node_ids[link['to']]['notes'] 
                        if 'hub' in notes.lower():
                            hubs.add(link['to'])
                        elif 'supernode' in notes.lower():
                            supernodes.add(link['to'])
                        else: 
                            user_nodes.add(link['to'])

            if "status" in node_ids[link['from']]:
                # check that the node is installed and not planned
                if node_ids[link['from']]['status'] == 'Installed':
                    if 'notes' in node_ids[link['from']]:
                        notes = node_ids[link['from']]['notes'] 
                        if 'hub' in notes.lower():
                            hubs.add(link['from'])
                        elif 'supernode' in notes.lower():
                            supernodes.add(link['from'])
                        else: 
                            user_nodes.add(link['from'])

print(f"supernodes: {len(supernodes)}, hub nodes: {len(hubs)}, user nodes: {len(user_nodes)}")

# convert lon, lat coords to x, y coords
transformer = proj.Transformer.from_crs("epsg:4326", "epsg:3857", always_xy=True)
base_x, base_y = transformer.transform(-74.0060, 40.7128) # lat and lon of "nyc", helpful for scaling

user_node_coords = {}
for node in user_nodes:
    lon, lat, _ = node_ids[node]['coordinates']
    x, y = transformer.transform(lon, lat)
    # print(lon, lat, '->', base_x - x, base_y - y)
    user_node_coords[f"n{node}"] = {'x': base_x - x, 'y': base_y - y}

hub_node_coords = {}
for node in hubs:
    lon, lat, _ = node_ids[node]['coordinates']
    x, y = transformer.transform(lon, lat)
    # print(lon, lat, '->', base_x - x, base_y - y)
    hub_node_coords[f"n{node}"] = {'x': base_x - x, 'y': base_y - y}

supernode_coords = {}
for node in supernodes:
    lon, lat, _ = node_ids[node]['coordinates']
    x, y = transformer.transform(lon, lat)
    # print(lon, lat, '->', base_x - x, base_y - y)
    supernode_coords[f"n{node}"] = {'x': base_x - x, 'y': base_y - y}

# set up json file
rules = [
    ['supernode', 'hub'],
    ['supernode', 'user'],
    ['user', 'hub'],
    ['hub', 'hub']
]

hierarchies = {
    'supernode': {
        'strength': 10000000,
        'nodes': [
            supernode_coords
        ]
    },
    'hub': {
        'strength': 1000000,
        'nodes': [
            hub_node_coords
        ]
    },
    'user': {
        'strength': 1000,
        'nodes': [
            user_node_coords
        ]
    }
}

json_temp = {"hierarchies": hierarchies, "rules": rules, "responseWaitTime": 1}

with open('./nycmesh.json', 'w') as f:
    json.dump(json_temp, f)