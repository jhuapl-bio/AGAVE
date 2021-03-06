<template>
<div>
  <b-tabs>

    <b-tab title="Data Settings" active>
      <div class="columns is-variable is-4">
        <b-field label="Default Data" class="column is-narrow">
          <b-select 
          placeholder="Data" 
          v-model="DataHandler.data_selected" 
          @change="emitChange($event, { full: true, target: 'data_selected' })">
            <option
            v-for="option in DataHandler.defaultDataList"
            :value="option"
            :key="option.id">
                {{ option.label }}
            </option>
          </b-select>
        </b-field>
        <b-field label="Segment" class="column is-narrow">
          <b-select placeholder="Segment" v-model="DataHandler.segment" @change="emitChange($event, { full: true, target: 'segment' })" :options="segments"></b-select>
        </b-field>
        <b-field label="Group" class="column is-narrow">
          <b-select placeholder="Group" v-if="DataHandler.group" v-model="DataHandler.group" @change="emitChange($event, { full: true, target: 'group' })" multiple :options="DataHandler.groups"></b-select>
        </b-field>
        <b-field label="Axis Experiment Consensus"  class="column is-narrow" v-if="DataHandler && DataHandler.consensus_map">
          <b-select :disabled="!isSwitched" placeholder="Mapped Experiment" v-model="DataHandler.selected_consensus" @change="emitChange($event, { full: false, target: 'selected_consensus' })">
            <option
            v-for="option in DataHandler.consensus_map"
            :value="option"
            :key="option.experiment">
                {{ option.experiment }}
            </option>
          </b-select>
        </b-field> 
        <b-field label="Subtype" class="column is-narrow">
          <b-select 
          placeholder="Subtype" 
          v-model="DataHandler.subtype" 
          @change="emitChange($event, { full: false, target: 'subtype' })">
            <option
            v-for="option in ['H1N1', 'H3N2']"
            :value="option"
            :key="option">
              {{ option }}
            </option>
          </b-select>
        </b-field>
      </div>
    </b-tab>

    <b-tab title="Heatmap Settings">
      <div class="columns is-variable is-4">
        <b-field label="Depth Threshold" class="column is-narrow">
          <b-numberinput v-model="depth_threshold" :step="1"  :min="0" :max="100000" controls-position="compact"></b-numberinput>
        </b-field>
        <!-- <b-field label="Frequency Threshold" class="column is-narrow"> -->
          <!-- <b-numberinput v-model="frequency_threshold" :step=".05" :min="0" :max="1.0" controls-position="compact"></b-numberinput> -->
        <!-- </b-field> -->
        <b-field label="Column Width" class="column is-narrow">
          <b-numberinput v-model="column_width" :step="1" :min="1" :max="100000" controls-position="compact"></b-numberinput>
        </b-field>
        <b-field label="Position Ranges" class="column is-2">
          <b-slider v-model="DataHandler.position_ranges" y :min="1" :max="DataHandler.position_max" @change="emitChange($event, { full: false, target: 'position_ranges' })" :step="1" ticks></b-slider>
        </b-field>
        <b-field label="Sort" class="column is-narrow">
          <b-switch v-model="sortBy" >
            {{ ( sortBy ? 'Name' : 'Time' ) }}
          </b-switch>
        </b-field>
        <b-field label="Axis labels" class="column is-narrow">
          <b-switch v-model="isSwitched" >
            {{ ( isSwitched ? 'Consensus' : 'Reference' ) }}
          </b-switch>
        </b-field>
      </div>
    </b-tab>

    <b-tab title="Data Upload">
      <div class="columns is-variable is-4">
        <b-field label="Custom Variant File Input" class="column is-6">
          <b-form-file
          type="file"
          v-model="customfile"
          id="customfile"
          ref="customfile"
          placeholder="Choose a file or drop it here..."
          drop-placeholder="Drop file here...">
          </b-form-file>
        </b-field>
      </div>
    </b-tab>

  </b-tabs>
</div>
</template>

<script lang="ts">

import { Component, Vue, Watch, Prop } from 'vue-property-decorator'
import DataHandler from "@/shared/DataHandler";

@Component({})
export default class VisualizationOptions extends Vue {

  // Variables to track the input values
  public depth_threshold = 0
  public frequency_threshold = 0.2
  public column_width = 9
  public data:any = null
  public cells: any = null
  public customfile: any = null
  public segment: string = 'HA'
  public segments: Array<string> = ['HA', 'NP', 'NA', 'M', 'PB1', 'PB2', 'NS', 'PA']
  public group: any[] = []
  public groups: Array<any> = []
  public isSwitched: boolean = true
  public sortBy: boolean = true
  minrange: number = 1
  maxrange: number = 1
  position_max: any =1
  position_ranges: any = [this.minrange,this.maxrange]
  fetching_information = false

  @Prop({ required: false, default: null })
  public referenceSequence!: any;
    
  private DataHandler = new DataHandler()

  activeTab = 0

  @Watch("isSwitched")
  onSwitchedChange(value: boolean, oldValue: boolean) {
    this.$emit('sliderUpdate', {value: value, target: 'isSwitched'})
  }

  @Watch("sortBy")
  onSortByChange(value: boolean, oldValue: boolean) {
    this.$emit('sliderUpdate', {value: value, target: 'sortBy'})
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

  @Watch('column_width')
  onColWidthChanged(value: number, oldValue: number) {
    this.$emit('sliderUpdate', {value: value, target: 'column_width'})
  }

  @Watch('depth_threshold')
  onDepthTChanged(value: number, oldValue: number) {
    this.emitChange(value, {full: false, target: 'depth_threshold' })
  }

  async emitChange(event: any, params: { full: boolean, target: string} ){
    // console.log(event, params,)
    if (params.target == 'depth_threshold'){
      this.DataHandler.depth_threshold = event
    } else if (params.target == 'segment'){
      this.DataHandler.segment = event
      await this.getData(`${this.DataHandler.data_selected.id}/${this.DataHandler.data_selected.subfolder}/${event}.json`, "file")
    } else if (params.target == 'data_selected'){
      this.DataHandler.group = []
      this.DataHandler.updateSubtype(event.virus)
      await this.getData(`${this.DataHandler.data_selected.id}/${this.DataHandler.data_selected.subfolder}/${this.DataHandler.segment}.json`, "file")
    } else if (params.target == 'group' ){
      this.DataHandler.group = event
    } else if (params.target == 'position_ranges'){
      this.DataHandler.position_ranges = event
    } else if (params.target == 'selected_consensus'){
      this.DataHandler.selected_consensus = event
    } else {
      return
    }
    if (params.full){
      this.DataHandler.fullUpdate()
    } else {
      this.DataHandler.updateCells()
    }
    this.$emit('sliderUpdate', {value: this.DataHandler, target: 'DataHandler'})
  }

  async getData(value: any, type: string){
    const $this = this
    try{
      await $this.DataHandler.getData(value, type)
      return 
    } catch(err: any) {
      console.log("errr found.....")
      $this.$swal.fire({
          position: 'center',
          icon: 'error',
          showConfirmButton:true,
          title:  "JSON parsing error",
          text: err
      });
      throw err
    }
  }

  mounted() {
    this.getData(`${this.DataHandler.data_selected.id}/${this.DataHandler.data_selected.subfolder}/${this.segment}.json`, "file").then((d:any)=>{
      this.DataHandler.fullUpdate()
      this.$emit('sliderUpdate', {value: this.DataHandler, target: 'DataHandler'})
    })
  }
  
}

</script>

<style scoped lang="scss">
  .b-slider {
    margin: 1.5em 0;
  }

  // Bootstrap is adding some styles we don't want!
  .tabs {
    display: block;
    overflow-x: hidden;
  }
  
  .columns {
    padding: 1rem 0;
  }

</style>
