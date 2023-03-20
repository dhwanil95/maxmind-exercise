<template>
  <div>
    <div>
      <v-card style="align-self: center;">
          <v-card-text>
            <div class="ml-8" v-for="(ipAddress, index) in ipAddresses" :key="index">
              <v-row>
                <v-col class="expand-col">
                  <v-btn
                    class="justify-right"
                    color="primary"
                    prepend-icon
                    dense
                    text
                    @click="openToggle(ipAddresses, index)"
                  >
                    <v-icon medium class="mr-0" v-if="ipAddresses[index].expanded === true">mdi-chevron-down</v-icon>
                    <v-icon medium class="mr-0" v-else>mdi-chevron-right</v-icon>
                  </v-btn>
                </v-col>
                <v-col class="ip-input-col">
                  <div>
                    <v-text-field
                      hide-details
                      outlined
                      dense
                      :value="ipAddress"
                      class="p-0 mb-3 ip-address-field"
                      v-model="ipAddresses[index].value"
                      :error="ipAddresses[index].errorMessage != ''"
                      placeholder="Enter IP Address"
                    >
                    </v-text-field>
                    <div v-if="ipAddresses[index].errorMessage.length > 0">
                       {{  ipAddress.errorMessage }}
                    </div>
                    <div v-if="ipAddresses[index].expanded">
                      <div class="result">
                        <div class="details">
                          <template v-if="result[index]">
                            <p v-if="result[index].country_code"><b>Country Code:</b> {{ result[index].country_code }}</p>
                            <p v-if="result[index].postal_code"><b>Postal Code:</b> {{ result[index].postal_code }}</p>
                            <p v-if="result[index].city_name"><b>City Name:</b> {{ result[index].city_name }}</p>
                            <p v-if="result[index].time_zone"><b>Time Zone:</b> {{ result[index].time_zone }}</p>
                            <p v-if="result[index].accuracy_radius"><b>Accuracy Radius:</b> {{ result[index].accuracy_radius }}</p>
                          </template>
                          <template v-else>
                            <p>No result for given IP</p>
                          </template>
                        </div>
                      </div>
                    </div>
                  </div>
                </v-col>
                <v-col class="delete-col">
                  <v-btn
                    class="justify-right"
                    color="primary"
                    prepend-icon
                    dense
                    text
                    @click="removeIPAddress(index)"
                  >
                    <v-icon medium class="mr-0">mdi-trash-can</v-icon>
                  </v-btn>  
                </v-col>
              </v-row>
            </div>
            <div v-if="this.noInputIp">
              <p>Please add atleast one IP Address</p>
            </div>
            <div class="ml-8 mr-0">
              <v-row class="pl-4">
                <v-col class="add-button">
                  <v-btn @click="addIPAddress()" small text color="primary" class="p-0">
                  Add IP Address<v-icon>mdi-plus</v-icon>
                  </v-btn>
                </v-col>
              </v-row>
              <v-row>
                <v-col class="text-left pt-0 ml-2 mb-6">
                  <v-btn  color="primary" class="lookup-button ml-10" @click="performLookup()">Look up</v-btn>
                </v-col>
              </v-row>
            </div>
          </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      ipAddresses: [{
         value: '', // Intially one input field with empty value
         expanded: false, // Initally input field is not expanded
         errorMessage: '' 
       }],
      result: [],
      noInputIp: false,
    }
  },
  methods: {
    // check if IP address is valid or not
    validateIPAddress(ipAddress) {
      // Regular expression to match an IPv4 address
      const regex = /^(\d{1,3}\.){3}\d{1,3}$/;
      return regex.test(ipAddress.value)
    },

    // Add new Ip Address
    addIPAddress() {
      this.ipAddresses.push({ 
        value: '', 
        expanded: false,
        errorMessage:''
      })
    },

    // Remove existing Ip address and remove its data from result if exsits
    removeIPAddress(index) {
      this.ipAddresses.splice(index, 1)
      if (this.result[index]) {
        this.result.splice(index, 1)
      }
    },

    // Expand the result while clicking on the button
    openToggle(ipAddresses,index){
      if(ipAddresses[index].expanded === true){
        this.ipAddresses[index].expanded = false;
      }
      else{
        this.ipAddresses[index].expanded = true;
      }
    },

    // Perform the look up  for Input Ip
    async performLookup() {

      // check if any ip address exists or not
      if(this.ipAddresses.length < 1){
        this.noInputIp = true
      }
      else{
        this.noInputIp = false
      }

      // send error message if IP address format is invalid
      for (const ipAddress of this.ipAddresses) {
        if (!this.validateIPAddress(ipAddress)) {
          ipAddress.errorMessage = "Please Enter valid IP Address";
          return; // return from the function if IP address is invalid
        } else {
          ipAddress.errorMessage = "";
        }
        ipAddress.expanded = true;
      }

      // Extract a list of IP addresses that don't already have results
      const newIpAddressList = this.ipAddresses
        .filter((ipAddress, index) => !this.result[index])
        .map(ipAddress => ipAddress.value)

      // Get the index values of the changed IP addresses
      const changedIpAddressList = this.ipAddresses
        .filter((ipAddress, index) => (this.result[index] && ipAddress.value !== this.result[index].ip_address))
        .map((ipAddress, index) => index);

      // Get the IP addresses of the changed IP addresses
      const changedIpAddresses = changedIpAddressList.map(index => this.ipAddresses[index].value);

      if (changedIpAddresses.length > 0) {
        try {
          const response = await axios.post('http://127.0.0.1:5000/geolocation', { ip_addresses: changedIpAddresses });
         
          // Update the results for the changed IP addresses
          response.data.forEach((newResult) => {
            const index = this.ipAddresses.findIndex(ipAddress => ipAddress.value === newResult.ip_address);
            if (index >= 0) {
              this.result[index] = newResult;
            }
          });
        } catch (error) {
          console.error(error);
        }
      }

      if ( newIpAddressList.length > 0){
        try{
          const response = await axios.post('http://127.0.0.1:5000/geolocation', { ip_addresses: newIpAddressList })
          // Merge the new results with the existing results
          const newResults = response.data
          this.result = [...this.result, ...newResults]
          } catch (error) {
          console.error(error)
      }
    }
  }
  }
}
</script>
<style lang="less" scoped>
  .ip-input-col {
    max-width: 450px; 
  }
  .delete-col {
    margin-left: 0px; 
  }

  .expand-col{
    max-width: 100px;
  }
  
  .add-button{
    margin-bottom: 10px;
    margin-left: 5%;
  }

  .result{
    border-bottom: 1px solid grey;
    border-left: 1px solid grey;
    border-right: 1px solid grey;
  }

  .details{
    margin-left: 10px;
  }
  @media (max-width: 640px) {
    .ml-8{
      margin-left: 0% !important;
    }

    .expand-col{
      margin-left: -20px;
    }
    .lookup-button {
      width: 80%;
      margin-left: 5% !important;
    }
    .delete-col {
      margin-right: -150px !important;
    }
  }
  @media only screen and (max-width: 600px) {
    .ip-input-col {
      width: 100%;
      margin-left: -35px !important;
    }
  }
</style>