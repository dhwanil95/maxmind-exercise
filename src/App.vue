<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <h3>IP Address Lookup</h3>
      </div>

      <v-spacer></v-spacer>

      </v-app-bar>

    <v-main>
      <LookupPage/>
    </v-main>
  </v-app>
</template>

<script>
import LookupPage from './components/LookupPage';

export default {
  name: 'App',

  components: {
    LookupPage,
  },

  data: () => ({
    //
  }),
};
</script>
