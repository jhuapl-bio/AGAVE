<template>
  <section>
    <!-- <h2 class="subtitle is-3">Local Variants Per Sample</h2> -->
    <div class="columns">
      <b-field label="Segment" class="column is-narrow">
        <b-select placeholder="Segment" v-model="segment">
          <option 
            v-for="segment in segments" 
            :value="segment" 
            :key="segment">
           {{segment}}
          </option>
        </b-select>
      </b-field>
      <b-field label="Group" class="column is-3">
        <b-select placeholder="Group" v-model="group" multiple :options="groups">
        </b-select>
      </b-field>
      <b-field label="Depth Threshold" class="column is-2">
        <b-numberinput v-model="depth_threshold" :step="1" :min="0" :max="100000" controls-position="compact"></b-numberinput>
      </b-field>
      <!-- <b-field label="Frequency Threshold" class="column is-narrow"> -->
        <!-- <b-numberinput v-model="frequency_threshold" :step=".05" :min="0" :max="1.0" controls-position="compact"></b-numberinput> -->
      <!-- </b-field> -->
      <b-field label="Column Width" class="column is-2">
        <b-numberinput v-model="column_width" :step="1" :min="1" :max="100000" controls-position="compact"></b-numberinput>
      </b-field>
      
    </div>
    <b-form-file
          type="file"
          v-model="customfile"
          id="customfile"
          ref="customfile"
          placeholder="Choose a file or drop it here..."
          drop-placeholder="Drop file here..."
        >
        </b-form-file>
        <div class="mt-3">Selected file: {{ customfile ? customfile.name : '' }}</div>
  </section>
</template>

<script lang="ts">

import { Component, Vue, Watch, Prop } from 'vue-property-decorator'
import LocalDataHelper from "@/shared/LocalDataHelper";

@Component({
  
})
export default class VisualizationOptions extends Vue {

  public depth_threshold = 0
  public frequency_threshold = 0.2
  public column_width = 6
  public data:any = null
  private localDataHelper = new LocalDataHelper();
  public customfile: any = null
  public segment: string = 'PB2'
  public segments: Array<string> = ['HA', 'NP', 'NA', 'M', 'PB1', 'PB2', 'NS', 'PA']
  public group: any[] = []
  public groups: Array<any> = []
  @Watch("customfile")
  async onChangeFile(value: any, oldValue: any) {
    const $this = this
    const reader = new FileReader()
    reader.onload = function(event:any) {
      $this.getData(reader.result, 'string')
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

  getData(string:any, type: string){
    let data:any = null
    if (type == 'file'){
      const promises: Object[] = [];
      promises.push(
        this.localDataHelper.readJSON(string)
      );
      Promise.all(promises).then((l) => {
        data = l[0];
        this.groups = [...new Set(data.map((d: any) => d.group))];
        console.log(this.group, ":::")
        if (! this.group || this.group.length == 0){
          this.group = [this.groups[0]]
        } else {
          let newgroups: any = []
          this.group.forEach((d:any)=>{
            if (this.groups.indexOf(this.group) <= -1){
              newgroups.push(d)
            }
          })
          this.group  = newgroups
        }
        this.data = data
      }).catch((err:any)=>{
        this.$swal.fire({
          position: 'center',
          icon: 'error',
          showConfirmButton:true,
          title:  "JSON parsing error",
          text: err
        });
      });
    } else {
        data = (this.localDataHelper.parseJSON(string))
        this.groups = [...new Set(data.map((d: any) => d.group))];
        if (this.groups.indexOf(this.group) <= -1){
          this.group = [this.groups[0]]
        }
        this.data = data
    } 
    
    
  }


  @Watch('depth_threshold')
  onDepthChanged(value: number, oldValue: number) {
    this.$emit('sliderUpdate', {value: value, target: 'depth_threshold'})
  }

  @Watch('segment')
  onSegChanged(value: string, oldValue: string) {
    this.getData(`New/grouped/${value}.json`, "file")
    this.$emit('sliderUpdate', {value: value, target: 'segment'})
  }

  @Watch('frequency_threshold')
  onFrequencyChanged(value: number, oldValue: number) {
    this.$emit('sliderUpdate', {value: value, target: 'frequency_threshold'})
  }
  @Watch('data')
  onDataChanged(value: string, oldValue: string) {
    this.$emit('sliderUpdate', {value: value, target: 'data'})
  }

  @Watch('column_width')
  onColWidthChanged(value: number, oldValue: number) {
    this.$emit('sliderUpdate', {value: value, target: 'column_width'})
  }
  
  @Watch('group')
  onGroupChanged(value: string, oldValue: string) {
    this.$emit('sliderUpdate', {value: value, target: 'group'})
  }


  mounted() {
    this.data= null
    this.group= []
    this.getData(`New/grouped/${this.segment}.json`, "file")
  }
  
}

</script>

<style scoped lang="scss">
  .b-slider {
    margin: 1.5em 0;
  }
</style>
