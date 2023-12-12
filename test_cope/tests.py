from cope.arena import Arena
from cope.packet import Packet


def test_parse() -> None:
    """
    Tests parsing of a simple one-node arena
    """
    arena = Arena("./test_cope/test_arenas/basic.json")
    assert 'n1' in arena.get_nodes(), "expected 'n1' to be part of the arena"
    return


def test_wheel_top() -> None:
    """
    Tests a wheel topology network where the nodes should be linked.
    """
    arena = Arena("./test_cope/test_arenas/wheet-top.json")
    node_mapping = arena.get_nodes()
    for n in ['n1', 'n2', 'n3', 'n4', 'n5']:
        assert n in node_mapping, "Wrong nodes in network"

    # tests for links

    links = [
        ('n1', 'n2'),
        ('n1', 'n3'),
        ('n1', 'n4'),
        ('n1', 'n5')
    ]
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

    arena.run()

    # TODO: what happens to the true receiver
    for n in ['n2', 'n3', 'n4', 'n5']:
        assert len(node_mapping[n].get_queue_state(
        )) == 1, 'all nodes should have received a packet'

    arena.run()  # TODO: change this to have the parameters required

    return


def test_generating_links() -> None:
    """
    Tests all of the partitions of whether a link will be established between two nodes.
    """
    arena = Arena('./test_cope/test_arenas/all-link-partitions.json')
    node_mapping = arena.get_nodes()
    for n in ['n1', 'n2', 'n3', 'n4']:
        assert n in node_mapping, 'expected ' + n + ' to be in node_mapping'

    links = [('n1', 'n2')]
    for node1, node2 in links:
        assert arena.can_link(node1, node2), node1 + \
            ' and ' + node2 + ' should be linked'
        assert arena.can_link(node2, node1), node2 + \
            ' and ' + node1 + ' should be linked'

    no_links = [('n1', 'n3'), ('n1', 'n4'), ('n2', 'n3'),
                ('n2', 'n4'), ('n3', 'n4')]
    for node1, node2 in no_links:
        assert not arena.can_link(node1, node2), node1 + \
            ' and ' + node2 + ' should not be linked'
        assert not arena.can_link(node2, node1), node2 + \
            ' and ' + node1 + ' should not be linked'

    return


def test_shortest_path() -> None:
    """
    Tests that the routing protocol is working correctly
    """
    arena = Arena('./test_cope/test_arenas/dfs.json')
    node_mapping = arena.get_nodes()
    for i in range(4):
        for j in range(4):
            n = 'n' + str(i) + str(j)
            assert n in node_mapping, 'expected ' + n + ' to be in node_mapping'

    arena.send_packet('n00', 'n33')
    n00 = node_mapping['n00']
    assert len(n00.get_queue_state()
               ) == 1, 'n00 should have one packet in queue'
    packet = n00.get_queue_state()[0]
    assert packet.get_path() == ['n00', 'n11', 'n22',
                                 'n33'], 'shortest path is wrong'

    arena.send_packet('n30', 'n03')
    n30 = node_mapping['n30']
    assert len(n30.get_queue_state()
               ) == 1, 'n30 should have one packet in queue'
    packet = n30.get_queue_state()[0]
    assert packet.get_path() == ['n30', 'n21', 'n12',
                                 'n03'], 'shortest path is wrong'

    arena.run()
    for n in ['n11', 'n01', 'n10', 'n21', 'n31', 'n20']:
        assert len(node_mapping[n].get_queue_state()
                   ) == 1, n + ' should have one packet in queue after one timestep'

    # TODO: I'm not entirely sure what to do with the other nodes that are not on the path
    # but get the packet anyway ... will test that here after we discuss though


def test_collision() -> None:
    """
    Tests collision behavior
    """
    arena = Arena("./test_cope/test_arenas/collision.json")
    node_mapping = arena.get_nodes()
    for i in range(1, 4):
        n = 'n' + str(i)
        assert n in node_mapping, 'expected ' + n + ' to be in node_mapping'

    n1, n3 = node_mapping['n1'], node_mapping['n3']

    arena.send_packet('n1', 'n2')
    arena.send_packet('n1', 'n2')
    n1_first = n1.get_queue_state()[0]
    arena.send_packet('n3', 'n2')
    n3_first = n3.get_queue_state()[0]
    arena.run()  # should have a collision, so no queues are changed

    if len(n1.get_queue_state()) == 1:
        assert len(n3.get_queue_state()
                   ) == 2, 'if n1 sent, then n3 should not have sent'
        assert n3.get_queue_state(
        )[0] == n3_first, 'makes sure the same packet is at n3\'s head'
    elif len(n3.get_queue_state()) == 0:
        assert len(n1.get_queue_state()
                   ) == 3, 'n1 should have not sent, and received a packet'
        assert n1.get_queue_state()[
            0] == n1_first, 'expected to the same packet to be at the head of n1\'s queue'
    else:
        raise AssertionError('neither queue sent anything')

    n2 = node_mapping['n2']
    assert len(n2.get_queue_state()) == 1, 'n2 should have gotten a packet'

    return


def test_hidden_terminal() -> None:
    """
    Tests hidden terminal behavior, AMPLIFY 10 TIMES
    """
    arena = Arena("./test_cope/test_arenas/hidden-terminal.json")
    node_mapping = arena.get_nodes()
    for i in range(1, 4):
        n = 'n' + str(i)
        assert n in node_mapping, 'expected ' + n + ' to be in node_mapping'

    n1, n3 = node_mapping['n1'], node_mapping['n3']

    arena.send_packet('n1', 'n2')
    arena.send_packet('n1', 'n2')
    n1_first = n1.get_queue_state()[0]
    arena.send_packet('n3', 'n2')
    n3_first = n3.get_queue_state()[0]
    arena.run()  # should have a hidden terminal instance occur, so no queues are changed

    assert len(n1.get_queue_state()
               ) == 1, 'expected length of n1\'s queue to be 1'
    assert len(n3.get_queue_state()
               ) == 0, 'expected length of n3\'s queue to be 0'
    n2 = node_mapping['n2']
    assert len(n2.get_queue_state()) == 0, 'n2 should not have gotten a packet'
    return
