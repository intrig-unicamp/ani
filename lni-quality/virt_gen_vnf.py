from virt_builder import InfraBuilder, Converter, ConverterV2
from numpy import random
import networkx as nx
import os

from nffg_lib.nffg import *
#from nffg_lib.virt_gen.virt_builder import InfraBuilder, Converter
from defs import *

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

class GeneratorV2:
    def __init__(self):
        self.converter = ConverterV2('BisBis', 'BisBis-View')

    def get(self, nodes_final, edges_final):
        virt = self.converter.get(nodes_final, edges_final)
        return virt

def info2(G):
    val1 = G.number_of_nodes()
    val2 = G.number_of_edges()
    nnodes=G.number_of_nodes()
    if len(G) > 0:
        s=sum(G.degree().values())
        val3 = float(s)/float(nnodes)
    return val1, val2, val3

def generate_ani_node_oriented(intModel, nfs, delay_req, bw_req, graph, iter_nf):
  #threshold = 0.75
  edges_final = []
  nodes_final = []

  nodes_src = []
  nodes_dst = []

  for i in range(iter_nf-1):
    #print (i)
    #nodes_src = [(n,d) for n,d in graph.nodes(data=True) if nfs[i].resources.cpu/d['cpu']<=threadhold]
    #nodes_dst = [(n,d) for n,d in graph.nodes(data=True) if nfs[i+1].resources.cpu/d['cpu']<=threadhold]
    nodes_src.append([(n,d) for n,d in graph.nodes(data=True) if d['cpu']>=nfs[i].resources.cpu])
    nodes_dst.append([(n,d) for n,d in graph.nodes(data=True) if d['cpu']>=nfs[i+1].resources.cpu])

    for nn in nodes_src:
      if nn not in nodes_final:
        nodes_final.append(nn)

    for nn in nodes_dst:
      if nn not in nodes_final:
        nodes_final.append(nn)

  print 'nodes final: '+ str(list(nodes_final))
  print 'edges final: '+ str(list(edges_final))

  #virt_gen = GeneratorV2()
  #virt = virt_gen.get(nodes_final, edges_final)
  #print 'saving ani-model ...'
  #strFolder='./ns_req_files/'
  #strModel='model'+str(intModel)
  #strFolder=strFolder+strModel+'/'
  #str_num_ns=str(num_ns)
  #strFolderADD=strFolder+'ns_req_files_add/'+'vnfs'+str_num_ns
  #virt.write_to_file(strFolderADD+'/ani-model-'+str(intModel)+'.xml')

  ani_graph = nx.Graph()
  for d in nodes_final:
    ani_graph.add_nodes_from(d)
  for d in edges_final:
    ani_graph.add_edges_from(d)

  #nx.write_gml(graph, './tests/configs/full-graph.gml')
  #nx.write_gml(ani_graph, './tests/configs/ani-graph.gml')
  print nx.info(graph)
  print nx.info(ani_graph)

  return nodes_final, edges_final, ani_graph

def generate_ani_edge_oriented(intModel, nfs, delay_req, bw_req, graph, iter_nf):
  ###########Compute minimo
  #for i in range(len(nfs)-1):
  #bw_req = MIN ()

  #threshold = 0.75
  edges_final = []
  nodes_final = []

  src_dst = []

  for i in range(iter_nf-1):
    #nodes_src = [(n,d) for n,d in graph.nodes(data=True) if nfs[i].resources.cpu/d['cpu']<=threshold]
    #nodes_dst = [(n,d) for n,d in graph.nodes(data=True) if nfs[i+1].resources.cpu/d['cpu']<=threshold]
    nodes_src = [(n,d) for n,d in graph.nodes(data=True)]
    nodes_dst = [(n,d) for n,d in graph.nodes(data=True)]
    #nodes_src = [(n,d) for n,d in graph.nodes(data=True) if d['cpu']>=nfs[i].resources.cpu \
    #                                                        and d['mem']>=nfs[i].resources.mem \
    #                                                        and d['storage']>=nfs[i].resources.storage]
    #nodes_dst = [(n,d) for n,d in graph.nodes(data=True) if d['cpu']>=nfs[i+1].resources.cpu \
    #                                                        and d['mem']>=nfs[i+1].resources.mem \
    #                                                        and d['storage']>=nfs[i+1].resources.storage]

    for src_id, src_d in nodes_src:
      for dst_id, dst_d in nodes_dst:
          aux = [(src_id,dst_id)]
          if aux not in src_dst:
            src_dst.append(aux)
            src_dst.append([(dst_id,src_id)])
            if src_id != dst_id:
              src_dst.append(aux)
              src_dst.append([(dst_id,src_id)])

              paths = []
              if nx.has_path(graph,src_id,dst_id):
                  for path in nx.all_shortest_paths(graph,src_id,dst_id):
                      edges = []
                      nodes = []
                    #if len(path)-1<=delay_req:
                      print ("SI, Nodes: [%s,%s], Path:[%s], Lenght:[%s]" % (src_id,dst_id, str(path), str(len(path)-1)))
                      num=0
                      for nodes_path in range(len(path)-1):
                        val_edge = [(srcid,dstid,data) for srcid, dstid, data in graph.edges_iter(data=True) if data['bandwidth']>=bw_req \
                                                                                        and ((srcid==path[nodes_path] and dstid==path[nodes_path+1])
                                                                                        or (srcid==path[nodes_path+1] and dstid==path[nodes_path]))]
                        if len(val_edge)==0:
                          #edges.append(val_edge)
                          break
                        else:
                          num=num+1
                          edges.append(val_edge)
                          #nodes_dst = [(n,d) for n,d in graph.nodes(data=True) if n==path[n]
                          #print 'dlachosper'+str(path[n])
                          #id_node = path[nodes_path]
                          #aux_node = [(n,d) for n,d in graph.nodes(data=True) if n == path[nodes_path]]
                          nodes.append([(n,d) for n,d in graph.nodes(data=True) if n == path[nodes_path]])
                          #id_node = path[n+1]
                          #aux_node = [(n,d) for n,d in graph.nodes(data=True) if n == path[nodes_path+1]]
                          nodes.append([(n,d) for n,d in graph.nodes(data=True) if n == path[nodes_path+1]])
                          #nodes.append(graph.node[path[n+1]])
                      if num==len(path)-1:
                        paths.append(path)
                        for e in edges:
                          if e not in edges_final:
                            edges_final.append(e)

                        for nn in nodes:
                          if nn not in nodes_final:
                            nodes_final.append(nn)
                    #else:
                      #print ("NO, Nodes: [%s,%s], Path:[%s], Lenght:[%s]" % (src_id,dst_id, str(path), str(len(path)-1)))
                  #print len(paths)
                  #print len(list(nx.all_shortest_paths(graph,src_id,dst_id)))
                  #if len(paths)<len(list(nx.all_shortest_paths(graph,src_id,dst_id))):
                    #print ("PATH NO NO, Nodes: [%s,%s], Paths:[%s]" % (src_id,dst_id, str(list(edges))))
                  #else:
                    #print ("PATH SI SI, Nodes: [%s,%s], Paths:[%s]" % (src_id,dst_id, str(list(edges))))

  print 'nodes final: '+ str(list(nodes_final))
  print 'edges final: '+ str(list(edges_final))

  #for nodes in nodes_final:
    #for id, data in [(id, data) for id, data in nodes]:
      #print id
      #print data

  #for edges in edges_final:
    #for src, dst, data in [(src, dst, data) for src, dst, data in edges]:
      #print src
      #print dst
      #print data
      #test.add_nodes_from(d)

  virt_gen = GeneratorV2()
  virt = virt_gen.get(nodes_final, edges_final)
  print 'saving ani-model ...'
  #virt.write_to_file('./tests/configs/ani-model-4.xml')
  strFolder='./ns_req_files/'
  strModel='model'+str(intModel)
  strFolder=strFolder+strModel+'/'
  str_num_ns=str(num_ns)
  strFolderADD=strFolder+'ns_req_files_add/'+'vnfs'+str_num_ns
  virt.write_to_file(strFolderADD+'/ani-model-'+str(intModel)+'.xml')

  ani_graph = nx.Graph()
  for d in nodes_final:
    ani_graph.add_nodes_from(d)
  for d in edges_final:
    ani_graph.add_edges_from(d)

  print nx.info(graph)
  print nx.info(ani_graph)

  return nodes_final, edges_final, ani_graph

def generate_ani(intModel, ns_name, nfs, delay_req, bw_req, graph, iter_nf):
  #graph=nx.read_gml('/home/dlachosper/Dropbox/Thesis/evaluation/ani/virt_gen/tests/configs/graph-4.gml')
  #node_src=1
  #node_dst=2
  #paths=nx.all_shortest_paths(graph,node_src,node_dst)
  #paths=nx.all_simple_paths(graph,node_src,node_dst)
  #print(list(paths))

  #threshold = 0.75
  edges_final = []
  nodes_final = []

  src_dst = []

  for i in range(iter_nf-1):
    #nodes_src = [(n,d) for n,d in graph.nodes(data=True) if nfs[i].resources.cpu/d['cpu']<=threshold]
    #nodes_dst = [(n,d) for n,d in graph.nodes(data=True) if nfs[i+1].resources.cpu/d['cpu']<=threshold]
    nodes_src = [(n,d) for n,d in graph.nodes(data=True) if d['cpu']>=nfs[i].resources.cpu]
    nodes_dst = [(n,d) for n,d in graph.nodes(data=True) if d['cpu']>=nfs[i+1].resources.cpu]
    #nodes_src = [(n,d) for n,d in graph.nodes(data=True) if d['cpu']>=nfs[i].resources.cpu \
    #                                                        and d['mem']>=nfs[i].resources.mem \
    #                                                        and d['storage']>=nfs[i].resources.storage]
    #nodes_dst = [(n,d) for n,d in graph.nodes(data=True) if d['cpu']>=nfs[i+1].resources.cpu \
    #                                                        and d['mem']>=nfs[i+1].resources.mem \
    #                                                        and d['storage']>=nfs[i+1].resources.storage]

    for src_id, src_d in nodes_src:
      for dst_id, dst_d in nodes_dst:
          aux = [(src_id,dst_id)]
          if aux not in src_dst:
            src_dst.append(aux)
            src_dst.append([(dst_id,src_id)])
            if src_id != dst_id:
              src_dst.append(aux)
              src_dst.append([(dst_id,src_id)])

              paths = []
              if nx.has_path(graph,src_id,dst_id):
                  for path in nx.all_shortest_paths(graph,src_id,dst_id):
                      edges = []
                      nodes = []
                    #if len(path)-1<=delay_req:
                      print ("SI, Nodes: [%s,%s], Path:[%s], Lenght:[%s]" % (src_id,dst_id, str(path), str(len(path)-1)))
                      num=0
                      for nodes_path in range(len(path)-1):
                        val_edge = [(srcid,dstid,data) for srcid, dstid, data in graph.edges_iter(data=True) if data['bandwidth']>=bw_req \
                                                                                        and ((srcid==path[nodes_path] and dstid==path[nodes_path+1])
                                                                                        or (srcid==path[nodes_path+1] and dstid==path[nodes_path]))]
                        if len(val_edge)==0:
                          #edges.append(val_edge)
                          break
                        else:
                          num=num+1
                          edges.append(val_edge)
                          #nodes_dst = [(n,d) for n,d in graph.nodes(data=True) if n==path[n]
                          #print 'dlachosper'+str(path[n])
                          #id_node = path[nodes_path]
                          #aux_node = [(n,d) for n,d in graph.nodes(data=True) if n == path[nodes_path]]
                          nodes.append([(n,d) for n,d in graph.nodes(data=True) if n == path[nodes_path]])
                          #id_node = path[n+1]
                          #aux_node = [(n,d) for n,d in graph.nodes(data=True) if n == path[nodes_path+1]]
                          nodes.append([(n,d) for n,d in graph.nodes(data=True) if n == path[nodes_path+1]])
                          #nodes.append(graph.node[path[n+1]])
                      if num==len(path)-1:
                        paths.append(path)
                        for e in edges:
                          if e not in edges_final:
                            edges_final.append(e)

                        for nn in nodes:
                          if nn not in nodes_final:
                            nodes_final.append(nn)
                    #else:
                      #print ("NO, Nodes: [%s,%s], Path:[%s], Lenght:[%s]" % (src_id,dst_id, str(path), str(len(path)-1)))
                  #print len(paths)
                  #print len(list(nx.all_shortest_paths(graph,src_id,dst_id)))
                  #if len(paths)<len(list(nx.all_shortest_paths(graph,src_id,dst_id))):
                    #print ("PATH NO NO, Nodes: [%s,%s], Paths:[%s]" % (src_id,dst_id, str(list(edges))))
                  #else:
                    #print ("PATH SI SI, Nodes: [%s,%s], Paths:[%s]" % (src_id,dst_id, str(list(edges))))

  print 'nodes final: '+ str(list(nodes_final))
  print 'edges final: '+ str(list(edges_final))

  #for nodes in nodes_final:
    #for id, data in [(id, data) for id, data in nodes]:
      #print id
      #print data

  #for edges in edges_final:
    #for src, dst, data in [(src, dst, data) for src, dst, data in edges]:
      #print src
      #print dst
      #print data
      #test.add_nodes_from(d)

  virt_gen = GeneratorV2()
  virt = virt_gen.get(nodes_final, edges_final)
  print 'saving ani-model ...'
  #virt.write_to_file('./tests/configs/ani-model-4.xml')
  strFolder='./ns_req_files/'
  strModel='model'+str(intModel)
  strFolder=strFolder+strModel+'/'
  str_num_ns=str(num_ns)
  strFolderADD=strFolder+'ns_req_files_add/'+'vnfs'+str_num_ns
  virt.write_to_file(strFolderADD+'/ani-model-'+str(intModel)+'.xml')

  ani_graph = nx.Graph()
  for d in nodes_final:
    ani_graph.add_nodes_from(d)
  for d in edges_final:
    ani_graph.add_edges_from(d)

  print nx.info(graph)
  print nx.info(ani_graph)

  return nodes_final, edges_final, ani_graph

def generate_ns_req (intModel, graph, ns_name):
  v_nf = []
  nffg_aux = NFFG(id='nffg_aux', name='nffg_aux', mode='ADD')

  for num_nf in range(1, NRO_VNFS_X_REQ+1):
    str_num_nf = str(num_nf)
    val_cpu = random.randint(NF_CPU_MIN, NF_CPU_MAX)
    #val_mem = random.randint(NF_MEM_MIN, NF_MEM_MAX)
    #val_sto = random.randint(NF_STORAGE_MIN, NF_STORAGE_MAX)

    nfA = nffg_aux.add_nf(id="nf"+str_num_nf, name="A", func_type='A', cpu=val_cpu, mem=0, storage=0)
    #nfA = nffg_aux.add_nf(id="nf"+str_num_nf, name="A", func_type='A', cpu=val_cpu, mem=val_mem,
    #                    storage=val_sto)
    nfA.add_port(0)
    nfA.add_port(1)
    v_nf.append(nfA)

  delay_req=140

  #graph_info = (NRO_VNFS_X_REQ-1)*[12*[0]]
  matrix=[]
  bw_req = 0

  for iter_nf in range(2, NRO_VNFS_X_REQ+1):
      row=[]
      bw_aux=random.randint(FLOW_BANDWIDTH_MIN, FLOW_BANDWIDTH_MAX)#4
      if bw_aux>bw_req:
        bw_req = bw_aux

      nodes_final_e, edges_final_e, ani_graph_e = generate_ani_edge_oriented(intModel, v_nf, delay_req, bw_req, graph, iter_nf)
      nodes_final_n, edges_final_n, ani_graph_n = generate_ani_node_oriented(intModel, v_nf, delay_req, bw_req, graph, iter_nf)
      nodes_final, edges_final, ani_graph = generate_ani(intModel, ns_name, v_nf, delay_req, bw_req, graph, iter_nf)

      val1, val2, val3 = info2(graph)
      valDen1 = nx.density(graph)
      row.append(val1)
      row.append(val2)
      row.append(val3)

      val4e, val5e, val6e = info2(ani_graph_e)
      valDen2e = nx.density(ani_graph_e)
      row.append(val4e)
      row.append(val5e)
      row.append(val6e)

      val4n, val5n, val6n = info2(ani_graph_n)
      valDen2n = nx.density(ani_graph_n)

      row.append(val4n)
      row.append(val5n)
      row.append(val6n)

      val4, val5, val6 = info2(ani_graph)
      valDen2 = nx.density(ani_graph)

      row.append(val4)
      row.append(val5)
      row.append(val6)

      matrix.append(row)

  for iter_nf in range(2, NRO_VNFS_X_REQ+1):
    strFoldere = './results/reduction/edge/'
    if not os.path.exists(strFoldere):
      os.makedirs(strFoldere)
    outputFileNamee =strFoldere+'out-model'+str(intModel)+'nf'+str(iter_nf)+'.txt'

    strFoldern = './results/reduction/node/'
    if not os.path.exists(strFoldern):
      os.makedirs(strFoldern)
    outputFileNamen =strFoldern+'out-model'+str(intModel)+'nf'+str(iter_nf)+'.txt'

    strFolder = './results/reduction/node-edge/'
    if not os.path.exists(strFolder):
      os.makedirs(strFolder)
    outputFileName =strFolder+'out-model'+str(intModel)+'nf'+str(iter_nf)+'.txt'

    os.system('echo "%d %d %s %s %d %d %s %s" >> %s' % (matrix[iter_nf-2][0],matrix[iter_nf-2][1],str(matrix[iter_nf-2][2]).replace('.',','),str(valDen1).replace('.',','), matrix[iter_nf-2][3],matrix[iter_nf-2][4],str(matrix[iter_nf-2][5]).replace('.',','),str(valDen2e).replace('.',','),outputFileNamee))
    os.system('echo "%d %d %s %s %d %d %s %s" >> %s' % (matrix[iter_nf-2][0],matrix[iter_nf-2][1],str(matrix[iter_nf-2][2]).replace('.',','),str(valDen1).replace('.',','), matrix[iter_nf-2][6],matrix[iter_nf-2][7],str(matrix[iter_nf-2][8]).replace('.',','),str(valDen2n).replace('.',','),outputFileNamen))
    os.system('echo "%d %d %s %s %d %d %s %s" >> %s' % (matrix[iter_nf-2][0],matrix[iter_nf-2][1],str(matrix[iter_nf-2][2]).replace('.',','),str(valDen1).replace('.',','), matrix[iter_nf-2][9],matrix[iter_nf-2][10],str(matrix[iter_nf-2][11]).replace('.',','),str(valDen2).replace('.',','),outputFileName))

'''
  for sam in range(1,NRO_SAMPLES_X_VNFS_X_REQ+1):
    ns_name_f=ns_name+'-sam-'+str(sam)
    while True:
      aux_id=[]
      for nodes in nodes_final:
        for id, data in [(id, data) for id, data in nodes]:
          aux_id.append(id)
      node_src = random.choice(aux_id)
      while True:
        node_dst= random.choice(aux_id)
        if node_src!=node_dst:
          break
      if nx.has_path(ani_graph,node_src,node_dst):
        paths=nx.shortest_path(ani_graph,node_src,node_dst)
        print(list(paths))
        break

    str_num_ns=str(num_ns)
    nffg = NFFG(id=ns_name_f, name=ns_name_f, mode='ADD')

    path_nf = []

    for nf in v_nf:
      nffg.add_nf(nf)

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

    nffg.add_req(sap_src.ports[0], sap_dst.ports[0], delay=delay_req, bandwidth=bw_req,
                 sg_path=path_nf)

    strFolder='./ns_req_files/'
    strModel='model'+str(intModel)
    strFolder=strFolder+strModel+'/'

    strFolderADD=strFolder+'ns_req_files_add/'+'vnfs'+str_num_ns+'/'
    if not os.path.exists(strFolderADD):
      os.makedirs(strFolderADD)

    strFolderDEL=strFolder+'ns_req_files_del/'+'vnfs'+str_num_ns+'/'
    if not os.path.exists(strFolderDEL):
      os.makedirs(strFolderDEL)

    nffg.mode='ADD'
    strFile=strFolderADD+'ns_req_'+str_num_ns+'_sam_'+str(sam)+'.nffg'
    with open(strFile, 'w') as nffg_file:
      json.dump(nffg.dump_to_json(), nffg_file)

    nffg.mode='DELETE'
    strFile=strFolderDEL+'ns_req_'+str_num_ns+'_sam_'+str(sam)+'.nffg'
    with open(strFile, 'w') as nffg_file:
      json.dump(nffg.dump_to_json(), nffg_file)
'''

if __name__ == "__main__":
    virt_gen = Generator(1)
    ##for model in range(1,7):
    for model in range(1,2):
        virt_gen.set_model(model)
        virt, graph = virt_gen.get()
        for num_ns in range(1, NRO_NS_REQ+1):
            while True:
                try:
                    ns_name='ns-req-'+str(num_ns)
                    generate_ns_req(model, graph, ns_name)
                    break
                except:
                    print 'dlachosper error'
        print 'saving model ' + str(model)

        strFolder='./ns_req_files/'
        strModel='model'+str(model)
        strFolderADD=strFolder+strModel
        virt.write_to_file(strFolderADD+'/model-'+str(model)+'.xml')
        nx.write_gml(graph, strFolderADD+'/full-graph-model-'+str(model)+'.gml')
        #virt.write_to_file('./tests/configs/model-'+str(model)+'.xml')
        #print 'saving graph ' + str(model)
        #nx.write_gml(graph, './tests/configs/graph-'+str(model)+'.gml')
