<template>
  <div class="row">
    <div class="col-12">
      <form @submit.prevent="onSubmit" method="post">
        <div class="card">
          <div class="card-header">Initialization</div>
          <div class="card-body">
            <div class="row">
              <div class="col-4">
                <div class="form-group">
                  <label for="name" class="form-label">Management IP</label>
                  <input v-model="form.management_ip" type="text" class="form-control" name="management_ip" placeholder="Controller IP">
                </div>
              </div>
            </div>
          </div>
          <div class="card-footer">
            <div class="row">
              <div class="col-md-1">
                <button v-on:click="snmp" type="button" class="btn btn-primary">Set SNMP</button>
              </div>
              <div class="col-md-1">
                <button v-on:click="netflow" type="button" class="btn btn-primary">Set Net_Flow</button>
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import swal from "sweetalert";

export default {
  data() {
    return {
      form: {
        management_ip: ""
      }
    };
  },
  methods: {
    netflow: async function() {
      this.form.service = "netflow"
      const res = await this.$axios.$post("initialization", this.form);
      if (res.success === true) {
        swal("Successful", res.message, "success")
      } else {
        swal("Something went wrong !")
      }
    },
    snmp: async function() {
      this.form.service = "snmp"
      const res = await this.$axios.$get("initialization", this.form);
      if (res.success === true) {
        swal("Successful", res.message, "success")
      } else {
        swal("Something went wrong !")
      }
    }
  }
};
</script>
