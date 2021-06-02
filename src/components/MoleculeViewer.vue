<template>
  <div class="columns mb-6 mt-6">
    <div id="jsmol" class="viewer"></div>
    <div id="button">
      <b-button outlined @click="focus">Focus</b-button>
      <b-button outlined @click="reset">Reset</b-button>
    </div>
  </div>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'
// import { PDBeMolstarPlugin } from 'pdbe-molstar/build/pdbe-molstar-plugin-1.1.0-dev.4'
// import { PDBeMolstarPlugin } from 'pdbe-molstar/build/pdbe-molstar-plugin-1.1.0-dev.4'
// const a = require('lib/pdbe-molstar-plugin-1.1.0.js')

@Component({
  components: {
  }
})
export default class MoleculeViewer extends Vue {

  public viewer: any;

  mounted() {

    this.viewer = new PDBeMolstarPlugin();
      //Set options (Checkout available options list in the documentation)
      const options = {
        moleculeId: '4o5n',
        hideControls: true,
        bgColor: {r:255, g:255, b:255}
      }
      
      const viewerContainer = document.getElementById('jsmol');
  
      this.viewer.render(viewerContainer, options);
  }

  focus() {
    this.viewer.visual.focus([{
      residue_number: 31
    }])
  }

  reset() {
    this.viewer.visual.reset({ camera: true})
  }
}

</script>

<style scoped lang="scss">
  .viewer {
    height: 600px;
    width: 100%;
    float: left;
    position: relative;
  }

</style>