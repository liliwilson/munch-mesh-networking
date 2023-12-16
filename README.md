<div align="center">

  <h1 align="center">MUNCH</h1>
    <p align="center"><i>Network coding for wireless community networks</i></p>
  <p align="center">
Lili Wilson and Sean Cheng    <br />
    6.185, Fall 2023
    <br />
  </p>
</div>

## Overview
MUNCH is a practical implementation of network coding inteded for use in wireless mesh community networks. MUNCH aims to leverage network coding to improve throughput for mesh networks, and is based largely off of the [COPE opportunistic network coding](http://nms.csail.mit.edu/~sachin/papers/copesc.pdf) system proposed in 2006. 

In addition to providing an implementation of MUNCH, this repository contains code for simulating wireless mesh netwoks with and without network coding implemented. While we only investigate throughput at latency for our initial project and only look at four main topologies, we believe that this platform has potential to facilitate more extensive research into network coding implementations and potential use under different network circumstances. See [future work](https://github.com/liliwilson/munch-mesh-networking?tab=readme-ov-file#future-work) below for a more detailed breakdown of ideas we have for the simulator. 

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

## Documentation
To explore the full documentation for each network type, you can find the mesh network docs [here](https://liliwilson.github.io/munch-mesh-networking/html/mesh) and COPE network coding network docs [here](https://liliwilson.github.io/munch-mesh-networking/html/cope).

## Running a simulation
Example code for running a simulation can be found in [`run_simulate.py`](./run_simulate.py). To run a simulation, you must provide a JSON file detailing the structure of the network, including which different node classes there are (e.g. supernode, hub node, user node), what the transmission ranges of each type of node are, where each node lies, and which classes of node are able to connect to one another. See [`topologies/alice_and_bob.json`](topologies/alice_and_bob.json) for a simpler example of recommended structure, and [`topologies/nycmesh.json`](topologies/nycmesh.json) for a more complicated example at scale. 

You can then input your topology file name at the top of `run_simulate` and define a CopeArena and MeshArena to test your network in. To test a network, call `arena.simulate()`, with the number of timesteps to have nodes send messages for, a sending node class, a receiving node class, and optionally a min and max datastream size as well as the probability that a given node will send a message at any timestep. This function will return a dictionary of per-node metrics, which can then be aggregated using the `aggregate_metrics` function and saved to `./simulation_results/{topology_name}`. This function can be modified to look at different metrics given the per-node metrics, for example, fairness. 

## Modifying simulation architecture
Both the [mesh](https://liliwilson.github.io/munch-mesh-networking/html/mesh) and [COPE](https://liliwilson.github.io/munch-mesh-networking/html/cope) simulation architecture consist of four primary classes: an `Arena`, a `Node`, a `Link`, and a `Packet`. The `Arena` class maintains overall network state, steps through timesteps and manages node traffic flow, enforces bandwidth allocation, and handles hidden terminal collisions. The `Node` class handles packet queueing and sending, packet coding for the COPE case, and gathering its own metrics. The `Link` class handles transmission between nodes, taking into account probability of a packet drop along a link based on the distances between the two nodes and their respective transmission strengths. Finally, the `Packet` class is used by COPE to add packet headers and reception reports to messages.

Modifications to each system can be studied by modifying behavior in any of the classes above. To run the test cases on the two networks, and ensure that nothing is broken before evaluating a simulation, run 
```
pytest *tests.py
``` 
in the root directory of the project. You should see all test cases passing. 

## Future work
While the simulation indicated that based on throughput and latency, MUNCH does not seem very promising for the wireless community network setting, we are excited about the potential of this simulation architecture to be used in further study of network coding. In future, we would like to make the future additions to this project:

* Use metrics to investigate fairness in different network topologies
    * Look at ratios of throughput and latency amongst different users, compare with distance from a supernode or hub node
* Investigate more complex traffic flows, making use of the (min data stream, max data stream) parameters that our simulator is capable of handling.
    * Look further at how many flows get fully completed, and what the time in between receiving packets in the flows is. Is there jitter?
* Look at energy consumption and storage of each network, adding in a per-node calculation that watches storage space used and energy per computation at that node
* Further optimize our code for the COPE network coding implementation, as it is currently very slow to run the same number of timesteps in this simulation compared to the normal mesh one
