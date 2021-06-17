<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-lg-9 pr-5">
        <VisualizationOptions @sliderUpdate="sliderUpdate"/>
        <!-- <hr class="solid"> -->
        <Heatmap 
          :depth_threshold=depth_threshold 
          :frequency_threshold=frequency_threshold 
          :column_width=column_width 
          :segment=segment
          :group=group
          @changePosition="changePosition"
        >
        </Heatmap>
      </div>
      <div class="col-lg-3 pb-6">
        <MoleculeViewer :segment=segment :position=position></MoleculeViewer>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import VisualizationOptions from '@/components/VisualizationOptions.vue'
import Heatmap from './Heatmap.vue'
import MoleculeViewer from './MoleculeViewer.vue'

@Component({
  components: {
    Heatmap,
    VisualizationOptions,
    MoleculeViewer
  }
})
export default class Visualization extends Vue {
  depth_threshold = 0
  frequency_threshold = 0.2
  column_width = 6
  segment = 'NP'
  position = 54
  group = '3C.2 - 3 dpi hNEC'
  sliderUpdate(gh: {target: string, value: number}) {
    const target = gh.target
    const value = gh.value
    this.$set(this, target, value)
  }
  changePosition(value: number){
    this.position = value
  }
  
}

</script>

<style scoped lang="scss">
</style>
