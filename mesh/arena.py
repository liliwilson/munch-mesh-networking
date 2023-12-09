import typing
from .link import Link
from .node import Node
from .packet import Packet

class Arena:

    def __init__(self, filename: str):
        """
        Initialize an arena given a file containing: 
            0. arena size
            1. a mapping of node types to their capabilities
            2. nodes of each type (identified by MAC address), and their locations as tuples
            3. rules for which types of nodes are allowed to connect to each other
        """
        pass

    def can_link(self, node1: str, node2: str) -> bool:
        """
        Given MAC addresses, test if two nodes can connect to one another.

        This involves checking if they are allowed to connect, as well as if they are close enough together
        that, given their power capabilities, they can reach one another.
        """
        pass

    def send_packet(self, src_node: str, dest_node: str):
        """
        Initiates a packet send from a source node, to a given a destination node.
        """
        pass

    def send_data_stream(self, src_node: str, dest_node: str) -> float:
        """
        Send a stream of data from source to destination, returns a float containing how many packets were received by dest.
        """
        pass


