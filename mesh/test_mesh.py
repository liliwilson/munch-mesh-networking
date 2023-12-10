from mesh.arena import Arena


def test_parse() -> None:
    """
    Tests parsing of a simple one-node arena
    """
    arena = Arena("./testing_auxiliaries/test_arenas/basic.json")
    assert 'n1' in arena.get_nodes(), "expected 'n1' to be part of the arena"
    return


def test_two_nodes() -> None:
    """
    Tests a two-node network where the nodes should be linked.
    """
    arena = Arena("./testing_auxiliaries/test_arenas/two-nodes.json")
    node_mapping = arena.get_nodes()
    assert 'n1' in node_mapping and 'n2' in node_mapping, "Wrong nodes in network"

    # tests for links

    links = [('n1', 'n2')]
    for node1, node2 in links:
        assert arena.can_link(node1, node2), node1 + \
            ' and ' + node2 + ' should be linked'
        assert arena.can_link(node2, node1), node2 + \
            ' and ' + node1 + ' should be linked'

    # initiates a packet sending request

    arena.send_packet('n1', 'n2')
    n1 = node_mapping['n1']
    n2 = node_mapping['n2']
    assert len(n1.get_queue_state()) == 1, 'n1 should have one packet in queue'
    packet = n1.get_queue_state()[0]
    assert packet.get_is_request(), 'packet should be a request packet'

    arena.run()  # TODO: change this to have the parameters required
    assert n2.get_packets_received() == 1, 'n2 should have received a packet'

    # TODO: Check if this is correct (read the error message)
    assert len(n2.get_queue_state(
    )) == 1, 'If this check is failing it is because I am imagining n2 instantly getting a response for n1'

    arena.run()  # TODO: change this to have the parameters required

    return
