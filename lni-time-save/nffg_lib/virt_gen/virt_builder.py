from virtualizer.virtualizer import *
from virt_random import *


class InfraBuilder:
    def __init__(self):
        self.node_resources = NodeResources()
        self.link_resources = LinkResources()
        self.topo = Topo()
        self.graph = None

    def create_infra_graph(self, model):
        self.graph = self.topo.get(model)

    def fill_nodes(self):
        for nid, data in self.graph.nodes_iter(data=True):
            resouces = self.node_resources.get()
            data.update(resouces)

    def fill_edges(self):
        for srcid, dstid, data in self.graph.edges_iter(data=True):
            resouces = self.link_resources.get()
            data.update(resouces)

    def get(self, model):
        self.create_infra_graph(model)
        self.fill_nodes()
        self.fill_edges()
        return self.graph



class Converter:
    def __init__(self, graph):
        self.graph = graph
        self.virt = Virtualizer()

    def set_graph(self, graph):
        self.graph = graph
        self.virt = Virtualizer(id='BisBis', name='BisBis-View')

    def add_infra_nodes(self):
        for nid, data in self.graph.nodes_iter(data=True):
            GnodeNF=GroupingNodes(tag="supported_NFs");
            #nfid=(nid*100)+0
            #nodeNF = Node (id=nfid, type='A')
            nodeNF = Node (id='A', type='A')
            GnodeNF.add(nodeNF)

            node = Infra_node(id=nid,
                              name=nid,
                              type=nid,
                              resources=Software_resource(
                                  cpu=data['cpu'],
                                  mem=data['mem'],
                                  storage=data['storage']),
			                  capabilities=Infra_nodeCapabilities(
                                  supported_NFs=GnodeNF))
            self.virt.nodes.add(node)

        #for nid, data in self.graph.nodes_iter(data=True):
        #    node = Infra_node(id=nid,
        #                      name=nid,
        #                      type=nid,
        #                      resources=Software_resource(
        #                          cpu=data['cpu'],
        #                          mem=data['mem'],
        #                          storage=data['storage']))
        #    self.virt.nodes.add(node)

    def add_node_port(self, ndid):
        ndid = str(ndid)
        if ndid in self.virt.nodes.node.keys():
            node = self.virt.nodes[ndid]
            if hasattr(node, 'ports'):
                if node.ports is None:
                    port_id = 0
                else:
                    port_id = len(node.ports.port.keys())
                port = Port(id=port_id,
                            name=port_id,
                            port_type='port-abstract')
                node.ports.add(port)
                return port

    def add_infra_links(self):
        for srcid, dstid, data in self.graph.edges_iter(data=True):
            src = self.add_node_port(srcid)
            dst = self.add_node_port(dstid)
            _id = str(srcid) + '-' + str(dstid)
            link = Link(id=_id,
                        name=_id,
                        src=src,
                        dst=dst,
                        resources=Link_resource(
                            bandwidth=data['bandwidth'],
                            delay=data['delay']))
            self.virt.links.add(link)

            src_b = dst
            dst_b = src
            _id_b = str(dstid) + '-' + str(srcid)
            link = Link(id=_id_b,
                        name=_id_b,
                        src=src_b,
                        dst=dst_b,
                        resources=Link_resource(
                            bandwidth=data['bandwidth'],
                            delay=data['delay']))
            self.virt.links.add(link)

    def get(self):
        self.add_infra_nodes()
        self.add_infra_links()
        return self.virt
