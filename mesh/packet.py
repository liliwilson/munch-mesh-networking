class Packet:

    def __init__(self, payload_size: int, packet_id: int, is_request: bool, path_to_dst: list[str]) -> None:
        """
        Creates a packet given a path to the destination MAC address and a packet size in bytes.

        Each packet also has packet_id, and notes whether it is a request for the destination or a response from the destination.
        """
        self.payload_size = payload_size
        self.packet_id = packet_id
        self.is_request = is_request
        self.path_to_dst = path_to_dst
        return

    def get_path(self) -> list[str]:
        """
        Gets the packet's path to destination.
        """
        return self.path_to_dst

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
