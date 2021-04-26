<template>
  <b-navbar shadow>
    <template #brand>
      <b-navbar-item class="navbar-item is-size-1 has-text-weight-semibold" :to="{path: '/'}">
        BARDA
      </b-navbar-item>
    </template>
    <template #end>
        <b-navbar-item active class="is-size-4 has-text-weight-semibold">
          <router-link to="/"> Data </router-link>
        </b-navbar-item>
        <b-navbar-item class="is-size-4 has-text-weight-semibold">
          <router-link to="/about"> About </router-link>
        </b-navbar-item>
    </template>
  </b-navbar>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'

@Component({})
export default class NavigationBar extends Vue {

}

</script>

<style scoped>
  .navbar {
    padding-left: 4em;
    padding-right: 4em;
  }
</style>
