from mesh.arena import Arena


def test_parse() -> None:
    '''
    Tests parsing of a simple one-node arena
    '''
    arena = Arena("./testing_auxiliaries/test_arenas/basic.json")
    assert {'n1'} == arena.get_nodes()
    return
