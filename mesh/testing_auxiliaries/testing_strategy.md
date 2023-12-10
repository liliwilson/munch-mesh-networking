# Testing Strategy

## Arena

### Partition on parsing

Can parse the following complexities:

1. Number of nodes: 1, 2, >2
2. Number of hierarchy clases: 1, 2, >2

### Partitions on links

1. Links existing based on hierarchy classes: No link should exist, some link should exist.

2. Links based on distance: Some link should exist, no link should exist

### Partition on Step/Simulate

4. Step/simulate works
5. Basic metrics work? (not sure how to test though -- maybe will use a butterfly network? Otherwise need to force step/simulate to run in order)

## Node

### Creation

1. Can add link
2. Can set path

### Interaction with Packet

3. Can generate packet with correct nexthop
4. Can receive packet correctly
5. Can receive and send packets correctly

## Link

### Partitions on creation

1. Can create Link Objects correctly

### Partitions on sending Packets through links

1. Will sometimes fail if too little distance.

## Packet

### Creation

1. Can create a Packet object
2. Packet object has correct attributes idk?
