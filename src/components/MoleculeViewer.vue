<template>
  <div class="columns mb-6 mt-6">
    <div ref="viewer" class="viewer"></div>
    <div>
      <b-button outlined @click="focus">Focus</b-button>
      <b-button outlined @click="reset">Reset</b-button>
    </div>
  </div>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'

@Component({
  components: {
  }
})
export default class MoleculeViewer extends Vue {

  public viewer: any;

  mounted() {

    // this object is being imported in index.html so ignore the syntax error it throws
    // @ts-ignore
    this.viewer = new PDBeMolstarPlugin();

    // Available options here: https://github.com/PDBeurope/pdbe-molstar/wiki/1.-PDBe-Molstar-as-JS-plugin
    // Our H3 protein is 4o5n and our H1 protein is 3lzg
    const options = {
      moleculeId: '4o5n',
      hideControls: true,
      bgColor: {r:255, g:255, b:255}
    }
    
    this.viewer.render(this.$refs.viewer, options);

    // Remove some buttons that break everything
    this.removeButtons();
  }

  // Example of focus ability. In the future let's rig this to the d3 heatmap so that when an amino acid is clicked, the molecule focuses on it
  focus() {
    this.viewer.visual.focus([{
      residue_number: 31
    }])
  }

  reset() {
    this.viewer.visual.reset({ camera: true})
  }

  private removeButtons() {
    // TODO: find better way to do this than directly accessing the DOM
    const button1 = document.querySelector('[title="Toggle Controls Panel"]')
    const button2 = document.querySelector('[title="Toggle Expanded Viewport"]')
    if(button1){
      button1.remove()
    }
    if(button2){
      button2.remove()
    }
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