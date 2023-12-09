# Our assumptions

1. Omni directional antennae with lines of sight in all directions
    * no obstructions (like walls) at the moment

2. Using UDP flows and not TCP flows
    * easier for us to implement
    * COPE paper saw most improvements with UDP flows

3. Network nodes know the topology and are stationary
    * relevant to our initial DFS and routing protocol
    * reasonable because we are using this to understand DIY networks for internet access, which generally are stationary

4. Link stability does not change over time
    * this allows our DFS results to be stable

5. Minimum-hop routing is fine

6. For two nodes, to determine link power, we take the weakest node (not assuming asymmetric connections)

7. We assume that one packet can be sent along one link in one timestep
