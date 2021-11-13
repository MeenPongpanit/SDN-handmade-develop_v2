"""Flow Aggregation Test"""
import requests

flows = requests.get('http://10.50.34.37:5001/api/v1/flow').json()
graph = requests.get("http://10.50.34.37:5001/api/v1/graph").json()
link = requests.get("http://10.50.34.37:5001/api/v1/link").json()


device_flow = {'edge_flow' : {}}
flow_id = []
for i in graph['graph']['edges']:
    device_flow['edge_flow'][i] = []

for i in range(len((link['links'])):
print(len)


print(device_flow)
print(len(device_flow['edge_flow']))


# agg_flows = {}
# # print(flows)
# for flow in flows['flows']:
#     # print(flow)
#     key = (flow['ipv4_src_addr'], flow['ipv4_dst_addr'], flow['l4_src_port'], flow['l4_dst_port'])
#     if key not in agg_flows:
#         agg_flows[key] = [flow]
#     else:
#         agg_flows[key].append(flow)

# for key in agg_flows:
#     if len(agg_flows[key]) < 3:
#         pass
#     print('>>>>>>>>>>>>>>>')
#     print('src:{} dst:{} src_port:{} dst_port:{}'.format(*key))
#     print('---------------')
#     for flow in sorted(agg_flows[key], key=lambda x:x['from_ip']):
#         if flow["ipv4_next_hop"] != '0.0.0.0':
#             print(f'\t from_ip:{flow["from_ip"]} next_hop:{flow["ipv4_next_hop"]} in_pkts:{flow["in_pkts"]}')

        # edge_flow : {
        #     edge0 : [{src_ip:, dst_ip:, src_port:, dst_port:}, {}, {}, {}], 
        #     edge1 : []
        # }


        



