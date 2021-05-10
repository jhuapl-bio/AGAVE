<template>
  <div>
    <p>
      The visualization will go here
    </p>
    <Heatmap></Heatmap>
  </div>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'
import Heatmap from './Heatmap.vue'
@Component({
  components: {
    Heatmap
  }
})
export default class Visualization extends Vue {
}

</script>

<style scoped lang="scss">
</style>
