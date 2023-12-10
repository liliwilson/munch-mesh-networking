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

    def set_path(self, path: typing.List[str]) -> None:
        """
        Sets the MAC address path from self to the supernode.
        """
        pass

    def generate_packet(self, dst: str) -> None:
        """
        Creates a generated packet with final destination dst and enqueues it.
        """
        pass

    def get_next_destination(self) -> str:
        """
        Returns the MAC address of the nexthop of the packet at the front of the queue.
        """
        pass

    def send_from_queue(self, timestep: int) -> None:
        """
        Dequeues the next packet and sends the packet to its next hop. 
        """
        pass

    def receive_packet(self, packet: Packet, timestep: int) -> None:
        """
        Receives a packet and adds the packet to own queue.

        If self is destination of packet, check if self sent packet with this packet id. If no, enqueue a response packet with same packet id. 
        """
        pass

    # Testing

    def is_neighbor(self, other: str) -> bool:
        """
        Given the MAC address of another node, returns True iff there is a link between self and other.
        """
        pass
