# Sean thoughts

## Changes

### Change simulate function to step (could also have a get_metrics function in arena as well)

Might be helpful to have a function called step, and it runs through one timestep? As opposed to simulate, so we can sort of see the internal workings of all the things

Can still look at simulate by stepping like $n$ times though.

### Distance instead of power for nodes

I think it'd be easier to just have a maximum distance a node can reliably transmit, and then calculate the chance that the transmission succeeds based off of that?

## Testing for normal metworks

Partitions in [`testing_strategy.md`](./mesh/tests/testing_strategy.md).

I also added some functions various classes (labelled them below testing!).
