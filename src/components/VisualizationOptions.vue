<template>
  <section>
    <h2 class="subtitle is-3">Visualization Options</h2>
    <div class="columns">
      <b-field label="Segment" class="column">
        <b-select placeholder="Segment" v-model="segment">
          <option 
            v-for="segment in segments" 
            :value="segment" 
            :key="segment">
           {{segment}}
          </option>
        </b-select>
      </b-field>
      <b-field label="Group" class="column">
        <b-select placeholder="Group" v-model="group">
          <option 
            v-for="group in groups" 
            :value="group" 
            :key="group">
           {{group}}
          </option>
        </b-select>
      </b-field>
      <b-field label="Depth Threshold" class="column">
        <b-slider v-model="depth_threshold"></b-slider>
      </b-field>
      <b-field label="Frequency Threshold" class="column">
        <b-slider v-model="frequency_threshold"></b-slider>
      </b-field>
      <b-field label="Column Width" class="column">
        <b-slider v-model="column_width"></b-slider>
      </b-field>
    </div>
  </section>
</template>

<script lang="ts">

import { Component, Vue, Watch } from 'vue-property-decorator'

@Component({
  
})
export default class VisualizationOptions extends Vue {

  public depth_threshold = 0
  public frequency_threshold = 0.2
  public column_width = 6
  public segments: Array<string> = ['NP', 'HA', 'NA', 'M1']
  public segment: string = 'NP'
  public groups: Array<string> = ["3C.2 - NPS",
    "3C.2 - 3 dpi hNEC",
    "3C.2 - 7 dpi hNEC",
    "3C.2 - MDCK",
    "3C.3 - NPS",
    "3C.3 - 3 dpi hNEC",
    "3C.3 - 7 dpi hNEC",
    "3C.3 - MDCK",
    "Flu B / unk"]
  public group: string = "3C.2 - 3 dpi hNEC"

  @Watch('depth_threshold')
  onDepthChanged(value: number, oldValue: number) {
    this.$emit('sliderUpdate', {value: value, target: 'depth_threshold'})
  }

  @Watch('segment')
  onSegChanged(value: string, oldValue: string) {
    this.$emit('sliderUpdate', {value: value, target: 'segment'})
  }

  @Watch('frequency_threshold')
  onFrequencyChanged(value: number, oldValue: number) {
    this.$emit('sliderUpdate', {value: value, target: 'frequency_threshold'})
  }

  @Watch('column_width')
  onColWidthChanged(value: number, oldValue: number) {
    this.$emit('sliderUpdate', {value: value, target: 'column_width'})
  }

  @Watch('group')
  onGroupChanged(value: string, oldValue: string) {
    this.$emit('sliderUpdate', {value: value, target: 'group'})
  }
  
}

</script>

<style scoped lang="scss">
</style>
