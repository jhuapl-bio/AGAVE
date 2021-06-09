<template>
  <section>
    <h2 class="subtitle is-3">Visualization Options</h2>
    <div class="columns">
      <b-field label="Segment Select" class="column">
        <b-form-select
          placeholder="Select Segment"
          v-model="segment"
          :options="segments">
        </b-form-select>
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


  private sliderValue = 42;
  depth_threshold = 10
  frequency_threshold = 0.2
  column_width = 7
  public segments: Array<string> = ['NP', 'HA', 'NA', 'M1']
  public segment: string = 'NP'
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
  


}

</script>

<style scoped lang="scss">
</style>
