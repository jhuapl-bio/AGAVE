<template>
  <div class="columns mt-6 mb-6">
    <div class="column is-12">
      <h2 class="subtitle is-3">
        Crystal structure of A/Victoria/361/2011 (H3N2) influenza virus hemagglutinin
      </h2>
      <div ref="viewer" class="viewer"></div>
      <!-- <div>
        <b-input type="text" v-model="localPosition"></b-input>
        <b-button outlined @click="focus">Focus</b-button>
        <b-button outlined @click="reset">Reset</b-button>
      </div> -->
    </div>
  </div>
</template>

<script lang="ts">

import { Component, Vue, Watch, Prop } from 'vue-property-decorator'

interface Residue {
  chain: string
  position: number
}

@Component({
  components: {
  }
})
export default class MoleculeViewer extends Vue {

  public viewer: any;
  public localPosition: number =  55;

  @Prop({ required: true, default: 55 })
  public position!: string;

  @Watch('position')
  onPositionChanged(value: number, oldValue: number) {
    this.localPosition = value
    this.focus()
  }

  mounted() {

    // this object is being imported in index.html so ignore the syntax error it throws
    // @ts-ignore
    this.viewer = new PDBeMolstarPlugin();

    // Available options here: https://github.com/PDBeurope/pdbe-molstar/wiki/1.-PDBe-Molstar-as-JS-plugin
    // Our H3N2 HA protein is 4o5n and our H1N1 HA protein is 3lzg
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
    this.viewer.visual.clearSelection();
    let residue: Residue;
    if ( this.localPosition >= 25 && this.localPosition <= 341 ) {
      residue = { chain: 'A', position: this.localPosition - 22 }
    } else if ( this.localPosition >= 346 && this.localPosition <= 518 ) {
      residue = { chain: 'B', position: this.localPosition - 345 }
    } else {
      residue = { chain: '', position: 0 }
    }
    if(residue.chain !== '') {
      this.viewer.visual.select({
        data: [{
          struct_asym_id: residue.chain,
          start_residue_number: residue.position,
          end_residue_number: residue.position,
          focus: true,
          color: {r:255, g:255, b:0}
        }]
      })
    }
  }

  reset() {
    this.viewer.visual.reset({ camera: true})
    this.viewer.visual.clearSelection();
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