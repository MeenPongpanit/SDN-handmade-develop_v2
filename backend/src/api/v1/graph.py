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
        print(filters)


        data = loads(dumps(request.app.db['link_utilization'].get_all()))
        nodes = {}
        edges = {}
        flows = request.app.db['flow_stat'].get_all().sort("in_bytes", -1)

        filtered_flow = []
        for flow in flows:

            if flow['l4_dst_port'] in filters or flow['l4_src_port'] in filters :
                filtered_flow.append(flow['ipv4_next_hop'])

        for link in data:
            src_node = link['src_node_hostname']
            dst_node = link['dst_node_hostname']
            if src_node not in nodes:
                nodes[src_node] = f'node{len(nodes)}'
            if dst_node not in nodes:
                nodes[dst_node] = f'node{len(nodes)}'
            edge_id = len(edges)
            edges[f'edge{edge_id}'] = {'source':nodes[src_node], 'target':nodes[dst_node]}
            if link['dst_if_ip'] in filtered_flow or link['src_if_ip'] in filtered_flow or not filters:
                edges[f'edge{edge_id}']['animate'] = True
        nodes = {nodes[i]:{'name':i} for i in nodes}
        graph = {"nodes":nodes, "edges":edges}
        print("#####################")
        print(graph['edges'])
        print("#####################")
        return json({"graph": graph, "status": "ok"})
 
