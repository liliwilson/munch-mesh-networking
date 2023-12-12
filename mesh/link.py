import typing
import random
from .packet import Packet


class Link:

    def __init__(self, node1: typing.Any, node2: typing.Any) -> None:
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

    # TESTING

    # This could prob also be used for setting the prob permanently?

    def get_probability(self) -> float:
        """
        Returns the probability that any packet send on this link will be completed

        Must be a value between 0 and 1 inclusive.
        """
        pass
