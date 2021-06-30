<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-lg-12 pr-5">
        <VisualizationOptions 
          @sliderUpdate="sliderUpdate"/>
        <hr class="solid">
      </div>
      <div class="col-lg-9 pr-5">      
        <Heatmap 
          :depth_threshold=depth_threshold 
          :frequency_threshold=frequency_threshold 
          :column_width=column_width 
          :segment=segment
          :group=group
          :referenceSequence=referenceSequence
          :data=data
          @changePosition="changePosition"
        >
        </Heatmap>
      </div>
      <div class="col-lg-3 pb-1">
        <MoleculeViewer 
          :segment=segment 
          :position=position
          @changeReferenceSequence="changeReferenceSequence"
          >
        </MoleculeViewer>
        <!-- <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/> -->
        
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator'
import VisualizationOptions from '@/components/VisualizationOptions.vue'
import Heatmap from './Heatmap.vue'
import MoleculeViewer from './MoleculeViewer.vue'
import LocalDataHelper from "@/shared/LocalDataHelper";

@Component({
  components: {
    Heatmap,
    VisualizationOptions,
    MoleculeViewer
  }
})
export default class Visualization extends Vue {
  public depth_threshold = 0
  public frequency_threshold = 0.2
  public column_width = 6
  public segment = 'PB2'
  public position = 54
  public data:any = null
  public group: any[] = []
  public customfile: any = null
  public referenceSequence: any = { positions: [], sequence: [] };
  private localDataHelper = new LocalDataHelper();
  sliderUpdate(gh: {target: string, value: number}) {
    const target = gh.target
    const value = gh.value
    this.$set(this, target, value)
  }
  
  changePosition(value: number){
    this.position = value
  }
  changeReferenceSequence(value: any){
    this.referenceSequence = value
  }  
  
}

</script>

<style scoped lang="scss">
</style>
