from repository.repository import Repository
from pymongo import UpdateOne
import netaddr
from bson.objectid import ObjectId


class LinkUtilizationRepository(Repository):
    def __init__(self):
        super(LinkUtilizationRepository, self).__init__()
        self.link = self.db.link_utilization  # Todo deprecated
        self.model = self.db.link_utilization

    def add_links(self, links):
        ops = []
        for link in links:
            ops.append(
                UpdateOne({
                    'src_node_ip': link['src_node_ip'],
                    'src_if_ip': link['src_if_ip'],
                    'dst_node_ip': link['dst_node_ip'],
                    'dst_if_ip': link['dst_if_ip']
                }, {
                    '$set': link
                    # '$set': {
                    #     'src_node_id': link['src_node_id'],
                    #     'dst_node_id': link['dst_node_id'],
                    #     'src_node_ip': link['src_node_ip'],
                    #     'dst_node_ip': link['dst_node_ip'],
                    #     'src_if_ip': link['src_if_ip'],
                    #     'dst_if_ip': link['dst_if_ip'],
                    #     'src_if_index': link['src_if_index'],
                    #     'dst_if_index': link['dst_if_index'],
                    #     'src_in_use': link['src_in_use'],
                    #     'src_out_use': link['src_out_use'],
                    #     'dst_in_use': link['dst_in_use'],
                    #     'dst_out_use': link['dst_out_use'],
                    #     'src_node_hostname': link['src_node_hostname'],
                    #     'dst_node_hostname': link['dst_node_hostname'],
                    #     'link_min_speed': link['link_min_speed']
                    # }
                }, upsert=True)
            )
        if not ops:
            return
        self.link.bulk_write(ops)
    
    def update_running_flows(self):
        for link in self.model.find():
            all_running_flows = self.db.flow_stat.find(
                    {'$or':[{'ipv4_next_hop':link["src_if_ip"]}, {'ipv4_next_hop':link["dst_if_ip"]}]}
                )
            all_running_flows_id = [f['_id'] for f in all_running_flows]    
            self.model.update_one(
                {'$and':[{"src_if_ip":link['src_if_ip']}, {"dst_if_ip":link['dst_if_ip']}]},
                {
                    '$set': {'running_flows':all_running_flows_id}
                }
            )

    def find_by_if_ip(self, ip1, ip2=None):
        if ip2 is None:
            links = self.link.find({
                '$or': [
                    {'src_if_ip': ip1},
                    {'dst_if_ip': ip1}
                ]
            })
            return links

        ip1 = netaddr.IPAddress(ip1)
        ip2 = netaddr.IPAddress(ip2)

        if ip1 == ip2:
            raise ValueError("Src IP can't equal Dst IP")

        if ip1 > ip2:
            ip1, ip2 = ip2, ip1

        link = self.link.find_one({
            'src_if_ip': str(ip1),
            'dst_if_ip': str(ip2)
        })
        return link

    def find_by_if_index(self, mgmt_ip, index):
        link = self.link.find({
            '$or': [
                {'src_node_ip': mgmt_ip, 'src_if_index': index},
                {'dst_node_ip': mgmt_ip, 'dst_if_index': index}
            ]
        })
        return link

    def find_by_id(self, id):
        return self.link.find_one({'_id': ObjectId(id)})

    def get_all(self):
        self.update_running_flows()
        return self.link.find()

    def get_by_id(self, id):
        self.update_running_flows()
        return self.link.find({'_id': ObjectId(id)})

    def get_by_name(self, name):
        self.update_running_flows()
        self.model.create_index([('src_node_hostname', 'text'), ('dst_node_hostname', 'text')])
        return self.model.find({'$text':{'$search': name}})
