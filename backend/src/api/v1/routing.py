from bson.json_util import dumps
from sanic.response import json
from sanic.views import HTTPMethodView


class RoutingView(HTTPMethodView):

    def get(self, request, device_name):
        device_repo = request.app.db['device']
        cr_repo = request.app.db['copied_route']
        _id = device_repo.get_oid_by_name(device_name)
        print(_id[0]['_id'])
        routes = cr_repo.get_by_device_id(_id[0]['_id'])
        # flows = request.app.db['flow_stat'].get_all().sort("in_bytes", -1)
        return json({"routes": routes, "status": "ok"}, dumps=dumps)
