<template>
  <div class="row">
    <div class="col-sm-12 col-md-12">
      <div class="card">
        <div class="card-header">
          Network graph
        </div>
        <div class="card-body">
          <network-graph :nodes="graphNode" :edges="graphEdge" @click="onClick" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NetworkGraph from "@/components/NetworkGraph.vue";
import * as jsnx from "jsnetworkx";
import ipaddrMixin from "@/mixins/ipaddr";



export default {
  data() {
    return {
      mode: "findpath",
      graph: null,
      node_label: "hostname",
      graphRawData: null,
      nodes_: {},
      graphNode: [],
      graphEdge: [],
      interval: null,
      eventName: "",
      information: "",
      selectEdge: ["192.168.2.0-192.168.2.1", "192.168.2.2-192.168.2.3"],
      nodeSelect: [],
      highlightNode: [],
      networks: [],
      mask:[],
      routes: [],
      devices: [],
      check:[],
      network_in_link: [],
      links: [],
      checkGraphEdge: [],
      neighbor: [],
      network_in_graph : [],
      edges : [],
      net : []
    };
  },
  components: {
    NetworkGraph
  },
  mixins: [ipaddrMixin],
  async mounted(){
    await this.fetchData();
  },
  methods: {
    async onClick(param) {
      this.eventName = "onClick"
      this.information = param
      if (this.mode == "findpath") {
        if (this.nodeSelect.length >= 2) {
          this.nodeSelect = [];
        }
        this.highlightNode = [];
        if (param.nodes.length < 1) {
          this.updateGraph();
          return;
        }
        this.nodeSelect.push(param.nodes[0]);
        // this.highlightNode = [];
        if (this.nodeSelect.length == 2) {
          const rawData = await this.$axios.$get(
            `path/${this.nodeSelect[0]},${this.nodeSelect[1]}`
          );
          this.highlightNode = rawData.paths;
        }
        this.updateGraph();
        // await this.$axios.$get("path/" + ip);
        return;
      }
      const info = param;
      if (param.nodes) {
        const ip = param.nodes[0];
        const device = await this.$axios.$get("device/ifip/" + ip);
        info["device"] = device;
      }
      this.eventName = "onClick";
      this.information = JSON.stringify(info, null, 2);
    },
    calculate_usage_percent(src_usage, dst_usage, speed) {
      return Math.max(src_usage, dst_usage) / speed * 100;
    },
    async fetchGraph() {
      this.neighbor = [];
      try {
        let res = await this.$axios.$get("device");
        this.devices = res.devices;
        res = await this.$axios.$get("link");
        this.links = res.links;
        let res2;
        let device;
        for (var i = 0; i < this.devices.length; i++) {
          device = this.devices[i];
          res2 = await this.$axios.$get(`routes/${device._id.$oid}`);
          if (res2) {
            this.routes.push(res2.routes);
          }
        }
        for (var i = 0; i < this.devices.length; i++) {
          device = this.devices[i];
          res2 = await this.$axios.$get(`device/${device._id.$oid}/neighbor`);
          if (res2) {
            this.neighbor.push(res2.neighbor);
          }
        }
        this.getNetwork();
      } catch (e) {}
      this.form = {
        ...this.propForm
      };
      this.graphRawData = await this.$axios.$get("link");
      this.updateGraph();
    },
    getNetwork() {
      for (var i = 0; i < this.routes.length; i++) {
       for (var j = 0; j < this.routes[i].length; j++) {
         if (this.networks.indexOf(this.routes[i][j].dst) < 0 && this.routes[i][j].dst != "0.0.0.0" && this.routes[i][j].mask != "255.255.255.255" && this.routes[i][j].if_index != 0) {
            this.networks.push(this.routes[i][j].dst);
            this.mask.push(this.subnetToCidr(this.routes[i][j].mask));
          }
        }
      }
    },
    hex_to_int(hex){
      return parseInt(hex, 16);
    },
    check_switch(hex){
      //alert(hex);
      if (this.hex_to_int(hex)%2 == 0){
        //alert ("switch");
        return true;
      }
      else if (hex.includes("Switch") && !hex.includes("Router")){
        //alert ("switch");
        return true;
      }
      else{
        //alert("Router");
        return false;
      }
    },
    getNetworkFromIP(ip, mask) {
      //alert(ip+", "+mask);
      var check = "";
      ip = ip.split(".");
      mask = mask.split(".");
      for (var i=0; i < mask.length; i++) {
        if (mask[i] != "255") {
          ip [i] = parseInt(ip[i], 10).toString(2).padStart(8, "0");
          mask[i] = parseInt(mask[i], 10).toString(2).padStart(8, "0");
          for (var j=0; j < mask[i].length; j++){
            if (mask[i][j] == "0") {
              check += "0";
            } else {
              check += ip[i][j];
            }
          }
          ip[i] = parseInt(check, 2);
        }
      }
      return ip.join(".");
    },
    count(list, check) {
      var count = 0;
      for (var i=0; i < list.length; i++) {
        if (list[i] == check) {
          count = count +1;
        }
      }
      return count;
    },
    getNetworkInLink() {
      for (var i=0; i < this.links.length; i++) {
        for (var a=0; a<this.devices.length; a++) {
          if (this.devices[a]._id.$oid == this.links[i].src_node_id.$oid || this.devices[a]._id.$oid == this.links[i].dst_node_id.$oid) {
            for (var b=0; b<this.devices[a].interfaces.length; b++) {
              if (this.links[i].src_ip == this.devices[a].interfaces[b].ipv4_address){
                this.network_in_link.push(this.getNetworkFromIP(this.links[i].src_ip, this.devices[a].interfaces[b].subnet));
              }
            }
          }
        }
      }
    },
    findInterfaces(src_node_id, dst_node_id, ip) {
      for (var a=0; a<this.devices.length; a++) {
        if (this.devices[a]._id.$oid == src_node_id.$oid || this.devices[a]._id.$oid == dst_node_id.$oid) {
          for (var b=0; b<this.devices[a].interfaces.length; b++) {
            if (ip == this.devices[a].interfaces[b].ipv4_address){
              return this.devices[a].interfaces[b];
            }
          }
        }
      }
    },
    getNetworkFromInterface(device_ip, interface_index) {
      for (var i=0; i < this.devices.length; i++){
        if (this.devices[i].device_ip == device_ip) {
          return this.getNetworkFromIP(this.devices[i].interfaces[interface_index-1].ipv4_address, this.devices[i].interfaces[interface_index-1].subnet);
        }
      }
    },
    not_in(net, edges){
      for (var i=0; i<edges.length; i++){
        if (edges[i][1] == net){
          return false;
        }
      }
      return true;
    },
    updateGraph() {
      this.network_in_link = [];
      this.getNetworkInLink();
      if (this.graphRawData.links) {
        this.network_in_graph = [];
        this.net = [];
        this.edges = [];
        this.graphEdge = [];
        this.graphNode = [];
        this.check = [];
        let nodes_ = {};
        let id = 1;
        // Max - Min in API
        this.graphRawData.links.forEach((link, i) => {
          // Calculate link usage
          const speed = this.calculate_usage_percent(
            Math.max(link.src_in_use, link.src_out_use),
            Math.max(link.dst_in_use, link.dst_out_use),
            link.link_min_speed
          );
          let color;
          if (speed < 50) {
            color = "rgb(144, 238, 144)";
          } else if (speed < 85) {
            color = "rgb(255, 165, 0)";
          } else {
            color = "rgb(255, 0, 0)";
          }
          const edgeId = `${link.src_if_ip}-${link.dst_if_ip}`;
          // Todo Fix highlight edges
          this.highlightNode.forEach(node => {
            if (
              node.indexOf(link.src_node_ip) > -1 ||
              node.indexOf(link.dst_node_ip) > -1
            ) {
              color = "rgb(0, 0, 153)";
            }
          });
          var ifaces = this.findInterfaces(link.src_node_id, link.dst_node_id, link.src_ip);
          const edge = {
            from: link.src_node_ip,
            to: link.dst_node_ip,
            width: link.link_min_speed / 400000,
            // value: link.src_in_use + link.dst_in_use,
            label: this.getNetworkFromIP(link.src_ip, ifaces.subnet)+"/"+ this.subnetToCidr(ifaces.subnet) +"("+ `${speed.toFixed(2)}%` + ")",
            id: edgeId,
            color: { color, highlight: color }
          };
          if (link.link_min_speed > 1544000) {
            edge.width = 1544000 /400000;
          }
          if (link.src_ip != link.dst_ip){
            this.check.push(this.getNetworkFromIP(link.src_ip, ifaces.subnet));
            //alert(link.src_ip +", "+ link.dst_ip);
            if (this.count(this.network_in_link, this.getNetworkFromIP(link.src_ip, ifaces.subnet)) <= 1 && ifaces.admin_status == 1 && ifaces.operational_status == 1) {
              this.graphEdge.push(edge);
              this.graph.addEdge(link.src_node_ip, link.dst_node_ip);
            }
          }
          if (!nodes_[link.src_node_ip]) {
            let label;
            switch (this.node_label) {
              case "hostname":
                label = link.src_node_hostname;
                break;
            }
            nodes_[link.src_node_ip] = {
              id: link.src_node_ip,
              value: 1,
              label: label
            };
            id++;
          }
          if (!nodes_[link.dst_node_ip]) {
            let label;
            switch (this.node_label) {
              case "hostname":
                label = link.dst_node_hostname;
                break;
            }
            nodes_[link.dst_node_ip] = {
              id: link.dst_node_ip,
              value: 1,
              label: label
            };
            id++;
          }
        });
        // show switch
        for (var i=0; i < this.neighbor.length; i++){
          for (var j=0; j< this.neighbor[i].length; j++){
            if (this.check_switch(this.neighbor[i][j].capabilities)){
              //alert(!this.neighbor[i][j].capabilities.includes("Router"));
              let label = this.neighbor[i][j].name;
              nodes_[this.neighbor[i][j].name] = {
                id: this.neighbor[i][j].name,
                value: 1,
                label: label,
                color: "#FFFF80"
              };
              id++;
              for (var a=0; a<this.devices.length; a++){
                if (this.devices[a].device_ip == this.neighbor[i][j].device_ip){
                  var ifaces = this.devices[a].interfaces[this.neighbor[i][j].local_ifindex-1];
                  // Calculate link usage
                  const speed = this.calculate_usage_percent(
                    ifaces.bw_in_usage_persec,
                    ifaces.bw_out_usage_persec,
                    ifaces.speed
                  );
                  let color;
                  if (speed < 50) {
                    color = "rgb(144, 238, 144)";
                  } else if (speed < 85) {
                    color = "rgb(255, 165, 0)";
                  } else {
                    color = "rgb(255, 0, 0)";
                  }
                  const edge = {
                    from: this.neighbor[i][j].name,
                    to: this.neighbor[i][j].device_ip,
                    id: this.neighbor[i][j].name+this.neighbor[i][j].device_ip,
                    label: this.getNetworkFromIP(ifaces.ipv4_address, ifaces.subnet)+"/"+this.subnetToCidr(ifaces.subnet) +"("+ `${speed.toFixed(2)}%` + ")",
                    color: { color, highlight: color },
                    width: 1544000 / 400000
                  }
                  if (this.graphEdge.map(function(e) { return e.id; }).indexOf(edge.id) < 0) {
                    this.graphEdge.push(edge);
                    this.graph.addEdge(this.neighbor[i][j].name, this.neighbor[i][j].device_ip);
                    this.edges.push([this.neighbor[i][j].device_ip, this.getNetworkFromIP(ifaces.ipv4_address, ifaces.subnet)]);
                  }
                }
              }
            }
          }
        }
        // show network
        for (var i=0; i < this.networks.length; i++){
          if ((!nodes_[this.networks[i]] && this.check.indexOf(this.networks[i]) < 0)||(this.count(this.network_in_link, this.networks[i]) > 2)){
            let label = this.networks[i]+"/"+this.mask[i];
            nodes_[this.networks[i]] = {
              id: this.networks[i],
              value: 1,
              label: label,
              color: "#FFF"
            };
            id++;
            for (var j=0; j < this.neighbor.length; j++){
              for (var k=0; k < this.neighbor[j].length; k++){
                if (this.check_switch(this.neighbor[j][k].capabilities)){
                  let color = "rgb(144, 238, 144)";
                  var network = this.getNetworkFromInterface(this.neighbor[j][k].device_ip, this.neighbor[j][k].local_ifindex);
                  this.network_in_graph.push(network);
                  const edge = {
                    from: network,
                    to: this.neighbor[j][k].name,
                    id: network+this.neighbor[j][k].name,
                    color: { color, highlight: color },
                    width: 1544000 / 400000
                  }
                  if (this.graphEdge.map(function(e) { return e.id; }).indexOf(edge.id) < 0) {
                    this.net.push(network);
                    this.graphEdge.push(edge);
                    this.graph.addEdge(network, this.neighbor[j][k].name);
                  }
                }
              }
            }
            if (!this.network_in_graph.includes(this.networks[i])){
              for (var j=0; j < this.devices.length; j++) {
                for (var k=0; k < this.devices[j].interfaces.length; k++) {
                  if (this.devices[j].interfaces[k].ipv4_address) {
                    //this.edges = JSON.stringify(this.edges);
                    //var check_edge = JSON.stringify([this.devices[j].interfaces[k].device_ip, this.networks[i]]);
                    //alert(this.edges.indexOf(check_edge) === -1);
                    for (var a=0; a<this.edges.length; a++){
                      //alert(this.edges[a]);
                      if ((this.devices[j].interfaces[k].device_ip == this.edges[a][0] && this.networks[i] == this.edges[a][1]) || this.not_in(this.networks[i], this.edges)){
                        if(this.getNetworkFromIP(this.devices[j].interfaces[k].ipv4_address, this.devices[j].interfaces[k].subnet) == this.networks[i] /*&& this.edges.indexOf(check_edge) === -1*/) {
                        var ifaces = this.devices[j].interfaces[k];
                        // Calculate link usage
                        const speed = this.calculate_usage_percent(
                          ifaces.bw_in_usage_persec,
                          ifaces.bw_out_usage_persec,
                          ifaces.speed
                        );
                        let color;
                        if (speed < 50) {
                          color = "rgb(144, 238, 144)";
                        } else if (speed < 85) {
                          color = "rgb(255, 165, 0)";
                        } else {
                          color = "rgb(255, 0, 0)";
                        }
                        const edge = {
                          from: this.devices[j].interfaces[k].device_ip,
                          to: this.networks[i],
                          id: this.devices[j].interfaces[k].device_ip+this.networks[i],
                          label: this.networks[i]+"/"+this.subnetToCidr(ifaces.subnet) +"("+ `${speed.toFixed(2)}%` + ")",
                          color: { color, highlight: color },
                          width: 1544000 / 400000
                        }
                        if (this.graphEdge.map(function(e) { return e.id; }).indexOf(edge.id) < 0 && !this.network_in_graph.includes(this.networks[i])) {
                          this.net.push(this.networks[i]);
                          this.graphEdge.push(edge);
                          this.graph.addEdge(this.devices[j].interfaces[k].device_ip, this.networks[i]);
                        }
                      }
                      }
                    }
                    
                  }
                }
              }
            }
          }
        }
        //delete node not use
        for (var i=0; i<this.devices.length; i++){
          if (!this.devices[i].is_ssh_connect){
            for (var j=0; j<this.neighbor.length; j++){
              for (var k=0; k<this.neighbor[j].length; k++){
                if (this.check_switch(this.neighbor[j][k].capabilities)
                 && this.neighbor[j][k].device_ip == this.devices[i].device_ip){
                  delete nodes_[this.neighbor[j][k].name];
                }
              }
            }
            for (var j=0; j<this.devices[i].interfaces.length; j++){
              if (this.devices[i].interfaces[j].ipv4_address){
                delete nodes_[this.getNetworkFromIP(this.devices[i].interfaces[j].ipv4_address, this.devices[i].interfaces[j].subnet)];
              }
            }
            delete nodes_[this.devices[i].device_ip];
          }
        }
        //alert(this.edges.length);
        for (var i=0;i<this.networks.length;i++){
          if (!this.net.includes(this.networks[i])){
            delete nodes_[this.networks[i]];
          }
        }
        //alert(this.networks);
        //alert(this.network_in_graph);
        this.nodes_ = nodes_;
        this.graphNode = Object.values(nodes_);
        if (this.checkGraphEdge.length == 0) {
          this.checkGraphEdge = this.graphEdge;
        }
        else if (this.checkGraphEdge.length != this.graphEdge.length) {
          //alert(this.checkGraphEdge.length+"  "+this.graphEdge.length);
          location.reload();
        }
        else {
          for (var i=0;i<this.graphEdge.length;i++) {
            if (this.graphEdge[i].from != this.checkGraphEdge[i].from || this.graphEdge[i].to != this.checkGraphEdge[i].to) {
              //alert(this.checkGraphEdge.length+"  "+this.graphEdge.length);
              location .reload();
            }
          }
        }
      }
    }
  },
  async mounted() {
    // console.log(jsnx)
    this.graph = new jsnx.Graph();
    this.interval = setInterval(() => this.fetchGraph(), 5000);
    try {
      let res = await this.$axios.$get("device");
      this.devices = res.devices;
      res = await this.$axios.$get("link");
      this.links = res.links;
      let res2;
      let device;
      for (var i = 0; i < this.devices.length; i++) {
        device = this.devices[i];
        res2 = await this.$axios.$get(`routes/${device._id.$oid}`);
        if (res2) {
          this.routes.push(res2.routes);
        }
      }
      for (var i = 0; i < this.devices.length; i++) {
        device = this.devices[i];
        res2 = await this.$axios.$get(`device/${device._id.$oid}/neighbor`);
        if (res2) {
          this.neighbor.push(res2.neighbor);
        }
      }
      this.getNetwork();
    } catch (e) {}
    this.form = {
      ...this.propForm
    };
  },
  beforeDestroy() {
    clearInterval(this.interval);
  }
};
</script>
