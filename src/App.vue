<template>
  <div>
    <img class="navbar-image" src="@/assets/jhu-shield.png"/>
    <NavigationBar/>
    <div class="router-outer container">
      <div class="router-inner columns pt-4">
        <div class="column is-offset-1 is-10">
          <router-view/>
        </div>
      </div>
    </div>
    <footer class="footer">
      <div class="content has-text-centered">
        The work of JHU, JHU/APL, and BARDA. Not sure what content needs to legally be here.
      </div>
    </footer>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import NavigationBar from './components/NavigationBar.vue'

@Component({
  components: {
    NavigationBar
  }
})
export default class App extends Vue {

}

</script>

<style scoped lang="scss">
  .navbar-image {
    max-height: 8rem;
    padding: 1rem 9rem;
  }
  .router-outer {
    display: flex;
    // height of screen - relative height of header + footer
    min-height: calc(100vh - 21.9rem);
    flex-direction: column;
  }
  .router-inner {
    flex: 1;
  }
  .footer {
    height: 3rem;
    width: 100%;
    background-color: $aplgrey2;
    // padding: 1rem;
  }
</style>
