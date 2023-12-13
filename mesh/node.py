import typing

from .packet import Packet
from .link import Link


class Node:

    def __init__(self, mac_address: str, x: float, y: float, hierarchy_class: str, transmit_distance: float, response_wait_time: int, storage_size: float) -> None:
        """
        Creates a node object
        """
        self.mac_address: str = mac_address
        self.x: float = x
        self.y: float = y
        self.hierarchy_class: str = hierarchy_class
        self.transmit_distance: float = transmit_distance
        self.response_wait_time: int = response_wait_time
        self.storage_size: float = storage_size

        self.links: dict[str, Link] = {}

        self.queue: list[tuple[Packet, int]] = []
        self.sent = set()
        self.waiting_for_response: dict[int, Packet] = {}
        self.received_packets = 0

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

    def enqueue_packet(self, packet: Packet, timestep: int) -> None:
        """
        Enqueues the given packet.

        If self is destination of packet, check if self sent packet with this packet id. 
            If yes, we are done. If no, enqueue a response packet and send back to original src.
        """
        if packet.get_id() in self.sent or (not packet.get_is_request() and packet.get_path()[-1] == self.get_mac()):
            # TODO: add in metrics here
            self.received_packets += 1
            return
        elif packet.get_is_request() and packet.get_path()[0] == self.get_mac():
            self.sent.add(packet.get_id())
            self.queue.append((packet, timestep))
        elif packet.get_is_request() and packet.get_path()[-1] == self.get_mac():
            self.waiting_for_response[timestep +
                                      self.response_wait_time] = packet.get_reverse()
        else:
            self.queue.append((packet, timestep))
        return

    def learn_timestep(self, timestep: int) -> None:
        """
        Tells this node the timestep that the arena is currently on. Updates the queue if it should
        """
        if timestep not in self.waiting_for_response:
            return

        response_packet = self.waiting_for_response.pop(timestep)
        self.queue.append((response_packet, timestep))
        return

    def get_next_destination(self) -> str or None:
        """
        Returns the MAC address of the nexthop of the packet at the front of the queue.
        """
        next_packet = self.queue[0][0]
        packet_path = next_packet.get_path()
        return packet_path[packet_path.index(self.mac_address) + 1]

    def send_from_queue(self, timestep: int, hidden_terminal: bool, override: bool) -> Packet:
        """
        Dequeues the next packet and sends the packet to its next hop. 

        If override, packet will always complete except if it's a hidden terminal
        """
        nexthop = self.get_next_destination()
        packet = self.queue.pop(0)[0]
        if hidden_terminal:
            return packet
        self.links[nexthop].transmit(
            packet, self.mac_address, timestep, override)
        return packet

    # Testing

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
