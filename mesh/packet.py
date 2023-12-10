import typing


class Packet:

    def __init__(self, payload_size: int, packet_id: int, is_request: bool, path_to_dst: typing.List[str]) -> None:
        """
        Creates a packet given a path to the destination MAC address and a packet size in bytes.

        Each packet also has packet_id, and notes whether it is a request for the destination or a response from the destination.
        """
        pass

    def get_path(self) -> list[str]:
        """
        Gets the packet's path to destination.
        """
        return []

    def get_is_request(self) -> bool:
        """
        Returns True iff the packet is a request packet.
        """
        return False
