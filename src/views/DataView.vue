<template>
  <div>
    <VisualizationOptions/>
    <hr class="solid">
    <Visualization/>
  </div>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'
import VisualizationOptions from '@/components/VisualizationOptions.vue'
import Visualization from '@/components/Visualization.vue'

@Component({
  components: {
    VisualizationOptions,
    Visualization
  }
})
export default class DataView extends Vue {

}

</script>

<style scoped>
  .solid {
      border-top: 2px
  }
</style>
