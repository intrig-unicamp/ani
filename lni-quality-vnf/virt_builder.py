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

    #def __init__(self):
    #    self.virt = Virtualizer(id='BisBis', name='BisBis-View')

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
            #x=self.virt.nodes.node.keys()
            #node = self.virt.nodes[str(nid)]
            self.add_node_port(nid,'port-sap')
        #for nid, data in self.graph.nodes_iter(data=True):
        #    node = Infra_node(id=nid,
        #                      name=nid,
        #                      type=nid,
        #                      resources=Software_resource(
        #                          cpu=data['cpu'],
        #                          mem=data['mem'],
        #                          storage=data['storage']))
        #    self.virt.nodes.add(node)

    def add_node_port(self, ndid, type):
        ndid = str(ndid)
        if ndid in self.virt.nodes.node.keys():
            node = self.virt.nodes[ndid]
            if hasattr(node, 'ports'):
                if type=='port-sap':
                  port_id='SAP'+str(ndid)
                else:
                  if node.ports is None:
                      port_id = 0
                  else:
                      port_id = len(node.ports.port.keys())
                port = Port(id=port_id,
                            name=port_id,
                            port_type=type)
                node.ports.add(port)
                return port

    def add_infra_links(self):
        for srcid, dstid, data in self.graph.edges_iter(data=True):
            src = self.add_node_port(srcid, 'port-abstract')
            dst = self.add_node_port(dstid, 'port-abstract')
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

class ConverterV2:
    def __init__(self, str_id, str_name):
        self.virt = Virtualizer(id=str_id, name=str_name)

    def add_infra_nodes(self, nodes_final):
        for nodes in nodes_final:
          for nid, data in [(id, data) for id, data in nodes]:
            GnodeNF=GroupingNodes(tag="supported_NFs");
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
            self.add_node_port(nid,'port-sap')

    def add_node_port(self, ndid, type):
        ndid = str(ndid)
        if ndid in self.virt.nodes.node.keys():
            node = self.virt.nodes[ndid]
            if hasattr(node, 'ports'):
                if type=='port-sap':
                  port_id='SAP'+str(ndid)
                else:
                  if node.ports is None:
                      port_id = 0
                  else:
                      port_id = len(node.ports.port.keys())
                port = Port(id=port_id,
                            name=port_id,
                            port_type=type)
                node.ports.add(port)
                return port

    def add_infra_links(self, edges_final):
      for edges in edges_final:
        for srcid, dstid, data in [(src, dst, data) for src, dst, data in edges]:
        #for srcid, dstid, data in self.graph.edges_iter(data=True):
            src = self.add_node_port(srcid, 'port-abstract')
            dst = self.add_node_port(dstid, 'port-abstract')
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

    def get(self, nodes_final, edges_final):
        self.add_infra_nodes(nodes_final)
        self.add_infra_links(edges_final)
        return self.virt
