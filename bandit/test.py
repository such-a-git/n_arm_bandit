import spynnaker8 as p
from spynnaker.pyNN.connections.\
    spynnaker_live_spikes_connection import SpynnakerLiveSpikesConnection
from spynnaker.pyNN.spynnaker_external_device_plugin_manager import \
    SpynnakerExternalDevicePluginManager as ex
from spinn_bandit import Bandit
import pylab
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
import numpy as np
from spinn_front_end_common.utilities.globals_variables import get_simulator

def get_scores(bandit_pop,simulator):
    b_vertex = bandit_pop._vertex
    scores = b_vertex.get_data(
        'score', simulator.no_machine_time_steps, simulator.placements,
        simulator.graph_mapper, simulator.buffer_manager, simulator.machine_time_step)

    return scores.tolist()

p.setup(timestep=1.0)

probabilities = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]

input_size = len(probabilities)
input_pop = p.Population(len(probabilities), p.SpikeSourcePoisson(rate=5))

output_pop1 = p.Population(2, p.IF_cond_exp())
output_pop2 = p.Population(2, p.IF_cond_exp())

random_seed = []
for j in range(4):
    random_seed.append(np.random.randint(0xffff))
arms_pop = p.Population(input_size, Bandit(probabilities, 200, rand_seed=random_seed))

input_pop.record('spikes')
# arms_pop.record('spikes')
output_pop1.record('spikes')
output_pop2.record('spikes')

i2a = p.Projection(input_pop, arms_pop, p.AllToAllConnector())

#neuron ID 0 = reward
#neuron ID 1 = no reward
test_rec = p.Projection(arms_pop, arms_pop, p.AllToAllConnector(), p.StaticSynapse(weight=0.1, delay=0.5))
i2o1 = p.Projection(arms_pop, output_pop1, p.AllToAllConnector(), p.StaticSynapse(weight=0.1, delay=0.5))
i2o2 = p.Projection(arms_pop, output_pop2, p.OneToOneConnector(), p.StaticSynapse(weight=0.1, delay=0.5))

simulator = get_simulator()

runtime = 10000
p.run(runtime)

scores = get_scores(bandit_pop=arms_pop, simulator=simulator)

print scores

spikes_in = input_pop.get_data('spikes').segments[0].spiketrains
spikes_out1 = output_pop1.get_data('spikes').segments[0].spiketrains
spikes_out2 = output_pop2.get_data('spikes').segments[0].spiketrains
Figure(
    Panel(spikes_in, xlabel="Time (ms)", ylabel="nID", xticks=True),
    Panel(spikes_out1, xlabel="Time (ms)", ylabel="nID", xticks=True),
    Panel(spikes_out2, xlabel="Time (ms)", ylabel="nID", xticks=True)
)
plt.show()

p.end()





