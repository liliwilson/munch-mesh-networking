import typing
from .packet import COPEPacket, ReceptionReport

class Node:

    def __init__(self, mac_address: str, x: float, y: float, hierarchy_class: str, transmit_distance: float, storage_size: float) -> None:
        """
        Creates a node object
        """
        pass

    def add_link(self, other: "Node") -> None:
        """
        Adds a link from self to other and creates a queue for that neighbor in self.
        """
        pass

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

    def send_from_queue(self, timestep: int) -> None: 
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