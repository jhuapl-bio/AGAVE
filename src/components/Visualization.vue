<template>
  <div class="container-fluid">
    <div class="row" style="padding: 0px; margin: 0">
      <div class="col-lg-12 pr-5">
        <VisualizationOptions 
          :referenceSequence=referenceSequence
          @sliderUpdate="sliderUpdate"/>
        <hr class="solid">
      </div>
      <div class="col-lg-8 pr-5" v-if="DataHandler.cells && DataHandler.cells.length > 0">      
        <Heatmap 
          ref="heatmap"
          :column_width=column_width 
          :DataHandler=DataHandler
          :isSwitched=isSwitched  
          :sortBy=sortBy      
          
          @changePosition="changePosition"
        >
        </Heatmap>
        <hr>
        <BarPlot 
          ref="barplot"
          v-if="DataHandler.cells"
          :DataHandler="DataHandler"
        ></BarPlot>
      </div>
      <b-col class="col-lg-4 pb-1">
        <MoleculeViewer 
          :segment=segment 
          :position=position
          :DataHandler=DataHandler
          @siteHover="siteHover"  
          @changeReferenceSequence="changeReferenceSequence"
          >
        </MoleculeViewer>
      </b-col>
      <b-col class="col-lg-12 pb-1">
        
        
      </b-col>
      <canvas id="mycanvas"></canvas>
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
import BarPlot from '@/components/BarPlot.vue'

@Component({
  components: {
    Heatmap,
    VisualizationOptions,
    MoleculeViewer,
    BarPlot
  }
})
export default class Visualization extends Vue {
  public depth_threshold = 0
  public frequency_threshold = 0.2
  public column_width = 9
  public segment = 'HA'
  public position = 54
  public cells:any = null
  public group: any[] = []
  public customfile: any = null
  public isSwitched: boolean = true
  public sortBy: boolean = true
  public referenceSequence: any[] = [];
  private localDataHelper = new LocalDataHelper();
  public switchedViewer = true
  private DataHandler = new DataHandler()
  $refs!: {
    heatmap: any;
    barplot: any;
  };
  sliderUpdate(gh: {target: string, value: any}) {
    const target = gh.target
    const value = gh.value
    this.$set(this, target, value)
    if (target == 'DataHandler'){
      this.segment = value.segment
      if (this.$refs.heatmap){
        this.$refs.heatmap.changeDataHandler()
        this.$refs.barplot.changeDataHandler()
      }
    }
    
  }
  siteHover(event: any){
    if (event.focus){
      this.$refs.heatmap.focusColumn(event.position, true)
    } else {
      this.$refs.heatmap.unfocusColumn(event.position)
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
