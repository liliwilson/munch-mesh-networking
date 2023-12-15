import typing
import random
from .packet import Packet

class Link:

    def __init__(self, node1: typing.Any, node2: typing.Any) -> None:
        """
        Creates a link object between node1 and node2. 
        """
        self.node1 = node1
        self.node2 = node2

    def transmit(self, packet: Packet, source: str, timestep: int, override: bool) -> bool:
        """
        Given a packet and a source MAC address, returns True iff the destination node receives the packet.

        Determined based on distance between nodes and strengths of the nodes.
        """
        success = random.random() < self.get_probability()
        if override:
            success = True
        if not success:
            return success
        elif source == self.node1.get_mac():
            self.node2.enqueue_packet(packet, timestep)
        elif source == self.node2.get_mac():
            self.node1.enqueue_packet(packet, timestep) 
        else: 
            raise ValueError("node must be connected to link to transmit over it")
        return success

    def get_probability(self) -> float:
        """
        Return the probability of successful transmission along this node using the formula from https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7954581, with randomness in the formula removed for ease of testing. 
        """
        transmit_range = min(self.node1.get_transmit_distance(),
                             self.node2.get_transmit_distance())
        n1_x, n1_y = self.node1.get_position()
        n2_x, n2_y = self.node2.get_position()
        actual = ((n1_x - n2_x) ** 2 + (n1_y - n2_y) ** 2) ** 0.5

        return max(1 - 0.8 * actual / transmit_range, 0)
