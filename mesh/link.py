import typing
import random
from .node import Node
from .packet import Packet


class Link:

    def __init__(self, node1: Node, node2: Node) -> None:
        """
        Creates a link object between node1 and node2. 
        """
        pass

    def transmit(self, packet: Packet, source: str) -> bool:
        """
        Given a packet and a source MAC address, returns True iff the destination node receives the packet.

        Determined based on distance between nodes and strengths of the nodes.
        """
        pass
