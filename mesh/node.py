import typing

from .packet import Packet
from .link import Link


class Node:

    def __init__(self, mac_address: str, x: float, y: float, hierarchy_class: str, transmit_distance: float, storage_size: float) -> None:
        """
        Creates a node object
        """
        self.mac_address = mac_address
        self.x = x
        self.y = y
        self.hierarchy_class = hierarchy_class
        self.transmit_distance = transmit_distance
        self.storage_size = storage_size

        self.links = {}

    def add_link(self, other: "Node") -> None:
        """
        Adds a link from self to other.
        """
        distance = min(self.transmit_distance, other.get_transmit_distance())
        other_x, other_y = other.get_position()
        actual = ((self.x - other_x) ** 2 + (self.y - other_y) ** 2) ** 0.5
        if actual <= distance:
            link = Link(self, other)
            self.links[other.get_mac()] = link 
        return
        

    def set_path(self, path: list[str]) -> None:
        """
        Sets the MAC address path from self to the supernode.
        """
        pass

    def generate_packet(self, dst: str) -> int:
        """
        Creates a generated packet with final destination dst and enqueues it.

        Outputs the packet_id of the packet generated.
        """
        pass

    def get_next_destination(self) -> str:
        """
        Returns the MAC address of the nexthop of the packet at the front of the queue.
        """
        pass

    def send_from_queue(self, timestep: int) -> Packet:
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
        return other in self.links

    def get_queue_state(self) -> list[Packet]:
        """
        Returns an ordered list of packets, representing self's current queue.
        """
        return []

    def get_packets_received(self) -> int:
        """
        Returns the number of packets that this node has received
        """
        return 0

    def get_position(self) -> tuple[float, float]:
        """
        Returns the position of the node in (x, y) format
        """
        return (self.x, self.y)
    
    def get_mac(self) -> str:
        """
        Returns the mac address of this node
        """
        return self.mac_address
    
    def get_transmit_distance(self) -> float:
        """
        Returns the transmit distance of this node
        """
        return self.transmit_distance


    def __str__(self) -> str:
        """
        Returns a human-readable version of the string.
        """
        return f"Node with MAC {self.mac_address}, at position ({self.x}, {self.y}) of class {self.hierarchy_class}"

    def __repr__(self) -> str:
        """
        Returns Node representation 
        """

        return f"Node(mac_addr=\"{self.mac_address}\", x={self.x}, y={self.y}, transmit_distance={self.transmit_distance}, hierarchy_class=\"{self.hierarchy_class}\")"


