from typing import Any

class Packet:
    num_packets = 0

    def __init__(self, is_request: bool, path_to_dst: list[str], packet_id: int = None) -> None:
        """
        Creates a packet given a path to the destination MAC address and a packet size in bytes.

        Each packet also has packet_id, and notes whether it is a request for the destination or a response from the destination.

        If no packet id supplied, sets to be the next packet id.
        """
        self.is_request = is_request
        self.path_to_dst = path_to_dst[:]
        if packet_id is not None:
            self.packet_id = packet_id
        else:
            self.packet_id = Packet.num_packets
            Packet.num_packets += 1

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
        return Packet(False, self.path_to_dst[::-1], self.packet_id)

    def __eq__(self, other: Any) -> bool:
        """
        Returns True iff two packets are equal
        """
        if not isinstance(other, Packet):
            return False
        if not self.packet_id == other.packet_id:
            return False
        if not self.is_request == other.is_request:
            return False
        if not self.path_to_dst == other.path_to_dst:
            return False
        return True
