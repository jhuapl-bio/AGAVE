<template>
  <div>
    <p>
      The visualization will go here
    </p>
    <Heatmap></Heatmap>
    <MoleculeViewer></MoleculeViewer>
  </div>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'
import Heatmap from './Heatmap.vue'
import MoleculeViewer from './MoleculeViewer.vue'

@Component({
  components: {
    Heatmap,
    MoleculeViewer
  }
})
export default class Visualization extends Vue {
}

</script>

<style scoped lang="scss">
</style>
