<template>
  <div>
    <div class="container pb-3 pt-3 pl-3">
      <img class="navbar-image" src="@/assets/jhu-shield.png"/>
    </div>
    <nav class="navbar is-aplblue">
      <div class="container">
        <div class="navbar-brand pl-3">
          <router-link class="navbar-item is-size-1" to="/">
            Untitled Data Viz
          </router-link>
          <a role="button" class="navbar-burger" :class="{'is-active': showMenu}" v-on:click="showMenu = !showMenu">
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
          </a>
        </div>
        <div class="navbar-menu navbar-end bg-is-inherited" :class="{'is-active': showMenu}">
          <b-navbar-item class="is-size-4" :class="{'is-active': $route.name === 'Data'}">
            <router-link to="/"> Data </router-link>
          </b-navbar-item>
          <b-navbar-item class="is-size-4" :class="{'is-active': $route.name === 'About'}">
            <router-link to="/about"> About </router-link>
          </b-navbar-item>
        </div>
      </div>
    </nav>
  </div>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'

@Component({})
export default class NavigationBar extends Vue {
  private showMenu = false;
}

</script>

<style scoped lang="scss">
  .navbar-image {
    max-height: 6rem;
  }
  .bg-is-inherited {
    background-color: inherit;
  }
  .navbar-item {
    padding-bottom: 0rem;
    padding-top: 0rem;
  }
  .navbar-burger {
    height: 4.5rem;
    width: 4.5rem;
  }
  a {
    color: white;
  }
  a:hover {
    color: white;
  }
  a.navbar-item:hover {
    background-color: rgba(0,0,0,0.05);
  }
  a.navbar-item.is-active {
    background-color: rgba(0,0,0,0.25);
  }
</style>
