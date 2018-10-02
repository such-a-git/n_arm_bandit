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


p.setup(timestep=1.0)

probabilities = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]

input_size = len(probabilities)
input_pop = p.Population(len(probabilities), p.SpikeSourcePoisson(rate=5))

output_pop1 = p.Population(2, p.IF_cond_exp())
output_pop2 = p.Population(2, p.IF_cond_exp())

#neuron ID 0 = reward
#neuron ID 1 = no reward
arms_pop = p.Population(1, p.Bandit(probabilities, 200, np.random.random()))

input_pop.record('spikes')
# arms_pop.record('spikes')
output_pop1.record('spikes')
output_pop2.record('spikes')

i2a = p.Projection(input_pop, arms_pop, p.AllToAllConnector())

i2o1 = p.Projection(arms_pop, output_pop1, p.AllToAllConnector(), p.StaticSynapse(weight=0.1, delay=0.5))
i2o2 = p.Projection(arms_pop, output_pop2, p.OneToOneConnector(), p.StaticSynapse(weight=0.1, delay=0.5))

runtime = 10000
p.run(runtime)

spikes_in = input_pop.get_data('spikes').segments[0].spiketrains
spikes_out1 = output_pop1.get_data('spikes').segments[0].spiketrains
spikes_out2 = output_pop2.get_data('spikes').segments[0].spiketrains
Figure(
    Panel(spikes_in, xlabel="Time (ms)", ylabel="nID", xticks=True),
    Panel(spikes_out1, xlabel="Time (ms)", ylabel="nID", xticks=True),
    Panel(spikes_out2, xlabel="Time (ms)", ylabel="nID", xticks=True)
)
plt.show()

# pylab.figure()
# ax = pylab.subplot(1, 3, 1)#4, 1)
# pylab.plot([i[1] for i in spikes_on], [i[0] for i in spikes_on], "r.")
# pylab.xlabel("Time (ms)")
# pylab.ylabel("neuron ID")
# pylab.axis([0, runtime, -1, input_size + 1])
# # pylab.show()
# # pylab.figure()
# # spikes_on = arms_pop.getSpikes()
# # ax = pylab.subplot(1, 3, 2)#4, 1)
# # pylab.plot([i[1] for i in spikes_on], [i[0] for i in spikes_on], "r.")
# # pylab.xlabel("Time (ms)")
# # pylab.ylabel("neuron ID")
# # pylab.axis([0, runtime, -1, input_size + 1])
# # pylab.show()
# # pylab.figure()
# spikes_on = output_pop.getSpikes()
# ax = pylab.subplot(1, 3, 3)#4, 1)
# pylab.plot([i[1] for i in spikes_on], [i[0] for i in spikes_on], "r.")
# pylab.xlabel("Time (ms)")
# pylab.ylabel("neuron ID")
# pylab.axis([0, runtime, -1, 1 + 1])
# pylab.show()
#
#     #     spikes.append(neuron_pop[j].get_data("spikes"))
#     #     v.append(neuron_pop[j].get_data("v"))
#     # Figure(
#     #     # raster plot of the presynaptic neuron spike times
#     #     Panel(spikes[0+((i/time_slice)*agent_neurons)].segments[0].spiketrains,
#     #           yticks=True, markersize=2, xlim=(0, i+time_slice)),
#     #     Panel(spikes[1+((i/time_slice)*agent_neurons)].segments[0].spiketrains,
#     #           yticks=True, markersize=2, xlim=(0, i+time_slice)),
#     #     Panel(spikes[2+((i/time_slice)*agent_neurons)].segments[0].spiketrains,
#     #           yticks=True, markersize=2, xlim=(0, i+time_slice)),
#     #     Panel(spikes[3+((i/time_slice)*agent_neurons)].segments[0].spiketrains,
#     #           yticks=True, markersize=2, xlim=(0, i+time_slice)),
#     #     Panel(spikes[4+((i/time_slice)*agent_neurons)].segments[0].spiketrains,
#     #           yticks=True, markersize=2, xlim=(0, i+time_slice)),
#     #     title="Simple synfire chain example with injected spikes",
#     #     annotations="Simulated with {}".format(p.name())

p.end()





