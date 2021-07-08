<template>
  <section>
    <!-- <h2 class="subtitle is-3">Local Variants Per Sample</h2> -->
    <div class="columns">
      <b-field label="Segment" class="column is-narrow">
        <b-select placeholder="Segment" v-model="DataHandler.segment" @change="emitChange($event, { full: true, target: 'segment' })" :options="segments">
          
        </b-select>
      </b-field>
      <b-field label="Group" class="column is-3">
        <b-select placeholder="Group" v-model="DataHandler.group" @change="emitChange($event, { full: true, target: 'group' })" multiple :options="DataHandler.groups">
        </b-select>
      </b-field>
      <b-field label="Depth Threshold" class="column is-2">
        <b-numberinput v-model="DataHandler.depth_threshold" :step="1" @change="emitChange($event, { full: false, target: 'depth_threshold' })" :min="0" :max="100000" controls-position="compact"></b-numberinput>
      </b-field>
      <!-- <b-field label="Frequency Threshold" class="column is-narrow"> -->
        <!-- <b-numberinput v-model="frequency_threshold" :step=".05" :min="0" :max="1.0" controls-position="compact"></b-numberinput> -->
      <!-- </b-field> -->
      <b-field label="Column Width" class="column is-2">
        <b-numberinput v-model="column_width" :step="1" :min="1" :max="100000" controls-position="compact"></b-numberinput>
      </b-field>
      <b-field label="Position Ranges" class="column is-3">
        <b-slider v-model="DataHandler.position_ranges" y :min="1" :max="DataHandler.position_max" @change="emitChange($event, { full: false, target: 'position_ranges' })" :step="1" ticks>
        </b-slider>
      </b-field>
      <b-field label="Axis labels" class="column is-2">
        <b-switch v-model="isSwitched" >
          {{ ( isSwitched ? 'Consensus Sequence' : 'Reference' ) }}
        </b-switch>
      </b-field>
    </div>
    <div class="columns">
      <b-field label="Axis Experiment Consensus"  class="column is-4" v-if="DataHandler && DataHandler.consensus_map">
        <b-select :disabled="!isSwitched" placeholder="Mapped Experiment" v-model="DataHandler.selected_consensus" @change="emitChange($event, { full: false, target: 'selected_consensus' })" 
                    >
                    <option
                      v-for="option in DataHandler.consensus_map"
                      :value="option"
                      :key="option.experiment">
                      {{ option.experiment }}
                    </option>
        </b-select>
      </b-field>   
      <b-field label="Custom Variant File Input" class="column is-8" >
        
        <b-form-file
              type="file"
              v-model="customfile"
              id="customfile"
              ref="customfile"
              placeholder="Choose a file or drop it here..."
              drop-placeholder="Drop file here..."
            >
            </b-form-file>
            
      </b-field>
    </div>
  </section>
</template>

<script lang="ts">

import { Component, Vue, Watch, Prop } from 'vue-property-decorator'
import DataHandler from "@/shared/DataHandler";

import * as d3 from "d3"
@Component({
  
})
export default class VisualizationOptions extends Vue {

  public depth_threshold = 0
  public frequency_threshold = 0.2
  public column_width = 6
  public data:any = null
  public cells: any = null
  public customfile: any = null
  public segment: string = 'HA'
  public segments: Array<string> = ['HA', 'NP', 'NA', 'M', 'PB1', 'PB2', 'NS', 'PA']
  public group: any[] = []
  public groups: Array<any> = []
  public isSwitched: boolean = true
  minrange: number = 1
  maxrange: number = 1
  position_max: any =1
  position_ranges: any = [this.minrange,this.maxrange]
  
  private DataHandler = new DataHandler()
  @Watch("isSwitched")
  onSwitchedChange(value: boolean, oldValue: boolean) {
    this.$emit('sliderUpdate', {value: value, target: 'isSwitched'})
  }
  @Watch("customfile")
  async onChangeFile(value: any, oldValue: any) {
    const $this = this
    const reader = new FileReader()
    let estimate_segment: any = null
    try{
      estimate_segment = value.name.split(".")[0]
      if (this.segments.indexOf(estimate_segment) > -1){
        this.segment = estimate_segment
      }
    } catch(err){
      console.log(err)
    }
    reader.onload = function(event:any) {
      $this.getData(reader.result, 'string').then((d:any)=>{
        $this.DataHandler.segment = $this.segment
        $this.$emit('sliderUpdate', {value: $this.DataHandler, target: 'DataHandler'})
      })
    }
    reader.onerror = function(err:any){
      $this.$swal.fire({
        position: 'center',
        icon: 'error',
        showConfirmButton:true,
        title:  "Error in submitting file",
        text: err
      })
    }
    let text = reader.readAsText(value) // you could also read images and other binaries
  }
  @Prop({ required: false, default: null })
  public referenceSequence!: any;


  @Watch('column_width')
  onColWidthChanged(value: number, oldValue: number) {
    this.$emit('sliderUpdate', {value: value, target: 'column_width'})
  }

  async emitChange(event: any, params: { full: boolean, target: string} ){
    console.log(event, params)
    if (params.target == 'depth_threshold'){
      this.DataHandler.depth_threshold = event
    } else if (params.target == 'segment'){
      this.DataHandler.segment = event
      await this.getData(`New/grouped/${event}.json`, "file")
    } else if (params.target == 'group'){
      this.DataHandler.group = event
    } else if (params.target == 'position_ranges'){
      this.DataHandler.position_ranges = event
    } else if (params.target == 'selected_consensus'){
      this.DataHandler.selected_consensus = event
    } else {
      return
    }
    if (params.full){
      this.DataHandler.updateData()
    }
    this.DataHandler.updateCells()
    this.$emit('sliderUpdate', {value: this.DataHandler, target: 'DataHandler'})
  }

  async getData(value: any, type: string){
    this.DataHandler.getData(value, type).then((d:any)=>{
      // this.$emit('sliderUpdate', {value: this.DataHandler, target: 'DataHandler'})
      return
    }).catch((err)=>{
      console.log("errr found.....")
     this.$swal.fire({
          position: 'center',
          icon: 'error',
          showConfirmButton:true,
          title:  "JSON parsing error",
          text: err
      });
    })
  }
  mounted() {
    this.getData(`New/grouped/${this.segment}.json`, "file").then((d:any)=>{
      this.$emit('sliderUpdate', {value: this.DataHandler, target: 'DataHandler'})
    })
    
  }
  
}

</script>

<style scoped lang="scss">
  .b-slider {
    margin: 1.5em 0;
  }
</style>
