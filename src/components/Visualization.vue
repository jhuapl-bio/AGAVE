<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-lg-12 pr-5">
        <VisualizationOptions 
          :referenceSequence=referenceSequence
          @sliderUpdate="sliderUpdate"/>
        <hr class="solid">
      </div>
      <div class="col-lg-9 pr-5" v-if="DataHandler.cells && DataHandler.cells.length > 0">      
        <Heatmap 
          ref="heatmap"
          :column_width=column_width 
          :DataHandler=DataHandler
          :isSwitched=isSwitched  
          :sortBy=sortBy        
          @changePosition="changePosition"
        >
        </Heatmap>
      </div>
      <div class="col-lg-3 pb-1">
        <MoleculeViewer 
          :segment=segment 
          :position=position
          :DataHandler=DataHandler
          @changeReferenceSequence="changeReferenceSequence"
          >
        </MoleculeViewer>
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
import DataHandler from "@/shared/DataHandler";

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
  public segment = 'HA'
  public position = 54
  public cells:any = null
  public group: any[] = []
  public customfile: any = null
  public isSwitched: boolean = true
  public sortBy: boolean = true
  public referenceSequence: any[] = [];
  private localDataHelper = new LocalDataHelper();
  private DataHandler = new DataHandler()
  $refs!: {
    heatmap: any;
  };
  sliderUpdate(gh: {target: string, value: any}) {
    const target = gh.target
    const value = gh.value
    this.$set(this, target, value)
    if (target == 'DataHandler'){
      this.segment = value.segment
      if (this.$refs.heatmap){
        this.$refs.heatmap.changeDataHandler()
      }
    }
    
  }
  
  changePosition(value: number){
    this.position = value
  }
  changeReferenceSequence(value: any){
    this.DataHandler.updateReference(value)
    this.sliderUpdate({target: "DataHandler", value: this.DataHandler})
  }  
  
}

</script>

<style scoped lang="scss">
</style>
