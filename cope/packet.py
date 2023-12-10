import typing

class Packet:

    def __init__(self, payload_size: int, packet_id: int, is_request: bool, path_to_dst: typing.List[str]) -> None:
        """
        Creates a packet given a path to the destination MAC address and a packet size in bytes.

        Each packet also has packet_id, and notes whether it is a request for the destination or a response from the destination.
        """
        pass


class ReceptionReport:

    def __init__(self, stored_packets: typing.List[int], node: str):
        """
        Create a reception report for a given node, given a list of packet IDs it has stored.
        """
        pass

class COPEPacket:

    def __init__(self, packets: typing.List[Packet], reception_report: ReceptionReport):
        """
        Creates a COPE packet, which encodes together a list of given packets and attaches a given reception report containing stored packet IDs for a node.
        """
        pass