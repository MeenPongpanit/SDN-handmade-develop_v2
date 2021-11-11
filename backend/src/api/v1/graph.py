from bson.json_util import dumps
from sanic.response import json
from sanic.views import HTTPMethodView
from json


class GraphView(HTTPMethodView):

    def get(self, request):
        data = json.dump(request.app.db['link_utilization'].get_all())
        print("================")
        print("================")
        print("================")
        print(data)
        print("================")
        print("================")
        print("================")
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
        return json({"graph": graph, "status": "ok"}, dumps=dumps)


