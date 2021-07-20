<template>
  <div style="">
    <nav class="navbar is-aplblue" style="">
      <div class="navbar-title" style="width: 100%">
        <div class="navbar-brand pl-3">
          <div class="navbar-image is-size-2" style="float:right">
            <a href="https://jhu.edu" >
              <img class="navbar-image" src="@/assets/images/apl.shield.large.white.svg"/>
            </a>
            
          </div>
          <h1 class="navbar-item is-size-2" style="float:left">
            <!-- {{name.join(" ")}} -->
            <div class="vertical">
            </div>
            <span v-for="n in name"
            v-bind:key="n"
            @mouseover="showTitleFull = true" @mouseleave="showTitleFull=false"
            style="color: #fff; cursor: default">
              {{n.substring(0,1)}}
              <!-- <strong style="color: #fff;">{{n.substring(0,1)}}</strong><small style="font-size: 14px">{{n.substring(1,n.length)}}</small> -->
            </span>
            <transition name="slide-fade">
              <div style="display:flex" v-if="showTitleFull">
                <div class = "vertical" >
                </div>
                <div >
                  <span v-for="n in name"
                    v-bind:key="n"
                    style="color: #fff;">
                    <small style="font-size: 14px">{{n}} </small>
                  </span> 
                </div>
              </div>
              
            </transition> 
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
    padding-top: 0;
    padding-bottom: 0;
    // padding-left: 6rem;
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
  nav {
    display:block
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
  .vertical {
      border-left: 2px solid #fff;
      height: 100%;
      padding-left: 10px;
      margin-left: 10px;
      vertical-align: baseline;
  }
  .slide-fade-enter-active {
    transition: all .2s ease;
  }
  .slide-fade-leave-active {
    transition: all .3s cubic-bezier(1.0, 0.5, 0.3, 0.8);
  }
  .slide-fade-enter, .slide-fade-leave-to
  /* .slide-fade-leave-active below version 2.1.8 */ {
    transform: translateX(10px);
    opacity: 0;
  }
</style>
