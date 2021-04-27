<template>
  <div class="container">
    <NavigationBar/>
    <div class="columns pt-4">
      <div class="column is-offset-1 is-10">
        <router-view/>
      </div>
    </div>
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

</style>
