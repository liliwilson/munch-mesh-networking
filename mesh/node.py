import typing

from .packet import Packet


class Node:

    def __init__(self, mac_address: str, x: float, y: float, hierarchy_class: str, transmit_power: float, storage_size: float) -> None:
        """
        Creates a node object
        """
        pass

    def add_link(self, other: "Node") -> None:
        """
        Adds a link from self to other.
        """
        pass

    def generate_packet(self, dst: str) -> None:
        """
        Creates a generated packet with final destination dst and enqueues it.
        """
        pass

    def send_from_queue(self) -> None:
        """
        Dequeues the next packet and sends the packet to its next hop. 
        """
        pass

    def receive_packet(self, packet: Packet) -> None:
        """
        Receives a packet and adds the packet to own queue.
        """
        pass
