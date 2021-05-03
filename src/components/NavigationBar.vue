<template>
  <b-navbar type="is-primary">
    <template #brand>
      <b-navbar-item class="navbar-item is-size-1" :to="{path: '/'}">
        Untitled Data Viz
      </b-navbar-item>
    </template>
    <template #end>
        <b-navbar-item class="is-size-4">
          <router-link to="/"> Data </router-link>
        </b-navbar-item>
        <b-navbar-item class="is-size-4">
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

<style scoped lang="scss">
  .navbar {
    padding-left: 8rem;
    padding-right: 8rem;
  }
  .navbar-item {
    padding-bottom: 0rem;
    padding-top: 0rem;
  }
  a {
    color: white;
  }
  a:hover {
    color: white;
  }
</style>
