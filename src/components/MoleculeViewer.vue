<template>
  <div class="columns mb-6">
    <div class="column is-12">
      <b-field label="Crystal structure of A/Victoria/361/2011 (H3N2) influenza virus hemagglutinin"></b-field>
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
  public protein_per_segment: any = {
    "HA": '4o5n',
    "NP": '1hoc',
    "NA": '2hty',
    'M1': '5v6g'
  }
  @Prop({ required: true, default: 55 })
  public position!: string;
  @Prop({ required: true, default: 'HA' })
  public segment!: string;

  @Watch('position')
  onPositionChanged(value: number, oldValue: number) {
    this.localPosition = value
    this.focus()
  }
  @Watch('segment')
  onSegmentChanged(value: number, oldValue: number) {
    console.log("segment changed", value, this.protein_per_segment[value])
    this.viewer.visual.update({
      moleculeId: this.protein_per_segment[value],
      hideControls: true,
      bgColor: {r:255, g:255, b:255}
    })
    // Remove some buttons that break everything
    this.removeButtons();
  }
  make_pdbemolstar(options: any){
    // this object is being imported in index.html so ignore the syntax error it throws
    // @ts-ignore
    this.viewer = new PDBeMolstarPlugin();
    this.viewer.render(this.$refs.viewer, options);
    // Remove some buttons that break everything
    this.removeButtons();
  }

  mounted() {
    // Available options here: https://github.com/PDBeurope/pdbe-molstar/wiki/1.-PDBe-Molstar-as-JS-plugin
    // Our H3N2 HA protein is 4o5n and our H1N1 HA protein is 3lzg
    const options: any= {
      moleculeId: this.protein_per_segment[this.segment],
      hideControls: true,
      bgColor: {r:255, g:255, b:255}
    }
    this.make_pdbemolstar(options)
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
    console.log(this.viewer)
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
    height: 22rem;
    width: 100%;
    float: left;
    position: relative;
  }

</style>