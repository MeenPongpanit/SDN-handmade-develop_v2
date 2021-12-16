from bson.json_util import dumps, loads
from sanic.response import json
from sanic.views import HTTPMethodView


class GraphView(HTTPMethodView):

    def get(self, request):
        data = loads(dumps(request.app.db['link_utilization'].get_all()))
        nodes = {}
        edges = {}
        for link in data:
            src_node = link['src_node_hostname']
            dst_node = link['dst_node_hostname']
            if src_node not in nodes:
                nodes[src_node] = f'node{len(nodes)}'
            if dst_node not in nodes:
                nodes[dst_node] = f'node{len(nodes)}'
            edges[f'edge{len(edges)}'] = {'source':nodes[src_node], 'target':nodes[dst_node]}
        nodes = {nodes[i]:{'name':i} for i in nodes}
        graph = {"nodes":nodes, "edges":edges}
        flows = request.app.db['flow_stat'].get_all().sort("in_bytes", -1)
        return json({"graph": graph, "status": "ok"})

    def post(self, request):

        filters = request.json['filters']
        filters = filters['_value']
        # print(filters)


        data = loads(dumps(request.app.db['link_utilization'].get_all()))
        nodes = {}
        edges = {}
        flows_by_edge = {}

        flows = request.app.db['flow_stat'].get_all().sort("in_bytes", -1)
        flows_data = []
        links_with_flows = []
        for flow in flows:
            flow_data = {
                'src_ip':flow['ipv4_src_addr'], 
                'dst_ip':flow['ipv4_dst_addr'], 
                'src_port':flow['l4_src_port'],
                'dst_port':flow['l4_dst_port'],
                'next_hop_ip':flow['ipv4_next_hop'],
                
                }
            if flow.get('Mbits_per_sec', ''):
                flow_data['flow_rate'] = '%.4f'%flow['Mbits_per_sec']
            else:
                flow_data['flow_rate'] = ''
            if (flow['l4_dst_port'] in filters) or (flow['l4_src_port'] in filters) or not filters :
                links_with_flows.append(flow['ipv4_next_hop'])
                flows_data.append(flow_data)


        for link in data:
            src_node = link['src_node_hostname']
            dst_node = link['dst_node_hostname']
            if src_node not in nodes:
                nodes[src_node] = f'node{len(nodes)}'
            if dst_node not in nodes:
                nodes[dst_node] = f'node{len(nodes)}'
            edge_id = f'edge{len(edges)}'
            edges[edge_id] = {'source':nodes[src_node], 'target':nodes[dst_node]}
            flows_by_edge[edge_id] = []
            if link['dst_if_ip'] in links_with_flows or link['src_if_ip'] in links_with_flows:
                edges[edge_id]['animate'] = True
            for flow_data in flows_data:
                if flow_data['next_hop_ip'] in (link['dst_if_ip'], link['src_if_ip']):
                    if flow_data['src_port'] in filters or flow_data['dst_port'] in filters or not filters:
                        flows_by_edge[edge_id].append(flow_data)
        
                    


        nodes = {nodes[i]:{'name':i} for i in nodes}
        graph = {"nodes":nodes, "edges":edges, "flows":flows_by_edge}
        # print("#####################")
        # print(graph['edges'])
        # print([(i['src_port'], i['dst_port']) for i in flows_data])
        # print("#####################")
        return json({"graph": graph, "flows_data":flows_by_edge, "status": "ok"})
 
