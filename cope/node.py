import typing
from .packet import Packet, COPEPacket, ReceptionReport
from .link import Link


class Node:

    def __init__(self, mac_address: str, x: float, y: float, hierarchy_class: str, transmit_distance: float, response_wait_time: int, storage_size: float) -> None:
        """
        Creates a node object
        """
        self.mac_address = mac_address
        self.x, self.y = x, y
        self.hierarchy_class: str = hierarchy_class
        self.transmit_distance: float = transmit_distance
        self.response_wait_time: int = response_wait_time
        self.storage_size: float = storage_size

        self.links: dict[str, Link] = {}

        self.queue: list[tuple[Packet, int]] = []  # TODO: needs to be changed
        self.sent = set()
        self.waiting_for_response: dict[int, Packet] = {}
        self.received_packets = 0

    def add_link(self, other: "Node") -> None:
        """
        Adds a link from self to other and creates a queue for that neighbor in self.
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

    def generate_packet(self, dst: str) -> None:
        """
        Creates a generated packet with final destination dst and enqueues it.
        """
        pass

    def get_next_destinations(self) -> str:
        """
        Returns the MAC address of the nexthop of the packets that will be sent next.
        """
        pass

    def send_from_queues(self, timestep: int) -> None:
        """
        Look for an encoding opportunity amongst the heads of our neighbor queues.

        Dequeues the next packet(s), creates a COPEPacket object, and sends the packet to its next hops. 
        """
        pass

    def receive_packet(self, packet: COPEPacket, timestep: int) -> None:
        """
        Receives a packet, tries to decode it, and adds the packet to own queue.

        If self is destination of packet, check if self sent packet with this packet id. If no, enqueue a response packet with same packet id. 
        """
        pass

    def receive_reception_report(self, reception_report: ReceptionReport, timestep: int) -> None:
        """
        Receives a reception report and updates stored neighbor state.
        """
        pass

    def is_linked(self, other: str) -> bool:
        """
        Given the MAC address of another node, returns True iff there is a link between self and other.
        """
        return other in self.links

    # TODO will it be an issue that this method is not taking into account another nodes transmission range?
    # this is to be used for determining if the medium is being used currently
    def in_range(self, x: float, y: float) -> bool:
        """
        Given an (x,y) coordinate, determines if that coordinate is within range of this node.
        """
        return ((x - self.x) ** 2 + (y - self.y) ** 2) ** 0.5 <= self.transmit_distance

    def get_queue_state(self) -> list[Packet]:
        """
        Returns an ordered list of packets, representing self's current queue.
        """
        return [p[0] for p in self.queue]

    def get_packets_received(self) -> int:
        """
        Returns the number of packets that this node has received
        """
        return self.received_packets

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

    def get_neighbors(self) -> list['Node']:
        """
        Return a list of nodes we are connected to.
        """
        return list(self.links.keys())

    def get_probability(self, neighbor: str) -> float:
        if not neighbor in self.links:
            return 0

        return self.links[neighbor].get_probability()

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
