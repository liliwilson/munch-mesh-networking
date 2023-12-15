from cope.arena import Arena as CopeArena
from mesh.arena import Arena as MeshArena

import json
import os

topology = "nycmesh.json"

cope_arena = CopeArena(f"./topologies/{topology}")
mesh_arena = MeshArena(f"./topologies/{topology}")

cope_metrics = cope_arena.simulate(
    10, 'user', 'supernode', probability_send=1)
mesh_metrics = mesh_arena.simulate(
    10, 'user', 'supernode', probability_send=1)


def aggregate_metrics(metrics, is_cope, topology):
    print(metrics)
    for _, n in metrics.items():
        timesteps = n['timesteps']
        break

    throughput = sum(n['successes'] for n in metrics.values()) / timesteps

    # this is just successes amongst sending nodes
    messages_sent = [n['successes']
                     for n in metrics.values() if n['successes'] != 0]

    throughputs = [round(sent / timesteps, 3) for sent in messages_sent]
    latencies = [round(n['average_latency'], 3)
                 for n in metrics.values() if n['average_latency'] != float('inf')]

    agg_metrics = {
        'overall_throughput': throughput,
        'timesteps': timesteps,
        'messages_sent': messages_sent,
        'latencies': latencies,
        'throughputs': throughputs
    }

    if is_cope:
        agg_metrics['coding_opps'] = [n['coding_opps_taken']
                                      for n in metrics.values() if n['coding_opps_taken'] != 0]

    print(agg_metrics)
    cope_str = 'cope' if is_cope else 'mesh'
    with open(f'./simulation_results/{topology}/{cope_str}_metrics_{topology}.json', 'w') as f:
        json.dump(agg_metrics, f)


exp_name = topology.split('.')[0]
if not os.path.exists('./simulation_results/' + exp_name):
    os.makedirs('./simulation_results/' + exp_name)

print("COPEEEE")
aggregate_metrics(cope_metrics, True, exp_name)


print("\n\nMESHHHH")
aggregate_metrics(mesh_metrics, False, exp_name)
