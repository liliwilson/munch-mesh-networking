# Metrics for the system

Testing all of the following for multiple topologies, both COPE and normal systems.

For a lot of these metrics, they just require individual nodes to keep track of which packets they sent at which timesteps, and when they get a response.

## Throughput

Measure the number of messages that we able to be sent/received in $n$ timesteps.

## Per-node energy

Add one to some per-node counter as a computation occurs.

## Fairness

Look at how many messages were successfully sent and received for each node.

## Latency

Nodes record the number of timesteps it takes to receive packets back.
