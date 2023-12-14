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

        self.queues: dict[str, list[tuple[Packet, int]]] = {}
        self.sent = {}
        self.waiting_for_response: dict[int, Packet] = {}
        self.received = {}
        self.received_packets = 0
        self.packet_pool = {}
        self.neighbor_state: dict[str, set[int]] = {}

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
            self.queues[other.get_mac()] = []
            self.neighbor_state[other.get_mac()] = set()
        return

    def set_path(self, path: list[str]) -> None:
        """
        Sets the MAC address path from self to the supernode.
        """
        pass

    def enqueue_packet(self, packet: Packet, timestep: int) -> None:
        """
        TODO: needs to be changed to deal with one queue for each neighbor
        Enqueues the given packet.

        If self is destination of packet, check if self sent packet with this packet id. 
            If yes, we are done. If no, enqueue a response packet and send back to original src.
        """
        if packet.get_id() in self.sent or (not packet.get_is_request() and packet.get_path()[-1] == self.get_mac()):
            # final reciever
            self.received[packet.get_id()] = timestep
            self.received_packets += 1
            return
        # initiating a send
        elif packet.get_is_request() and packet.get_path()[0] == self.get_mac():
            self.sent[packet.get_id()] = timestep
            self.queues[packet.get_path()[1]].append((packet, timestep))
        elif packet.get_is_request() and packet.get_path()[-1] == self.get_mac():
            # need to create a response
            self.waiting_for_response[timestep +
                                      self.response_wait_time] = packet.get_reverse()
        elif self.get_mac() not in packet.get_path():
            # we are sus
            pass
        else:
            # on the path
            path = packet.get_path()
            nexthop = path[path.index(self.mac_address) + 1]
            self.queues[nexthop].append((packet, timestep))
        # should always be putting a packet that we enqueue into our pool
        self.packet_pool[packet.get_id()] = timestep
        return

    def receive_cope_packet(self, cope_packet: COPEPacket, timestep: int) -> None:
        """
        Lets the given node receive a COPEPacket
        """
        reception_report = cope_packet.get_reception_report()
        self.receive_reception_report(reception_report)

        packets = cope_packet.get_packets()
        new_packet = None
        for packet in packets:
            if packet.get_id() not in self.packet_pool and new_packet is None:
                new_packet = packet
            elif new_packet is not None:  # Too many unknown packets
                return

        self.packet_pool[new_packet.get_id()] = timestep
        self.enqueue_packet(new_packet, timestep)

        return

    def receive_reception_report(self, report: ReceptionReport) -> None:
        """
        Updates self's state based on the reception report
        """
        node = report.get_node()
        packets = report.get_packets()
        self.neighbor_state[node].union(packets)
        return

    def learn_timestep(self, timestep: int) -> None:
        """
        Tells this node the timestep that the arena is currently on. Updates the queue if it should 
        """
        pass

    def get_next_destination(self) -> str:
        """
        Returns the MAC address of the nexthop of the packets that will be sent next.
        """
        smallest = float('inf')
        nexthop = None
        for neighbor, queue in self.queues.items():
            if not queue:
                continue
            elif queue[0][1] < smallest:
                nexthop = neighbor
                smallest = queue[0][1]

        return nexthop

    def send_from_queues(self, timestep: int, hidden_terminal: bool, override: bool) -> None:
        """
        Look for an encoding opportunity amongst the heads of our neighbor queues.

        Dequeues the next packet(s), creates a COPEPacket object, and sends the packet to its next hops. 
        """
        nexthops = [self.get_next_destination()]
        packets = [self.queues[nexthops[0]].pop(0)[0]]
        if hidden_terminal:
            return

        for neighbor, q in self.queues.items():  # adds all packets to the copepacket
            if all(p.get_id() in self.neighbor_state[neighbor] for p in packets):
                packets.append(q.pop(0)[0])
                nexthops.append(neighbor)

        for neighbor in nexthops:  # this ensures fairness, so we are not just encoding the same people
            self.neighbor_state[neighbor] = self.neighbor_state.pop(neighbor)

        cope_packet = COPEPacket(packets, ReceptionReport(
            set(self.packet_pool), self.mac_address))

        for nexthop in self.links:
            self.links[nexthop].transmit(
                cope_packet, self.mac_address, timestep, override)

        return

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

    def get_queue_state(self, neighbor: str) -> list[Packet]:
        """
        Returns an ordered list of packets, representing self's current queue.
        """
        assert neighbor in self.queues, 'cannot get queues of node that is not neighbor'
        return [p for p, _ in self.queues[neighbor]]

    def get_all_queues(self) -> dict[str, list[tuple[Packet, int]]]:
        """
        Returns the state of all queues of self
        """
        return {k: v[:] for k, v in self.queues.items()}

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

    def get_packet_pool(self) -> set[int]:
        """
        Returns the packet pool of self
        """
        return self.packet_pool

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
