from cope.arena import Arena as CopeArena
from mesh.arena import Arena as MeshArena

import json
import os

topology = "alice_and_bob.json"

cope_arena = CopeArena(f"./topologies/{topology}")
mesh_arena = MeshArena(f"./topologies/{topology}")

cope_metrics = cope_arena.simulate(20, 'type1', 'type1', probability_send=1)
mesh_metrics = mesh_arena.simulate(20, 'type1', 'type1', probability_send=1)

def aggregate_metrics(metrics, is_cope, topology):
    for _, n in metrics.items():
        timesteps = n['timesteps']
        break

    throughput = sum(n['successes'] for n in metrics.values()) / timesteps

    # this is just successes amongst sending nodes
    messages_sent = [n['successes'] for n in metrics.values() if n['successes'] != 0]

    throughputs = [round(sent / timesteps, 3) for sent in messages_sent]
    latencies = [round(n['average_latency'],3) for n in metrics.values() if n['average_latency'] != float('inf')]

    metrics = {
        'overall_throughput': throughput,
        'timesteps': timesteps,
        'messages_sent': messages_sent,
        'latencies': latencies,
        'throughputs': throughputs
    }

    print(metrics)
    cope_str = 'cope' if is_cope else 'mesh'
    with open(f'./simulation_results/{topology}/{cope_str}_metrics_{topology}.json', 'w') as f:
        json.dump(metrics, f)

exp_name = topology.split('.')[0]
if not os.path.exists('./simulation_results/' + exp_name):
    os.makedirs('./simulation_results/' + exp_name)

print("COPEEEE")
aggregate_metrics(cope_metrics, True, exp_name)


print("\n\nMESHHHH")
aggregate_metrics(mesh_metrics, False, exp_name)
