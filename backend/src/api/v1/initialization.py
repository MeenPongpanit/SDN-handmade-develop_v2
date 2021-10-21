import paramiko
import time
from set_snmp import init_snmp_setting
from set_netflow import init_netflow_setting
from bson.json_util import dumps
from sanic.response import json
from sanic.views import HTTPMethodView

from repository import DeviceRepository

class InitializationView(HTTPMethodView):
    def get(self, request):
        # print(request.management_ip)
        device_repo = request.app.db['device']
        devices = device_repo.get_all()
        init_snmp_setting(devices)
        print('snmp init')
        return json({"success": True, "message": "Initialization SNMP Success"})
    def post(self, request):
        print("||||||||||||||||||")
        print(request.json)
        # print(request.data)
        device_repo = request.app.db['device']
        devices = device_repo.get_all()
        if request.json['service'] == 'netflow':
            management_ip = request.json['management_ip']
            init_netflow_setting(devices, management_ip)
            print('netflow init')
            return json({"success": True, "message": "Initialization Net_Flow Success"})
        elif request.json['service'] == 'snmp':
            init_snmp_setting(devices)
            print('snmp init')
            return json({"success": True, "message": "Initialization SNMP Success"})

