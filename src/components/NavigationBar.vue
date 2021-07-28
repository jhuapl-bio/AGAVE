<template>
<b-navbar centered style="color: white;" class="navbar is-aplblue" role="navigation" aria-label="main navigation">
    <div id="navbarBasicExample" class="navbar-menu">
      <h1 class="navbar-item is-size-3" style="">
        <span v-for="n in name"
        v-bind:key="n"
        @mouseover="showTitleFull = true" @mouseleave="showTitleFull=false"
        style="color: #fff; cursor: default">
          {{n.substring(0,1)}}
        </span>
        <transition name="slide-fade">
          <div style="display:flex" v-if="showTitleFull">
            <div >
              <span v-for="n in name"
                v-bind:key="n"
                style="color: #fff;">
                <small style="font-size: 14px">{{n}} </small>
              </span> 
            </div>
          </div>
        </transition> 
      </h1>
    <div class="navbar-start">
      <a id="logo" class="navbar-item force-center" href="https://jhu.edu">
        <img class="navbar-image" src="@/assets/images/apl.logo.large.horizontal.white.svg"/>
      </a>
    </div>
    <div class="navbar-end">
      <a class="navbar-item" style="opacity: 0.0;">
        About
      </a>
    </div>
  </div>
       
  </b-navbar>
  <!-- <div style="">
    <nav class="navbar is-aplblue" centered>
      <div class="navbar-brand">
        <h1 class="navbar-item is-size-3" style="">
          <span v-for="n in name"
          v-bind:key="n"
          @mouseover="showTitleFull = true" @mouseleave="showTitleFull=false"
          style="color: #fff; cursor: default">
            {{n.substring(0,1)}}
          </span>
          <transition name="slide-fade">
            <div style="display:flex" v-if="showTitleFull">
              <div >
                <span v-for="n in name"
                  v-bind:key="n"
                  style="color: #fff;">
                  <small style="font-size: 14px">{{n}} </small>
                </span> 
              </div>
            </div>
          </transition> 
        </h1>
      </div>
      <div class="navbar-image is-size-1" style="">
            <a href="https://jhu.edu" >
              <img class="navbar-image" src="@/assets/images/apl.logo.small.horizontal.white.svg"/>
            </a>
            
        </div>
    </nav>
    
  </div> -->
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
    max-height: 16rem;
    min-height: 6rem;
    padding-top: 0;
    padding-bottom: 0;
  }
  .navbar, .navbar-brand, .navbar-item, .navbar-image{
    padding-top: 0px;
    padding-bottom: 0px;
    text-align: center;
  }

  .navbar-start{
    flex-grow: 1;
    justify-content: center;
    text-align: center;
  }

  @media screen and (max-width: $desktop - 1px){
      #logo{
          display: none;
      }
      .force-center{
          position: absolute;
          left: 50%;
          transform: translateX(-50%);
      }
      .navbar-end{
          display: flex;
          justify-content: center;
      }
  }

  @media screen and (min-width: $desktop){
      .navbar-brand{
          display: none;
      }
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
