from os import link
import typing
from .link import Link
from .node import Node
from .packet import Packet
import json

class Arena:

    def __init__(self, filename: str) -> None:
        """
        Initialize an arena given a file containing: 
            1. a mapping of node types to their capabilities
            2. nodes of each type (identified by MAC address), and their locations as tuples
            3. rules for which types of nodes are allowed to connect to each other
        """
        with open(filename, 'r') as f:
            data = json.load(f)
            data_rules = data['rules']
            hierarchies = data['hierarchies']

        rules = {h: set() for h in hierarchies}
        for t1, t2 in data_rules:
            rules[t1].add(t2)
            rules[t2].add(t1)

        # mapping of hierarchies to list MAC addresses
        self.hierarchy_dict = {} 

        # mapping of MAC addresses to nodes
        self.node_dict = {}

        for hierarchy in hierarchies:
            transmit_distance = hierarchies[hierarchy]['strength']

            list_of_macs = []
            for node_obj in hierarchies[hierarchy]['nodes']:
                mac_addr = list(node_obj.keys())[0]
                x = node_obj[mac_addr]['x']               
                y = node_obj[mac_addr]['y']
                node = Node(mac_addr, x, y, hierarchy, transmit_distance, 0)

                for link_class in rules[hierarchy]:
                    if link_class not in self.hierarchy_dict:
                        continue
                    for other in self.hierarchy_dict[link_class]:
                        node_other = self.node_dict[other]
                        node.add_link(node_other)
                        node_other.add_link(node)

                list_of_macs.append(mac_addr)

                self.node_dict[mac_addr] = node
            
            self.hierarchy_dict[hierarchy] = list_of_macs

        
    
    def can_link(self, node1: str, node2: str) -> bool:
        """
        Given MAC addresses, test if two nodes can connect to one another.

        This involves checking if they are allowed to connect, as well as if they are close enough together
        that, given their power capabilities, they can reach one another.
        """
        return self.node_dict[node1].is_neighbor(node2) and self.node_dict[node2].is_neighbor(node1)

    def send_packet(self, src_node: str, dest_node: str) -> None:
        """
        Initiates a packet send from a source node, to a given a destination node.
        """
        start_node = self.node_dict[src_node]

        # do dijkstras here to find best path

        pass

    def simulate(self, timesteps: int, end_user_hierarchy_class: str, internet_enabled_hierarchy_class: str) -> dict[str, float]:
        """
        Simulates the arena for a given number of timesteps, with nodes from the end_user_hierarchy_class sending packets, and users from the internet_enabled_hierarchy_class will receive packets.
        """
        pass

    def run(self) -> None:
        """
        Steps the arena for one timestep
        """
        pass

    def get_nodes(self) -> dict[str, Node]:
        """
        Returns a dict mapping MAC addresses to node objects for all nodes in this arena
        """
        return {k: v for k, v in self.node_dict.items()}
