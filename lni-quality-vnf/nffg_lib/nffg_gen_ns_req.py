#!/usr/bin/env python
# Copyright 2017 Janos Czentye, Balazs Nemeth, Balazs Sonkoly
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Contains several functions that generate example NFFGs.
"""
import sys

from nffg import *
from virt_gen.virt_builder import InfraBuilder, Converter
from virt_gen.defs import *

class Generator:
    def __init__(self, model):
        self.model = model
        self.builder = InfraBuilder()
        self.converter = Converter(None)

    def get(self):
        graph = self.builder.get(self.model)
        self.converter.set_graph(graph)
        virt = self.converter.get()
        return virt

    def set_model(self, model):
        self.model = model

def ns_req_1 ():
  nffg = NFFG(id="ns-req-1", name="ns-req-1", mode='ADD')

  sap55 = nffg.add_sap(name="SAP55", id="SAP55")
  sap55.add_port(1)
  sap21 = nffg.add_sap(name="SAP21", id="SAP21")
  sap21.add_port(1)

  nfA = nffg.add_nf(id="nf1", name="A", func_type='A', cpu=2, mem=2,
                  storage=0)
  nfA.add_port(1)

  nffg.add_sglink(sap55.ports[1], nfA.ports[1], id="sap55nfA")
  nffg.add_sglink(nfA.ports[1], sap21.ports[1], id="nfAsap21")

  nffg.add_req(sap55.ports[1], sap21.ports[1], delay=30, bandwidth=4,
               sg_path=["sap55nfA", "nfAsap21"])

  return nffg

def generate_ns_req (strMode):
  for num_ns in range(1,NRO_NS_REQ+1):
    str_num_ns=str(num_ns)
    #nffg = NFFGModel()
    #nffg.id=id="ns-req-"+str_num_ns
    #nffg.name="ns-req-"+str_num_ns
    #nffg.mode='ADD'
    nffg = NFFG(id="ns-req-"+str_num_ns, name="ns-req-"+str_num_ns, mode=strMode)

    v_nf = []
    for num_nf in range(1,num_ns+1):
      str_num_nf = str(num_nf)
      nfA = nffg.add_nf(id="nf"+str_num_nf, name="A", func_type='A', cpu=2, mem=2,
                      storage=0)
      nfA.add_port(0)
      nfA.add_port(1)
      v_nf.append(nfA)

    path_nf = []

    sap_src = nffg.add_sap(name="SAP55", id="SAP55")
    sap_src.add_port(0)
    strID="ns"+str_num_ns+sap_src.id+v_nf[0].id
    nffg.add_sglink(sap_src.ports[0], v_nf[0].ports[0], id=strID)
    path_nf.append(strID)

    for i in range(len(v_nf)-1):
        strID="ns"+str_num_ns+str(v_nf[i].id)+str(v_nf[i+1].id)
        nffg.add_sglink(v_nf[i].ports[1], v_nf[i+1].ports[0], id=strID)
        path_nf.append(strID)

    sap_dst = nffg.add_sap(name="SAP48", id="SAP48")
    sap_dst.add_port(0)
    strID="ns"+str_num_ns+v_nf[len(v_nf)-1].id+sap_dst.id
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
    if strMode=='ADD':
      strFolder='./ns_req_files_add/'
    else:
      strFolder='./ns_req_files_del/'

    strFile=strFolder+'ns_req_'+str_num_ns+'.nffg'
    with open(strFile, 'w') as nffg_file:
      json.dump(nffg.dump_to_json(), nffg_file)

if __name__ == "__main__":
  nffg=generate_ns_req('ADD')
  nffg=generate_ns_req('DELETE')
