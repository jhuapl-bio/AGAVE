<template>
<div>
  <b-tabs>

    <b-tab title="Data Settings" active>
      <b-row >
      <b-col sm="2">
          <b-field label="File" class="column is-narrow">
            <b-select placeholder="File" v-if="DataHandler.defaultDataListFiles"  v-model="DataHandler.defaultDataListFile" @change="emitChange($event, { full: true, target: 'file' })"  :options="DataHandler.defaultDataListFiles"></b-select>
          </b-field>
          <b-field style="display: flex" label="Show Discordants Only" class="column is-narrow ">
            <b-checkbox  class=" ml-5"
              @change="emitChange($event, { full: true, target: 'discordant' })" 
              v-model="showDiscordantOnly" ></b-checkbox>
          </b-field>
      </b-col>
      <b-col sm="2">
          <b-field :label="(isDataSwitched ? 'Default Data' : 'Custom')" class="column is-narrow">
            <b-select 
              placeholder="Data" 
              v-model="DataHandler.experiment"
              @change="emitChange($event, { full: true, target: 'data_selected' })">
              <option
              v-for="option in DataHandler.experiments"
              :value="option"
              :key="option.id">
                  {{ option.label }}
              </option>
            </b-select>
          </b-field>
        </b-col>
        <b-col sm="2">
          <b-field label="Protein"  class="column is-narrow">
            <b-select placeholder="protein" v-model="DataHandler.protein" @change="emitChange($event, { full: true, target: 'protein' })" :options="DataHandler.proteins"></b-select>
          </b-field>
        </b-col>
        <b-col sm="2">
          <b-field label="Sample"  class="column is-narrow">
            <b-select placeholder="Sample"  :disabled="DataHandler.changing" v-if="DataHandler.sample" v-model="DataHandler.sample" @change="emitChange($event, { full: true, target: 'sample' })" multiple :options="DataHandler.samples"></b-select>
          </b-field>
        </b-col>
        <b-col sm="2">
          <b-field label="Group"  class="column is-narrow">
            <b-select placeholder="Group"  :disabled="DataHandler.changing" v-if="DataHandler.group" v-model="DataHandler.group" @change="emitChange($event, { full: true, target: 'group' })" multiple :options="DataHandler.groups"></b-select>
          </b-field>
          <!-- <b-field label="Axis Experiment Consensus"  class="column is-narrow" >
            <b-select :disabled="!isSwitched" placeholder="Mapped Experiment" 
              :options="DataHandler.experiments"
              v-model="DataHandler.experiment"
              @change="emitChange($event, { full: false, target: 'selected_consensus' })">
            </b-select> 
          </b-field>  -->
        </b-col>
        <b-col sm="2">
          <b-field label="Organism" class="column is-narrow">
            <b-select 
            placeholder="Organism"   :disabled="DataHandler.changing"
            v-model="DataHandler.organism" 
            @change="emitChange($event, { full: true, target: 'organism' })">
              <option
              v-for="option in DataHandler.organisms"
              :value="option"
              :key="option">
                {{ option }}
              </option>
            </b-select>
          </b-field>
        </b-col>
      </b-row>
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
          <b-numberinput :value="column_width" :step="1" :min="1" :max="100000" controls-position="compact" @input="onColWidthChanged($event)"></b-numberinput>
        </b-field>
        <b-field label="Position Ranges" class="column is-2">
          <b-slider v-model="DataHandler.position_ranges" y :min="1" :max="DataHandler.position_max" @change="emitChange($event, { full: false, target: 'position_ranges' })" :step="1" ticks></b-slider>
        </b-field>
        <b-field label="Sort" class="column is-narrow">
          <b-switch v-model="sortBy" >
            {{ ( sortBy ? 'Name' : 'Time' ) }}
          </b-switch>
        </b-field>
        <b-field label="Amino Acid Labels" class="column is-narrow">
            <b-select :value="amino_acid_label_option" @input="onAminoAcidLabelChanged($event)">
              <option v-for="option in amino_acid_label_options" :value="option" :key="option">
                {{ option }}
              </option>
            </b-select>
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
  public data:any = null
  public cells: any = null
  public customfile: any = null
  public protein: string = ""
  public showDiscordantOnly: boolean = true
  public proteins: Array<string> = []
  public group: any[] = []
  public groups: Array<any> = []
  public isDataSwitched: boolean = true
  public sortBy: boolean = true
  minrange: number = 1
  maxrange: number = 1
  position_max: any =1
  position_ranges: any = [this.minrange,this.maxrange]
  fetching_information = false
 
  @Prop({ required: false, default: null })
  public referenceSequence!: any;
  @Prop({ required: false})
  public column_width!: number;
  @Prop({ required: false})
  public amino_acid_label_option!: string;

  public DataHandler = new DataHandler()

  amino_acid_label_options = ["None", "Consensus amino acids", "Reference amino acids"]

  activeTab = 0

  @Watch("isDataSwitched")
  onSwitchedChangeDataType(value: boolean, oldValue: boolean) {
    this.emitChange(value, { full: true, target: 'data_type_selected' })
  }
  @Watch("sortBy")
  onSortByChange(value: boolean, oldValue: boolean) {
    this.$emit('sliderUpdate', {value: value, target: 'sortBy'})
  }

  @Watch("customfile")
  async onChangeFile(value: any, oldValue: any) {
    const $this = this
    const reader = new FileReader()
    this.isDataSwitched = false
    let estimate_protein: any = null
    reader.onload = function(event:any) {
      $this.getData(reader.result, 'string').then((d:any)=>{
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

  onColWidthChanged(value: number) {
    this.$emit('sliderUpdate', {value: value, target: 'column_width'})
  }

  onAminoAcidLabelChanged(value: string) {
    this.$emit('sliderUpdate', {value: value, target: 'amino_acid_label_option'})
  }

  @Watch('depth_threshold')
  onDepthTChanged(value: number, oldValue: number) {
    this.emitChange(value, {full: false, target: 'depth_threshold' })
  }

  async emitChange(event: any, params: { full: boolean, target: string} ){
    let changedData = true
    if (params.target == 'depth_threshold'){
      this.DataHandler.depth_threshold = event
    } else if (params.target == 'protein'){
      this.DataHandler.updateProtein(event)
      // await this.getData(`${this.DataHandler.data_selected.path}`, "file")
    } else if (params.target == 'organism'){
      // this.DataHandler.group = []
      // this.DataHandler.organism = event
      this.DataHandler.updateOrganism(event)
      // await this.getData(`${this.DataHandler.data_selected.path}`, "file")
    } else if (params.target == 'data_type_selected'){
      // this.DataHandler.changeDataType(event)
    } else if (params.target == 'data_selected' ){
      this.DataHandler.changeExperiment(event)
    } else if (params.target == 'group' ){
      this.DataHandler.group = event
    } else if (params.target == 'position_ranges'){
      this.DataHandler.position_ranges = event
    } else if (params.target == 'sample' ){
      this.DataHandler.sample = event
    } else if (params.target == 'file' ){
      changedData = false
      await this.getData(event, "file")
    } else if (params.target == 'selected_consensus'){
      this.DataHandler.selected_consensus = event
    } else if (params.target == 'discordant'){
      this.DataHandler.discordantOnly = event
    } else {
      return
    }
    if (params.full){
      this.DataHandler.fullUpdate()
    } else {
      this.DataHandler.updateCells()
    }
    if (changedData){
      this.$emit('sliderUpdate', {value: this.DataHandler, target: 'DataHandler'})
    }
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
    this.getData(`${this.DataHandler.data_selected}`, "file").then((d:any)=>{
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
