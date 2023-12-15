from mesh.arena import Arena
from mesh.packet import Packet


def test_parse() -> None:
    """
    Tests parsing of a simple one-node arena
    """
    arena = Arena("./test_mesh/test_arenas/basic.json")
    assert 'n1' in arena.get_nodes(), "expected 'n1' to be part of the arena"
    return


def test_two_nodes() -> None:
    """
    Tests a two-node network where the nodes should be linked.
    """
    arena = Arena("./test_mesh/test_arenas/two-nodes.json")
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

    arena.run(override=True)

    assert len(n1.get_queue_state()
               ) == 0, 'n1 should have sent and thus have no packets'

    for _ in range(5):
        arena.run()

    assert len(n2.get_queue_state(
    )) == 1, 'If this check is failing it is because I am imagining n2 instantly getting a response for n1'

    arena.run(override=True)
    assert n1.get_packets_received() == 1, 'n1 should have gotten 1 packet'

    return


def test_generating_links() -> None:
    """
    Tests all of the partitions of whether a link will be established between two nodes.
    """
    arena = Arena('./test_mesh/test_arenas/all-link-partitions.json')
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
    arena = Arena('./test_mesh/test_arenas/dfs.json')
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

    arena.run(override=True)
    for n in ['n11', 'n21']:
        assert len(node_mapping[n].get_queue_state()
                   ) == 1, n + ' should have one packet in queue after one timestep'


def test_collision() -> None:
    """
    Tests collision behavior
    """
    arena = Arena("./test_mesh/test_arenas/collision.json")
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

    if len(n1.get_queue_state()) == 2:
        assert n1.get_queue_state()[
            0] == n1_first, 'expected to the same packet to be at the head of n1\'s queue'
        assert len(n3.get_queue_state()
                   ) == 0, 'if n1 didn\'t send, then n3 should have sent'
    elif len(n3.get_queue_state()) == 1:
        assert n3.get_queue_state()[
            0] == n3_first, 'expected to the same packet to be at the head of n3\'s queue'
        assert len(n1.get_queue_state()) == 1, 'n1 should have sent a packet'
    else:
        raise AssertionError('neither queue sent anything')

    arena.run()
    n2 = node_mapping['n2']
    assert len(n2.get_queue_state()) == 1, 'n2 should have gotten a packet'
    assert n2.get_queue_state()[0] == n1_first.get_reverse() or n2.get_queue_state()[
        0] == n3_first.get_reverse(), 'packet that n2 got should be one of the two that n1 or n3 sent for the reverse direction'
    return


def test_hidden_terminal() -> None:
    """
    Tests hidden terminal behavior
    """
    arena = Arena("./test_mesh/test_arenas/hidden-terminal.json")
    node_mapping = arena.get_nodes()
    for i in range(1, 4):
        n = 'n' + str(i)
        assert n in node_mapping, 'expected ' + n + ' to be in node_mapping'

    n1, n3 = node_mapping['n1'], node_mapping['n3']

    arena.send_packet('n1', 'n2')
    arena.send_packet('n1', 'n2')
    arena.send_packet('n3', 'n2')
    # should have a hidden terminal instance occur, so no queues are changed
    arena.run(override=True)

    assert len(n1.get_queue_state()
               ) == 1, 'expected length of n1\'s queue to be 1'
    assert len(n3.get_queue_state()
               ) == 0, 'expected length of n3\'s queue to be 0'
    n2 = node_mapping['n2']
    assert len(n2.get_queue_state()) == 0, 'n2 should not have gotten a packet'
    return


def test_priority_nodes() -> None:
    """
    Tests that arena is properly assuring fairness
    """
    arena = Arena("./test_mesh/test_arenas/cycles-priority-nodes.json")
    node_mapping = arena.get_nodes()
    for i in range(1, 4):
        n = 'n' + str(i)
        assert n in node_mapping, 'expected ' + n + ' to be in node_mapping'
    assert len(node_mapping) == 3, 'expected only four nodes in mapping'

    arena.send_packet('n1', 'n3', False)
    arena.send_packet('n1', 'n3', False)
    arena.send_packet('n2', 'n3', False)
    arena.send_packet('n2', 'n3', False)

    arena.run(override=True)
    arena.run(override=True)

    for n in ['n1', 'n2']:
        assert len(node_mapping[n].get_queue_state()
                   ) == 1, 'each node should have sent once'


def test_packet() -> None:
    """
    Tests that packet objects and helper methods work.
    """
    packet_id = 300
    path = [str(i) for i in range(100)]
    packet = Packet(True, path, packet_id)
    assert packet.get_path() == path, "packet path is wrong"
    assert packet.get_is_request() == True, "packet should be a request"
    assert packet.get_id() == packet_id, "Packet_id is wrong"
    assert packet.get_reverse() == Packet(
        False, [str(i) for i in range(99, -1, -1)], packet_id
    )
    return


def test_links() -> None:
    """
    Tests some link probabilities based on how far they are.  
    """
    return

def test_sim_collision() -> None:
    """
    Test simulation and metrics getting for the collision example.
    """
    arena = Arena("./test_mesh/test_arenas/collision.json")
    metrics = arena.simulate(100, 'type1', 'type3', probability_send=0.1)
    n1_metrics = metrics['n1']

    assert n1_metrics['successes'] > 0
    assert n1_metrics['average_latency'] > 1
    assert n1_metrics['throughput'] <= 1 and n1_metrics['throughput'] >= 0

def test_sim_hidden_terminals() -> None:
    """
    Test simulation and metrics getting for the hidden terminals example.
    """
    arena = Arena("./test_mesh/test_arenas/hidden-terminal.json")

    metrics = arena.simulate(100, 'type1', 'type1', probability_send=0.1)

    for _, node in metrics.items():
        assert node['average_latency'] > 1
        assert node['throughput'] <= 1 and node['throughput'] >= 0
        assert node['drops'] > 0