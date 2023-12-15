from .packet import Packet, COPEPacket, ReceptionReport
from .link import Link

class Node:

    def __init__(self, mac_address: str, x: float, y: float, hierarchy_class: str, transmit_distance: float, response_wait_time: int, packet_pool_expiration: float) -> None:
        """
        Creates a node object
        """
        self.mac_address = mac_address
        self.x, self.y = x, y
        self.hierarchy_class: str = hierarchy_class
        self.transmit_distance: float = transmit_distance
        self.response_wait_time: int = response_wait_time

        self.links: dict[str, Link] = {}
        self.queues: dict[str, list[tuple[Packet, int]]] = {}
        self.waiting_for_response: dict[int, Packet] = {}
        self.packet_pool: dict[tuple[str, bool], int] = {}
        self.neighbor_state: dict[str, set[tuple[int, bool]]] = {}
        self.packet_pool_expiration: int = packet_pool_expiration

        self.sent: dict[int, int] = {}
        self.received: dict[int, int] = {}
        self.received_packets: int = 0
        self.coded_packets_history: list[tuple[list[int], int]] = []

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

    def enqueue_packet(self, packet: Packet, timestep: int) -> None:
        """
        Enqueues the given packet.

        If self is destination of packet, check if self sent packet with this packet id. 
            If yes, we are done. If no, enqueue a response packet and send back to original src.
        """
        # we are the final destination of a response
        if packet.get_id() in self.sent or (not packet.get_is_request() and packet.get_path()[-1] == self.get_mac()):
            self.received[packet.get_id()] = timestep
            self.received_packets += 1
            return
        # we are initiating a send
        elif packet.get_is_request() and packet.get_path()[0] == self.get_mac():
            self.packet_pool[(
                packet.get_id(), packet.get_is_request())] = timestep
            self.sent[packet.get_id()] = timestep
            self.queues[packet.get_path()[1]].append((packet, timestep))
        # we are the final destination of a request
        elif packet.get_is_request() and packet.get_path()[-1] == self.get_mac():
            self.waiting_for_response[timestep +
                                      self.response_wait_time] = packet.get_reverse()
        # we are engaging in promiscuous listening
        elif self.get_mac() not in packet.get_path():
            pass
        # we are a node on the path
        else:
            path = packet.get_path()
            nexthop = path[path.index(self.mac_address) + 1]
            self.queues[nexthop].append((packet, timestep))
        # should always be putting a packet that we enqueue into our pool
        self.packet_pool[(packet.get_id(), packet.get_is_request())] = timestep
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
            if (packet.get_id(), packet.get_is_request()) not in self.packet_pool and new_packet is None:
                new_packet = packet
            elif (packet.get_id(), packet.get_is_request()) not in self.packet_pool and new_packet is not None:  # Too many unknown packets
                return

        # we have already seen all packets encoded here
        if new_packet is None:
            return

        self.packet_pool[(new_packet.get_id(),
                          new_packet.get_is_request())] = timestep
        self.enqueue_packet(new_packet, timestep)
        return

    def cleanup(self, timestep: int) -> None:
        """
        Cleans up hidden terminal collisions for nodes in promiscuous mode
        """
        if list(self.packet_pool.values()).count(timestep) > 1:
            self.packet_pool = {p: t for p, t in self.packet_pool.items() if t != timestep}
        
        self.packet_pool = {p: t for p, t in self.packet_pool.items() if timestep - t < self.packet_pool_expiration}
        return

    def receive_reception_report(self, report: ReceptionReport) -> None:
        """
        Updates self's state based on the reception report
        """
        node = report.get_node()
        packets = report.get_packets()
        self.neighbor_state[node] = set(packets)
        return

    def learn_timestep(self, timestep: int) -> None:
        """
        Tells this node the timestep that the arena is currently on. Updates the queue if it should 
        """
        if timestep not in self.waiting_for_response:
            return

        response_packet = self.waiting_for_response.pop(timestep)
        path = response_packet.get_path()
        self.packet_pool[(response_packet.get_id(),
                          response_packet.get_is_request())] = timestep
        self.queues[path[1]].append((response_packet, timestep))
        return

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
            if neighbor not in nexthops:
                if q and all((p.get_id(), p.get_is_request()) in self.neighbor_state[neighbor] for p in packets):
                    print("ayo")
                    packets.append(q.pop(0)[0])
                    nexthops.append(neighbor)

        for neighbor in nexthops:  # this ensures fairness, so we are not just encoding the same people
            self.neighbor_state[neighbor] = self.neighbor_state.pop(neighbor)

        cope_packet = COPEPacket(packets, ReceptionReport(
            set(self.packet_pool), self.mac_address))

        self.coded_packets_history.append(
            ([packet.get_id() for packet in packets], timestep))

        for nexthop in self.links:
            self.links[nexthop].transmit(
                cope_packet, self.mac_address, timestep, override)

        return

    def send_reception_report(self, timestep: int, override: bool) -> None:
        """
        Node sends a reception report to all its neighbors
        """
        report = ReceptionReport(
            set(p for p in self.packet_pool), self.mac_address)
        for _, link in self.links.items():
            link.transmit_reception_report(
                report, self.mac_address, timestep, override)
        return

    def is_linked(self, other: str) -> bool:
        """
        Given the MAC address of another node, returns True iff there is a link between self and other.
        """
        return other in self.links

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
        """
        Return the probability that a transmission to a neighbor will succeed.
        """
        if not neighbor in self.links:
            return 0

        return self.links[neighbor].get_probability()

    def get_packet_pool(self) -> set[int]:
        """
        Returns the packet pool of self
        """
        return self.packet_pool

    def get_sent(self) -> dict[str, str]:
        """
        Return a dictionary of packets sent by this node and their timesteps
        """
        return {k: v for k, v in self.sent.items()}

    def get_received(self) -> dict[str, str]:
        """
        Return a dictionary of packets received by this node and their timesteps
        """
        return {k: v for k, v in self.received.items()}

    def get_coded_packets_history(self) -> list[tuple[list[int], int]]:
        """
        Return the packet coding history for this node. 
        """
        return [(entry[0][:], entry[1]) for entry in self.coded_packets_history]

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
