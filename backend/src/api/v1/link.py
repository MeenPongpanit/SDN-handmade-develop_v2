from bson.json_util import dumps
from sanic.response import json
from sanic.views import HTTPMethodView


class LinkView(HTTPMethodView):

    def get(self, request, _id=None):  
        if _id is None:
            links = request.app.db['link_utilization'].get_all()
            return json({"links": links, "status": "ok"}, dumps=dumps)
        elif len(_id) == 24:
            link = request.app.db['link_utilization'].get_by_id(_id)
            return json({"link": link, "status": "ok"}, dumps=dumps)
        link = request.app.db['link_utilization'].get_by_name(_id)
        return json({"link": link, "status": "ok"}, dumps=dumps)

