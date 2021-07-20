<template>
  <div>
    <div class=" pb-3 pt-3 left-padding">
      <a href="https://jhu.edu">
        <img class="navbar-image" src="@/assets/images/jhu-shield.png"/>
      </a>
    </div>
    <nav class="navbar is-aplblue">
      <div class="navbar-title">
        <div class="navbar-brand pl-3">
          <h1 class="navbar-item is-size-2">
            <!-- {{name.join(" ")}} -->
            
            <span v-for="n in name"
            v-bind:key="n"
            style="color: #fff;"
            >
            <p style="font-size: 1.2em; ">
              <strong style="color: #fff;">{{n.substring(0,1)}}</strong><small style="font-size: 14px">{{n.substring(1,n.length)}}</small>
            </p> 
            

            </span>
            <!-- <div style="display:block">
            <span v-for="n in name"
            v-bind:key="n"
            style="color: #fff; cursor: default"
            @mouseover="showTitleFull = true" @mouseleave="showTitleFull=false"
            >
              <strong style="color: #fff">{{n.substring(0,1)}}
              </strong>
            </span>
            <transition name="fade">
              <p style="font-size: 12px" v-if="showTitleFull">{{name.join("")}}</p>
            </transition>
            </div> -->
            <!-- <div style="display:block; font-size: 12px;">
            <span v-for="n in name"
            v-bind:key="n"
            style="color: #fff; font-size: 29px; cursor: default"
            >
              {{n.substring(0,1)}}
            </span>
            <hr>
            {{name.join("")}}
            </div> -->



          </h1>
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
  public showTitleFull = false;
  public name: string[] = ['Automated', 'Genomics', 'Application for', 'Variant', 'Exploration']
}

</script>

<style scoped lang="scss">
  .navbar-image {
    max-height: 6rem;
    padding-left: 6rem
  }
  .navbar-title {
    padding-left: 4rem;
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
  .fade-enter-active, .fade-leave-active {
    transition: opacity .5s;
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
  }
</style>
