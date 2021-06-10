<template>
  <div>
    
    <NavigationBar/>
    <div class="router-outer container">
      <div class="router-inner columns pt-4">
        <div class="column is-offset-1-mobile add-padding">
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
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
@Component({
  components: {
    NavigationBar
  }
})
export default class App extends Vue {

}

</script>

<style scoped lang="scss">
  .router-outer {
    display: flex;
    // height of screen - relative height of header + footer
    min-height: calc(100vh - 21.4rem);
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
  .add-padding {
    padding-left: 30px;
    padding-right: 30px;
  }
</style>
