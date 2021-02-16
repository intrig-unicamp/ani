from virt_random import Topo

topo = Topo()

g = topo.get(4)
print g.edges(data=True)