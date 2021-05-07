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
      <b-field label="Example Slider" class="column">
        <b-slider v-model="sliderValue"></b-slider>
      </b-field>
    </div>
  </section>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'

@Component({})
export default class VisualizationOptions extends Vue {
  private data: Array<string> = [
    'Hannah',
    'Tom',
    'Brian'
  ];

  private sliderValue = 42;
}

</script>

<style scoped lang="scss">
</style>
