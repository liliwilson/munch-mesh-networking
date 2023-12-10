import typing
from .link import Link
from .node import Node
from .packet import Packet


class Arena:

    def __init__(self, filename: str) -> None:
        """
        Initialize an arena given a file containing: 
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

    def send_packet(self, src_node: str, dest_node: str) -> None:
        """
        Initiates a packet send from a source node, to a given a destination node.
        """
        pass

    def simulate(self, timesteps: int, end_user_hierarchy_class: str, internet_enabled_hierarchy_class: str) -> typing.Dict[str, float]:
        """
        Simulates the arena for a given number of timesteps, with nodes from the end_user_hierarchy_class sending packets, and users from the internet_enabled_hierarchy_class will receive packets.
        """
        pass
