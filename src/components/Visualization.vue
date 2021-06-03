<template>
  <b-container>
    <VisualizationOptions @sliderUpdate="sliderUpdate"/>
    <hr class="solid">
    <Heatmap 
      :depth_threshold=depth_threshold 
      :frequency_threshold=frequency_threshold 
      :column_width=column_width 
    >
    </Heatmap>
  </b-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import VisualizationOptions from '@/components/VisualizationOptions.vue'
import Heatmap from './Heatmap.vue'
@Component({
  components: {
    Heatmap,
    VisualizationOptions
  }
})
export default class Visualization extends Vue {
  depth_threshold = 10
  frequency_threshold = 0.2
  column_width = 7
  sliderUpdate(gh: {target: string, value: number}) {
    const target = gh.target
    const value = gh.value
    this.$set(this, target, value)
  }
  
}

</script>

<style scoped lang="scss">
</style>
