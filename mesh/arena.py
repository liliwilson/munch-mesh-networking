import typing
from .link import Link
from .node import Node
from .packet import Packet
import json
import heapq
import random

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

        response_wait_time: int = data['responseWaitTime']

        rules = {h: set() for h in hierarchies}
        for t1, t2 in data_rules:
            rules[t1].add(t2)
            rules[t2].add(t1)

        # mapping of hierarchies to list MAC addresses
        self.hierarchy_dict: dict[str, list[str]] = {}

        # mapping of MAC addresses to nodes
        self.node_dict: dict[str, Node] = {}

        for hierarchy in hierarchies:
            transmit_distance = hierarchies[hierarchy]['strength']

            list_of_macs = []

            all_nodes = hierarchies[hierarchy]['nodes'][0]
            for mac_addr, node_obj in all_nodes.items():
                x = node_obj['x']
                y = node_obj['y']
                node = Node(mac_addr, x, y, hierarchy,
                            transmit_distance, response_wait_time, 0)

                for link_class in rules[hierarchy]:
                    # if linked to own class, check against current list of MACs
                    if link_class == hierarchy:
                        for other in list_of_macs:
                            node_other = self.node_dict[other]
                            node.add_link(node_other)
                            node_other.add_link(node)

                    # otherwise, check amongst the already finalized hierarchy classes
                    if link_class not in self.hierarchy_dict:
                        continue
                    for other in self.hierarchy_dict[link_class]:
                        node_other = self.node_dict[other]
                        node.add_link(node_other)
                        node_other.add_link(node)

                list_of_macs.append(mac_addr)

                self.node_dict[mac_addr] = node

            self.hierarchy_dict[hierarchy] = list_of_macs

        self.active_node_list: list[str] = list(self.node_dict.keys())
        self.timestep: int = 0
        self.packets_queued: int = 0

    def can_link(self, node1: str, node2: str) -> bool:
        """
        Given MAC addresses, test if two nodes can connect to one another.

        This involves checking if they are allowed to connect, as well as if they are close enough together
        that, given their power capabilities, they can reach one another.
        """
        return self.node_dict[node1].is_linked(node2) and self.node_dict[node2].is_linked(node1)

    def send_packet(self, src_node: str, dst_node: str, is_two_way: bool = True) -> None:
        """
        Initiates a packet send from a source node, to a given a destination node.
        """
        # TODO do we want to define behavior for if start and end equal
        if src_node == dst_node:
            return

        probabilities = {node: 0 for node in self.node_dict.keys()}
        probabilities[src_node] = -1
        predecessors = {node: None for node in self.node_dict.keys()}

        priority_queue = [(-1, src_node)]

        while priority_queue:
            current_prob, current_node = heapq.heappop(priority_queue)
            if current_prob > probabilities[current_node]:
                continue

            if current_node == dst_node:
                break

            node_obj = self.node_dict[current_node]
            for neighbor in node_obj.get_neighbors():
                new_prob = current_prob * node_obj.get_probability(neighbor)
                neighbor_prob = probabilities[neighbor]

                if new_prob < neighbor_prob:
                    probabilities[neighbor] = new_prob
                    predecessors[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_prob, neighbor))

        best_path = []
        current_node = dst_node
        while current_node is not None:
            best_path.insert(0, current_node)
            current_node = predecessors[current_node]

        # TODO do we want to set storage size as a constant, or input to arena?
        packet = Packet(0, is_two_way, best_path)
        self.node_dict[src_node].enqueue_packet(packet, self.timestep)

    def simulate(self, timesteps: int, end_user_hierarchy_class: str, internet_enabled_hierarchy_class: str, min_stream_size: int = 1, max_stream_size: int = 1, probability_send: float = 0.01) -> dict[str, float]:
        """
        Simulates the arena for a given number of timesteps, with nodes from the end_user_hierarchy_class sending packets, and users from the internet_enabled_hierarchy_class will receive packets.
        
        To simulate data streams, will queue random number of packets between min_stream_size and max_stream_size, and at any timestep the probability that a sender node will enqueue a new message is equal to probability_send.
        """
        while self.timestep < timesteps:
            # queue messages
            for end_user in self.hierarchy_dict[end_user_hierarchy_class]:
                # randomly pick a supernode to send to
                internet_enabled_node = random.choice(self.hierarchy_dict[internet_enabled_hierarchy_class])
                
                # with random probability, send a flow
                if random.random() < probability_send:
                    num_packets_in_flow = random.randint(min_stream_size, max_stream_size)
                    for _ in range(num_packets_in_flow):
                        self.send_packet(end_user, internet_enabled_node)
                    
            self.run()

        # get metrics
        per_node_metrics = {}
        for node_mac, node in self.node_dict.items():
            sent = node.get_sent()
            received = node.get_received()

            packet_drops, packet_successes = 0, 0
            latencies = []
            for packet_id in sent:
                if packet_id not in received:
                    packet_drops += 1
                else:
                    packet_successes += 1
                    latencies.append(received[packet_id] - sent[packet_id])

            per_node_metrics[node_mac] = {
                'successes': packet_successes,
                'throughput': packet_successes / timesteps,
                'drops': packet_drops,
                'average_latency': sum(latencies)/len(latencies) if len(latencies) > 0 else float('inf')
            }
        
        return per_node_metrics


        # get metrics after running
            # throughput: across nodes, sum packets received
                # measure packet loss? sum packets sent
            # latency: across nodes, average timestep received - timestep sent
            # fairness: compare things across nodes, also compare to # hops away from supernode

        return {}

    def run(self, override=False) -> None:
        """
        Steps the arena for one timestep
        """
        sending: list[Node] = []
        nexthops = set()
        ht = set() 

        for node in self.active_node_list:
            node_obj = self.node_dict[node]
            node_queue = node_obj.get_queue_state()
            if not node_queue:
                continue

            # check if medium is free by comparing to nodes in sending
            for sender in sending:
                # checks if either one is in range of the other
                if node_obj.in_range(*sender.get_position()):
                    break
                elif sender.in_range(*node_obj.get_position()):
                    break
            else:
                sending.append(node_obj)
                nexthop = node_obj.get_next_destination()
                if nexthop in nexthops:
                    ht.add(nexthop)
                else:
                    nexthops.add(nexthop)

        for ht_node in ht:
            nexthops.remove(ht_node)

        for sender in sending:
            dest = sender.get_next_destination()
            sender.send_from_queue(
                self.timestep, bool(dest in ht), override)

        for sender in sending:
            self.active_node_list.remove(sender.get_mac())
            self.active_node_list.append(sender.get_mac())

        # this bit tells nodes whether they should create a response packet
        for node in self.active_node_list:
            node_obj = self.node_dict[node]
            node_obj.learn_timestep(self.timestep)

        self.timestep += 1

    def get_nodes(self) -> dict[str, Node]:
        """
        Returns a dict mapping MAC addresses to node objects for all nodes in this arena
        """
        return {k: v for k, v in self.node_dict.items()}
