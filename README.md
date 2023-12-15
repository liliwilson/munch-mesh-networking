# MUNCH
MUNCH is a practical implementation of network coding inteded for use in wireless mesh community networks. MUNCH aims to leverage network coding to improve throughput for mesh networks, and is based largely off of the [COPE opportunistic network coding](http://nms.csail.mit.edu/~sachin/papers/copesc.pdf) system proposed in 2006. 

In addition to providing an implementation of MUNCH, this repository contains code for simulating wireless mesh netwoks with and without network coding implemented. While we only investigate throughput at latency for our initial project and only look at four main topologies, we believe that this platform has potential to facilitate more extensive research into network coding implementations and potential use under different network circumstances. See future work below for a more detailed breakdown of ideas we have for the simulator. 

<p align='center'>

<img width="400" alt="nycmesh" src="https://github.com/liliwilson/munch-mesh-networking/assets/56806227/d515b2de-b4cd-4f0a-80d9-b4f4eb1089b6">

</p>

<p align='center'> <a href="https://www.nycmesh.net">NYCMesh</a> community wireless network </p>


## Project structure
The [`cope`](./cope) and [`mesh`](./mesh) directories contain the simulation structure for MUNCH and normal wireless mesh networks respectively. A simulation is managed by an instance of the Arena class, which handles initializing a topology from a JSON file, managing network traffic flows, stepping through timesteps in a simulation, and gathering metrics. The high level arena workflow for each network type can be found in `{network}/docs/{network}_arena_workflow.md`.

The [`test_cope`](./test_cope) and [`test_mesh`](./test_mesh) directories contain test cases and test topology that were used to verify that the simulators were working as expected. You can find all of the test cases within `tests.py` and the test arenas in the `test_arenas` subdirectory of each testing folder.

The code for running a simulation and aggregating metrics lies in [`run_simulate.py`](./run_simulate.py). We explain below how to set up a simulation. 

All test topologies used for simulating can be found in [`./topologies`](./topologies). The code for generating the NYCMesh network topology can be found here in [`nyc_mesh_parse.py`](./topologies/nyc_mesh_parse.py), drawing data from [`nycmesh_map_data`](./topologies/nycmesh_map_data/). 


Here is a more visual breakdown of the project structure:
```
├── README.md
├── cope
│   ├── arena.py
│   ├── docs
│   │   ├── assumptions.md
│   │   └── cope_arena_workflow.md
│   ├── link.py
│   ├── node.py
│   └── packet.py
├── docs
│   └── metrics.md
├── mesh
│   ├── arena.py
│   ├── docs
│   │   ├── arena_workflow.md
│   │   └── assumptions.md
│   ├── link.py
│   ├── node.py
│   └── packet.py
├── requirements.txt
├── run_simulate.py
├── test_cope
│   ├── test_arenas
│   │   ├── alice_and_bob.json
│   │   ├── all-link-partitions.json
│   │   ├── basic.json
│   │   ├── collision.json
│   │   ├── cycles-priority-nodes.json
│   │   ├── dfs.json
│   │   ├── hidden-terminal.json
│   │   └── wheel-top.json
│   └── tests.py
├── test_mesh
│   ├── test_arenas
│   │   ├── all-link-partitions.json
│   │   ├── basic.json
│   │   ├── collision.json
│   │   ├── cycles-priority-nodes.json
│   │   ├── dfs.json
│   │   ├── hidden-terminal.json
│   │   └── two-nodes.json
│   ├── testing_strategy.md
│   └── tests.py
└── topologies
    ├── README.md
    ├── alice_and_bob.json
    ├── cope_setup.json
    ├── images
    │   └── cope_node_map.jpeg
    ├── nyc_mesh_parse.py
    ├── nycmesh.json
    ├── nycmesh_map_data
    │   ├── links.json
    │   └── nodes.json
    └── wheel-top.json
```

## Running a simulation
Example code for running a simulation can be found in [`run_simulate.py`](./run_simulate.py). To run a simulation, you must provide a JSON file detailing the structure of the network, including which different node classes there are (e.g. supernode, hub node, user node), what the transmission ranges of each type of node are, where each node lies, and which classes of node are able to connect to one another. See [`topologies/alice_and_bob.json`](topologies/alice_and_bob.json) for a simpler example of recommended structure, and [`topologies/nycmesh.json`](topologies/nycmesh.json) for a much more complicated example at scale. 



## Modifying simulation architecture
* test files


## Future work
- sanity check simulations
- use metrics to investigate fairness
- add in TCP support
- diff traffic flows, data streams
