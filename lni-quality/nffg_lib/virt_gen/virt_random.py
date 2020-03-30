from numpy import random
import networkx as nx
from defs import *

class Randomness:
    def __init__(self, _min, _max):
        self.min = _min
        self.max = _max
        self.value = 0

    def create_range(self):
        self.min = random.randint()
        self.max = self.min + random.randint()

    def set_range(self, _min, _max):
        self.min = _min
        self.max = _max

    def get(self, _min=None, _max=None):
        if _min and _max:
            self.set_range(_min, _max)
        self.value = random.randint(self.min, self.max)
        return self.value


class NodeResources:
    def __init__(self):
        self.r = Randomness(0,0)
        self.values = {
            'cpu':0,
            'mem':0,
            'storage':0,
        }
        self.cpu_max = NODE_CPU_MAX
        self.cpu_min = NODE_CPU_MIN
        self.mem_max = NODE_MEM_MAX
        self.mem_min = NODE_MEM_MIN
        self.storage_max = NODE_STORAGE_MAX
        self.storage_min = NODE_STORAGE_MIN

    def get(self):
        self.values = {
            'cpu': self.r.get(self.cpu_min, self.cpu_max),
            'mem': self.r.get(self.mem_min, self.mem_max),
            'storage': self.r.get(self.storage_min, self.storage_max),
        }
        return self.values


class LinkResources:
    def __init__(self):
        self.r = Randomness(0, 0)
        self.values = {
            'delay': 0,
            'bandwidth': 0,
        }
        self.delay_max = LINK_DELAY_MAX
        self.delay_min = LINK_DELAY_MIN
        self.bandwidth_max = LINK_BANDWIDTH_MAX
        self.bandwidth_min = LINK_BANDWIDTH_MIN

    def get(self):
        self.values = {
            'delay': self.r.get(self.delay_min, self.delay_max),
            'bandwidth': self.r.get(self.bandwidth_min, self.bandwidth_max),
        }
        return self.values


class NodeLinkResources(LinkResources):
    def __init__(self):
        LinkResources.__init__(self)
        self.delay_max = NODE_LINK_DELAY_MAX
        self.delay_min = NODE_LINK_DELAY_MIN
        self.bandwidth_max = NODE_LINK_BANDWIDTH_MAX
        self.bandwidth_min = NODE_LINK_BANDWIDTH_MIN

class NFLinkResources(LinkResources):
    def __init__(self):
        LinkResources.__init__(self)
        self.delay_max = NF_LINK_DELAY_MAX
        self.delay_min = NF_LINK_DELAY_MIN
        self.bandwidth_max = NF_LINK_BANDWIDTH_MAX
        self.bandwidth_min = NF_LINK_BANDWIDTH_MIN


class NodeLinks:
    def __init__(self):
        self.num_ports = 0
        self.num_links = 0
        self.values = {}
        self.node_link_resources = NodeLinkResources()

    def set_num_ports(self, ports):
        self.num_ports = ports
        self.num_links = ((2*self.num_ports) - 1) * NODES_LINK_PROB

    def get(self):
        for port in range(self.num_links):
            self.values[1] = self.node_link_resources.get()
        return self.values

class NFLinks(NodeLinks):
    def __init__(self):
        pass

class Links:
    def __init__(self):
        pass


class Nodes:
    def __init__(self):
        pass


class Topo:
    def __init__(self):
        self.nodes = NODES
        self.degree = DEGREE
        self.edge_prob = EDGES_PROB
        self.neighbour_edges = NEIGHBOUR_EDGES
        self.graph = None

    def create(self, model):
        if model == 1:
            self.graph = nx.random_regular_graph(self.degree, self.nodes)
        elif model == 2:
            self.graph = nx.binomial_graph(self.nodes, self.edge_prob)
        elif model == 3:
            self.graph = nx.gnm_random_graph(self.nodes, self.neighbour_edges)
        elif model == 4:
            self.graph = nx.powerlaw_cluster_graph(self.nodes, self.neighbour_edges, self.edge_prob)
        elif model == 5:
            self.graph = nx.dense_gnm_random_graph(self.nodes, self.neighbour_edges)
        else:
            self.graph = nx.barabasi_albert_graph(self.nodes, self.neighbour_edges)

    def get(self, model):
        self.create(model)
        return self.graph
