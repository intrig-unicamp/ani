from virt_builder import InfraBuilder, Converter
from numpy import random
import networkx as nx
import os

from nffg_lib.nffg import *
#from nffg_lib.virt_gen.virt_builder import InfraBuilder, Converter
from defs import *
import sys

class Generator:
    def __init__(self, model):
        self.model = model
        self.builder = InfraBuilder()
        self.converter = Converter(None)

    def get(self):
        graph = self.builder.get(self.model)
        self.converter.set_graph(graph)
        virt = self.converter.get()
        return virt, graph

    def set_model(self, model):
        self.model = model

def generate_ns_req (intModel, graph):
  for num_ns in range(1,NRO_NS_REQ+1):
    ns_name='ns-req-'+str(num_ns)
    for sam in range(1,NRO_SAMPLES_NS_X_REQ+1):
        ns_name_f=ns_name+'-sam-'+str(sam)
        while True:
          node_src= random.randint(1, len(graph))
          while True:
            node_dst= random.randint(1, len(graph))
            if node_src!=node_dst:
              break
          if nx.has_path(graph,node_src,node_dst):
            paths=nx.shortest_path(graph,node_src,node_dst)
            print(list(paths))
            break

        ##NS-REQ
        str_num_ns=str(num_ns)
        nffg = NFFG(id=ns_name_f, name=ns_name_f, mode='ADD')

        v_nf = []
        for num_nf in range(1,num_ns+1):
          str_num_nf = str(num_nf)
          nfA = nffg.add_nf(id="nf"+str_num_nf, name="A", func_type='A', cpu=2, mem=2,
                          storage=0)
          nfA.add_port(0)
          nfA.add_port(1)
          v_nf.append(nfA)

        path_nf = []

        name_sap_src='SAP'+str(node_src)
        sap_src = nffg.add_sap(name=name_sap_src, id=name_sap_src)
        sap_src.add_port(0)
        strID="ns"+str_num_ns+'sam'+str(sam)+sap_src.id+v_nf[0].id
        nffg.add_sglink(sap_src.ports[0], v_nf[0].ports[0], id=strID)
        path_nf.append(strID)

        for i in range(len(v_nf)-1):
            strID="ns"+str_num_ns+'sam'+str(sam)+str(v_nf[i].id)+str(v_nf[i+1].id)
            nffg.add_sglink(v_nf[i].ports[1], v_nf[i+1].ports[0], id=strID)
            path_nf.append(strID)

        name_sap_dst='SAP'+str(node_dst)
        sap_dst = nffg.add_sap(name=name_sap_dst, id=name_sap_dst)
        sap_dst.add_port(0)
        strID="ns"+str_num_ns+'sam'+str(sam)+v_nf[len(v_nf)-1].id+sap_dst.id
        nffg.add_sglink(v_nf[len(v_nf)-1].ports[1], sap_dst.ports[0], id=strID)
        path_nf.append(strID)

        nffg.add_req(sap_src.ports[0], sap_dst.ports[0], delay=30, bandwidth=4,
                     sg_path=path_nf)
          #str_num_nf=str(num_nf)
          #nf = NodeNF()
          #nf.id = "nf"+str_num_nf
          #nf.name = "A"
          #nf.functional_type = "A"
          #nf.resources.cpu = "2"
          #nf.resources.mem = "2"
          #nf.resources.storage = "0"

          #nffg.node_nfs.append(nf)
        #print (nffg.dump())
        strFolder='./ns_req_files/'
        strModel='model'+str(intModel)
        strFolder=strFolder+strModel+'/'
        #if strMode=='ADD':
        strFolderADD=strFolder+'ns_req_files_add/'+'vnfs'+str_num_ns+'/'
        if not os.path.exists(strFolderADD):
          os.makedirs(strFolderADD)
        #else:
        strFolderDEL=strFolder+'ns_req_files_del/'+'vnfs'+str_num_ns+'/'
        if not os.path.exists(strFolderDEL):
          os.makedirs(strFolderDEL)
        #print strFolder

        strFile=strFolderADD+'ns_req_'+str_num_ns+'_sam_'+str(sam)+'.nffg'
        with open(strFile, 'w') as nffg_file:
          json.dump(nffg.dump_to_json(), nffg_file)

        nffg.mode='DELETE'
        strFile=strFolderDEL+'ns_req_'+str_num_ns+'_sam_'+str(sam)+'.nffg'
        with open(strFile, 'w') as nffg_file:
          json.dump(nffg.dump_to_json(), nffg_file)

def generate_ani (intModel, graph):
  for num_ns in range(1,NRO_NS_REQ+1):
    for sam in range(1,NRO_SAMPLES_NS_X_REQ+1):
      str_num_ns=str(num_ns)
      strFolder='/home/dlachosper/Dropbox/Thesis/evaluation/ani/virt_gen/ns_req_files/'
      #strFolder='./ns_req_files/'
      strModel='model'+str(intModel)
      strFolder=strFolder+strModel+'/'
      strFolderADD=strFolder+'ns_req_files_add/'+'vnfs'+str_num_ns+'/'
      strFile=strFolderADD+'ns_req_'+str_num_ns+'_sam_'+str(sam)+'.nffg'

      with open(strFile) as f:
        nffg=NFFG.parse(f.read())

      for hop in nffg.sg_hops:
        src = hop.src.node.id
        dst = hop.dst.node.id
        print src
        #nffg.add_edge(hop.src.node, hop.dst.node, hop)

      for req in nffg.reqs:
        delay=req.delay
        bandwidth=req.bandwidth
        print req
        print req.delay
        for p in req.path.nodes:
          print p
        src_sap_port = nffg.__detect_connected_sap(port=req.src)
        dst_sap_port = __detect_connected_sap(port=req.dst)
        print src_sap_port
        print dst_sap_port
      print strFile
  return null

if __name__ == "__main__":
    for model in range(3,4):
        graph = nx.read_gml('/home/dlachosper/Dropbox/Thesis/evaluation/ani/virt_gen/tests/configs/graph-'+str(model)+'.gml')
        print nx.info(graph)
        generate_ani(model, graph)
        #print 'saving model ' + str(model)
        #virt.write_to_file('./tests/configs/model-'+str(model)+'.xml')
        #print 'saving graph ' + str(model)
        #nx.write_gml(graph, './tests/configs/graph-'+str(model)+'.gml')
