from cope.arena import Arena as CopeArena
from mesh.arena import Arena as MeshArena

topology = "alice_and_bob.json"

cope_arena = CopeArena(f"./topologies/{topology}")
mesh_arena = MeshArena(f"./topologies/{topology}")

cope_metrics = cope_arena.simulate(1000, 'type1', 'type1', probability_send=1)
mesh_metrics = mesh_arena.simulate(1000, 'type1', 'type1', probability_send=1)

print("COPEEEE")
print(cope_metrics)
print(sum([i['successes'] for i in cope_metrics.values()])/10000)

print("MESHHHH")
print(mesh_metrics)
print(sum([i['successes'] for i in mesh_metrics.values()])/10000)
