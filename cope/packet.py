from typing import Any


class Packet:
    num_packets = 0

    def __init__(self, payload_size: int, is_request: bool, path_to_dst: list[str], packet_id: int = None) -> None:
        """
        Creates a packet given a path to the destination MAC address and a packet size in bytes.

        Each packet also has packet_id, and notes whether it is a request for the destination or a response from the destination.
        """
        if packet_id is None:
            self.packet_id = Packet.num_packets
            Packet.num_packets += 1
        else:
            self.packet_id = packet_id

        self.payload_size = payload_size
        self.is_request = is_request
        self.path_to_dst: list[str] = path_to_dst

    def get_path(self) -> list[str]:
        """
        Gets the packet's path to destination.
        """
        return self.path_to_dst[:]

    def get_is_request(self) -> bool:
        """
        Returns True iff the packet is a request packet.
        """
        return self.is_request

    def get_id(self) -> int:
        """
        Returns self's packet_id.
        """
        return self.packet_id

    def get_reverse(self) -> "Packet":
        """
        Returns a packet that is response of this packet.
        """
        assert self.is_request, 'can not get the reverse of a response packet'
        return Packet(self.payload_size, False, self.path_to_dst[::-1], self.packet_id)

    def __eq__(self, other: Any) -> bool:
        """
        Returns True iff two packets are equal
        """
        if not isinstance(other, Packet):
            return False
        if not self.payload_size == other.payload_size:
            return False
        if not self.packet_id == other.packet_id:
            return False
        if not self.is_request == other.is_request:
            return False
        if not self.path_to_dst == other.path_to_dst:
            return False
        return True


class ReceptionReport:

    def __init__(self, stored_packets: set[int], node: str):
        """
        Create a reception report for a given node, given a list of packet IDs it has stored.
        """
        self.stored_packets = stored_packets
        self.node = node

    def get_node(self) -> str:
        """
        Gets the source of this reception packet
        """
        return self.node

    def get_packets(self) -> set[int]:
        """
        Gets the packets that are self.get_node() is confirmed to have
        """
        return self.stored_packets


class COPEPacket:

    def __init__(self, packets: list[Packet], reception_report: ReceptionReport):
        """
        Creates a COPE packet, which encodes together a list of given packets and attaches a given reception report containing stored packet IDs for a node.
        """
        self.packets = packets
        self.reception_report = reception_report

    def get_packets(self) -> list[Packet]:
        """
        Returns the list of packets in the COPEPacket
        """
        return self.packets

    def get_reception_report(self) -> ReceptionReport:
        """
        Returns the reception report in this COPEPacket
        """
        return self.reception_report
