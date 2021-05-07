<template>
  <section>
    <h2 class="subtitle is-3">Visualization Options</h2>
    <b-field label="Example Dropdown">
      <b-select placeholder="Select a name">
        <option
          v-for="option in data"
          :value="option"
          :key="option">
          {{ option }}
        </option>
      </b-select>
    </b-field>
    <b-field label="Example Checkbox">
      <b-checkbox>Hello</b-checkbox>
    </b-field>
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
  ]
}

</script>

<style scoped lang="scss">
</style>
