import logging
import socket
import threading
import traceback
from datetime import datetime, timedelta

import repository
import sdn_utils
from netflow.netflow_packet import ExportPacket


class NetflowWorker(threading.Thread):

    def __init__(self, bind_ip, bind_port, active_time=60, inactive_time=20):
        threading.Thread.__init__(self)
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.active_time = active_time
        self.inactive_time = inactive_time
        self.sock = None
        self.stop_flag = False
        self.device = []
        self.daemon = False
        self.flow_stat_repository = repository.FlowStatRepository()
        # Setting thread name
        self.name = 'netflow-sv'

    def run(self):
        """ Create netflow Server
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.bind_ip, self.bind_port))
        logging.info("Netflow server: Listening on interface {}:{}".format(self.bind_ip, self.bind_port))

        _templates = {}

        while not self.stop_flag:
            try:
                (data, sender) = self.sock.recvfrom(8192)

                if data == b'stop':
                    continue

                # logging.info("Received data from {}, length {}".format(sender, len(data)))

                export = ExportPacket(data, _templates)

                # Update templates
                _templates.update(export.templates)

                flows = []
                ended_flows = []
                created_at = sdn_utils.datetime_now()
                packet_datetime = datetime.utcfromtimestamp(export.header.timestamp)
                for flow in export.flows:
                    # Check flow is active or inactive
                    # It updated only is flow is active
                    # Inactive
                    if flow.data['last_switched'] + timedelta(seconds=self.inactive_time) < packet_datetime:
                        flow_type = 'inactive'
                        ended_flows.append(flow.data)
                    # Active
                    else:
                        flow.data['from_ip'] = str(sender[0])
                        flow.data['created_at'] = created_at
                        flows.append(flow.data)
                        flow_type = 'active'

                    # Remove flows are not active
                    # TODO
                
                self.flow_stat_repository.remove_ended_flows(ended_flows)
                self.flow_stat_repository.update_flows(flows)

            except Exception:
                logging.info(traceback.format_exc())

        self.sock.close()
        logging.info("Netflow server: stopped loop")

    def shutdown(self):
        """ Stop netflow Server
        """
        logging.info("Netflow server: shutdown...")
        self.stop_flag = True
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(
            b'stop', (self.bind_ip, self.bind_port)
        )
