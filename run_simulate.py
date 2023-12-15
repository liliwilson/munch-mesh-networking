from cope.arena import Arena as CopeArena
from mesh.arena import Arena as MeshArena

import json
import os
import time

# define topology here
topology = "cope_setup.json"

def aggregate_metrics(metrics, is_cope, topology):
    print(metrics)
    for _, n in metrics.items():
        timesteps = n['timesteps']
        break

    throughput = sum(n['successes'] for n in metrics.values()) / timesteps

    # this is just successes amongst sending nodes
    messages_sent = [n['successes']
                     for n in metrics.values() if n['successes'] != 0]

    throughputs = [round(sent / timesteps, 6) for sent in messages_sent]
    latencies = [round(n['average_latency'], 6)
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

    cope_str = 'cope' if is_cope else 'mesh'
    with open(f'./simulation_results_final/{topology}/{cope_str}_metrics_{topology}.json', 'w') as f:
        json.dump(agg_metrics, f)

exp_name = topology.split('.')[0] 
if not os.path.exists('./simulation_results_final/' + exp_name):
    os.makedirs('./simulation_results_final/' + exp_name)

# make arenas
mesh_arena = MeshArena(f"./topologies/{topology}")
cope_arena = CopeArena(f"./topologies/{topology}")

# define number of timesteps, sending nodes, receiving nodes, and optionally datastream size parameters and node sending probabilities here
mesh_metrics = mesh_arena.simulate(
    100, 'type1', 'type1', probability_send=.5)
t = time.time()

aggregate_metrics(mesh_metrics, False, exp_name)
print('mesh time', time.time() - t)

t = time.time()
cope_metrics = cope_arena.simulate(
    100, 'type1', 'type1', probability_send=.5)

aggregate_metrics(cope_metrics, True, exp_name)
print('cope time', time.time() - t)

