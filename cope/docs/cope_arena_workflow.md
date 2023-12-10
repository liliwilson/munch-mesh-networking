# COPE Arena Workflow

## Initializing the arena

This is going to be the same as in [`/mesh/docs/arena_workflow.py`](../../mesh/docs/arena_workflow.md), except we will also want to initialize nodes with a packet pool time limit.

## Running a simulation.

Before we can begin simulating, we need to set up the arena given an input text file. This input text file should contain the arena size, a list of nodes and their locations and types, a mapping of node types to their specs (e.g. power output, storage), and a set of rules for which types of nodes are allowed to send and receive traffic directly from one another.

1. Instantiate nodes at their different locations.
2. Make links between the nodes:

    a. $\forall$ pairs of nodes, check if a link can be created between them (by checking classes against the hierarchy class)

    b. If we can make a link, instantiate the link. The link objects will handle determining if transmission probabilty is > 0 based on the power of transmission of its end nodes.

3. Perform DFS from supernodes to determine the ideal paths for each node, using information from links about probability of transmission.

4. Update every node using `set_path` to store the path from that node to the supernode.

## Running a simulation

Given a number `timesteps`, simulate the network running for that many timesteps. The simulation will operate under the assumption that we have an `end_user_hierarchy_class` and an `internet_access_hierarchy_class`, where the end users typically generate _request_ packets to send to the internet whose destination is a node with internet access (which in turn will generate a _response_).

In this model, we use the arena to implement a simpler version of the MAC protocol, as well as help manage our COPE protocol to determine which nodes can send at any given point in time.

At each timestep, the following will take place:

1. The arena cycles through its list of active nodes to find nodes that are ready to send. For each node in the list:

    a. Check if that node has a packet in its queue that it is ready to send. Instead of just taking the next packet in the queue, a node will look to encode as many packets as possible. If no packets are available, it will try to send a reception report.

    b. If there is a packet to send, we need to check if the medium in that node's area is already being used that timestep. We do this by checking if the range of this node overlaps with any nodes that are currently in the senders list.

    c. If the current node detects another sender in its area, do not send this time and continue back to (a) for the next node in the list. Otherwise, add this node to the list of senders. Continue back to (a).

2. Given a list of senders and COPEPackets, each sender will aim to send to _everyone_ they can reach (this is to represent braodcast). 

3. The arena will determine if any collisions would happen were the packets to be sent by looping through the senders and checking if any of them have the same destination node. It will also do this check amongst the reception reports (which are sent via a different channel and thus checked separately) This is to represent the "hidden terminals" problem we often see in wireless networks. The paper notes that hidden terminals become a big issue here, and specifically engineered their network to have no hidden terminals to avoid these problems. We plan to investigate this here.

4. In the case of a collision, all nodes involved in that collision get moved to the back of the list of nodes and wait some random amount of timesteps before trying to send again.

5. All remaining un-collided senders will then be triggered to send their enqueued packet to its nexthop, determined using a minimum-path routing protocol with the DFS results from the beginning. These senders will also all be moved to the back of the arena's node list, to try to enforce some of the MAC fairness that the protocol normally manages.

We also need some way to make sure that senders generate_packets to a random receiver at different timesteps. We plan to incorporate some randomness here to decide when to randomly generate a packet.

### Metrics from arena

After concluding the main simulation loop, we will return the metrics described in [`metrics.md`](../../docs/metrics.md) as a dictionary.
