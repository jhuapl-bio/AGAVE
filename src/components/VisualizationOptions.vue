<template>
  <section>
    <h2 class="subtitle is-3">Visualization Options</h2>
    <div class="columns">
      <b-field label="Example Dropdown" class="column">
        <b-select placeholder="Select a name">
          <option
            v-for="option in data"
            :value="option"
            :key="option">
            {{ option }}
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
  private data: Array<string> = [
    'Hannah',
    'Tom',
    'Brian'
  ];

  private sliderValue = 42;
  depth_threshold = 10
  frequency_threshold = 0.2
  column_width = 7

  @Watch('depth_threshold')
  onDepthChanged(value: number, oldValue: number) {
    this.$emit('sliderUpdate', {value: value, target: 'depth_threshold'})
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
