# Our Assumptions

1. Reception reports broadcast on separate frequency - will not collide with normal packets.

2. If it's not possible to decode a packet, our arena will handle it.

3. No guessing on neighbor state. It's difficult to implement and COPE should still provide benefits. Guessing is also mainlu helpful for dropped reception reports, but we assume no dropped reception reports.

4. All packets are the same size.
