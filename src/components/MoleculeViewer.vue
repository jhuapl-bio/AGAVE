<template>
  <div class="columns mb-6">
    <div class="column is-12">
      <b-field :label="this.title"></b-field>
      <div >
        <b-input-group prepend="PDB ID" class="mt-3">
          <b-form-input type="text" v-model="protein" ></b-form-input>
          <b-input-group-append>
            <b-button
              elevation="2"
              @click="proteinChange(protein.toLowerCase())"
            >Change Protein</b-button>
          </b-input-group-append>
        </b-input-group>
      </div>
      <div ref="viewer" class="viewer"></div>
      <b-field v-if="queryingReferenceSequence" label="Querying Reference Sequence..."></b-field>
      <b-field v-if="queryingResidueMapping" label="Querying Residue Mapping.."></b-field>
      <b-field v-if="chain_focus" :label="'Chains at '+this.localPosition" class="column is-narrow">
        <b-select placeholder="Chain" @change="focus()"  v-model="chain_focus" :options="available_focus_chains">
        </b-select>
      </b-field>
    </div>
  </div>
</template>

<script lang="ts">

import { Component, Vue, Watch, Prop } from 'vue-property-decorator'
import axios from 'axios'
import swal from 'vue-sweetalert2'

interface Residue {
  chain: string
  position: number
  entity: string
}

@Component({
  components: {
  }
})
export default class MoleculeViewer extends Vue {

  public viewer: any;
  public chain_focus: any = null 
  public entity_focus:any = null;
  
  public available_focus_chains: any[] = []
  public protein: string = "";
  public map_positions:any = {}
  public queryingResidueMapping: boolean = false;
  public queryingReferenceSequence: boolean = false;
  public localPosition: number =  55;
  public referenceSequence: any = { positions: [], sequence: [] };
  public protein_per_segment: any = {
    "HA": '4o5n',
    "NP": '1hoc',
    "NA": '2hty',
    'M1': '5v6g',
    'M': '5v6g',
    'PB1': '6qx3',
    'PB2': '6euv',
    'NS': '6qxe',
    'PA': '2w69'
  }
  
  @Prop({ required: true, default: 55 })
  public position!: string;
  @Prop({ required: true, default: 'HA' })
  public segment!: string;

  public title: string = "No title found"

  @Watch('position')
  onPositionChanged(value: number, oldValue: number) {
    this.localPosition = value
    // this.chain_focus = null
    this.focus()
  }
  
  @Watch('referenceSequence', { immediate: true, deep: true })
  onRefSeqChange(value: any, oldValue: any) {
    if (value.positions && value.positions.length > 0){
      this.$emit("changeReferenceSequence", value)
    }
  }
  @Watch('segment')
  onSegmentChanged(value: number, oldValue: number) {
    
    this.proteinChange(this.protein_per_segment[this.segment])
    // Remove some buttons that break everything
    this.removeButtons();
  }
  parseError(err: any){
    console.log(err)
    if (err.toJSON){
      return err.toJSON().message
    } else {
      return  err
    } 
  }
  proteinChange(value: string){
    this.chain_focus = null
    const options: any= {
      moleculeId: value,
      hideControls: true,
      bgColor: {r:255, g:255, b:255}
    }
    this.queryAPI(options)
    this.viewer.visual.update(options)
  }
  reportError(err:any, title: string){
    const error = this.parseError(err) 
    this.$swal.fire({
      position: 'center',
      icon: 'error',
      showConfirmButton:true,
      title:  title,
      text: error
    });
    
  }
  async queryAPI(options:any){
    let error: any = null
    try {
      // https://www.ebi.ac.uk/pdbe/graph-api/pdbe_pages/uniprot_mapping/4o5n/1
      this.queryingResidueMapping = true;
      // throw new Error("new err")
      let response: any = await this.getdata(`https://www.ebi.ac.uk/pdbe/graph-api/mappings/uniprot_segments/${options.moleculeId}`)
      this.title = "Fetching..."
      console.log("Querying API call finished", response)
      this.map_positions = {}
      if (
        response.data && 
        response.data[options.moleculeId] && 
        response.data[options.moleculeId].UniProt){
        let data: any = response.data[options.moleculeId].UniProt;
        const uniprots = Object.keys(response.data[options.moleculeId].UniProt)
        let sum = 1;
        uniprots.forEach((accession: any)=>{
          if (data[accession].mappings){
            const mappings: any = data[accession].mappings
            mappings.forEach((mapping:any)=>{
              if (! this.map_positions.hasOwnProperty(mapping.entity_id)){
                this.map_positions[mapping.entity_id] = { chains: [], positions: []}
              }
              this.map_positions[mapping.entity_id].chains.push(mapping.struct_asym_id) 
              this.map_positions[mapping.entity_id].positions = [mapping.start.residue_number, mapping.unp_start - mapping.start.residue_number, mapping.end.residue_number, mapping.unp_end - mapping.start.residue_number +1 ]
            })        
          }
          
        })
        const keys: any[] = Object.keys(this.map_positions).sort()
        let position: number = 0;
        keys.forEach((key:any)=>{
          if (this.map_positions[key].positions[1] < position){
            this.map_positions[key].positions[1] = position 
            this.map_positions[key].positions[3] = position + this.map_positions[key].positions[2]
          }
          position =  this.map_positions[key].positions[3] + this.map_positions[key].positions[0] 
            
        })
        this.protein = options.moleculeId
      }
    } catch(err){
      this.reportError(err, "Error in fetching Query Info")
    } finally {
      this.queryingResidueMapping = false;
      try {
        this.queryingReferenceSequence = true;
        this.referenceSequence = { positions: [], sequence: [] };
        let response: any =  await this.getdata(`https://www.ebi.ac.uk/pdbe/search/pdb/select?q=pdb_id:${options.moleculeId}&wt=json`)
        if (
          response.data && 
          response.data.response && 
          response.data.response.docs){
          const chains: any = response.data.response.docs
          let ref_seq: string[] = []
          let ref_pos: number[] = []
          chains.forEach((chain: any)=>{
            if (chain.entity_id in this.map_positions){
              if (chain.title) {
                this.title = chain.title
              } else {
                this.title = "No title found"
              }
              this.map_positions[chain.entity_id].chains = this.map_positions[chain.entity_id].chains.sort()
              
              const ids: any[]  = chain.struct_asym_id;
              for (let i = this.map_positions[chain.entity_id].positions[1]; i < this.map_positions[chain.entity_id].positions[3]; i++){
                if (i >= 0){
                  const position = this.determinePosition(i, this.map_positions[chain.entity_id].positions[1])
                  ref_seq.push(chain.molecule_sequence.substring(position,position+1) + "." + (i+1))
                  ref_pos.push(i+1)
                }
              }
              this.referenceSequence.sequence = ref_seq
              this.referenceSequence.positions = ref_pos
              // console.log("reference seq", this.referenceSequence)
              // console.log("map postiions", this.map_positions)
            }
          })
        }
      } catch(err){
        this.reportError(err, "Error in Fetching Reference Info")
      } finally {
        this.queryingReferenceSequence = false;
      }
    }
    
    
    
    
  }
  async make_pdbemolstar(options: any){
    // this object is being imported in index.html so ignore the syntax error it throws
    // @ts-ignore
    this.viewer = new PDBeMolstarPlugin();
    this.viewer.render(this.$refs.viewer, options);
    // Remove some buttons that break everything
    this.removeButtons();
  }
  async getdata(string:string){
    let response = await axios
      .get(string)
    return response
  }
  async mounted() {
    // Available options here: https://github.com/PDBeurope/pdbe-molstar/wiki/1.-PDBe-Molstar-as-JS-plugin
    // Our H3N2 HA protein is 4o5n and our H1N1 HA protein is 3lzg
    const options: any= {
      moleculeId: this.protein_per_segment[this.segment],
      hideControls: true,
      bgColor: {r:255, g:255, b:255}
    }
    this.make_pdbemolstar(options)
    this.queryAPI(options)
  }
  determinePosition(localPosition: number, mapPosition: number){
    return localPosition - mapPosition
  }
  // Example of focus ability. In the future let's rig this to the d3 heatmap so that when an amino acid is clicked, the molecule focuses on it
  focus() {
    this.viewer.visual.clearSelection();
    let residue: Residue =  { chain: '', entity: '', position: 0 };
    // if ( this.localPosition >= 25 && this.localPosition <= 341 ) {
    //   residue = { chain: 'A', position: this.localPosition - 22 }
    // } else if ( this.localPosition >= 346 && this.localPosition <= 518 ) {
    //   residue = { chain: 'B', position: this.localPosition - 345 }
    // } else {
    //   residue = { chain: '', position: 0 }
    // }
    let found: boolean = false
    for(let d of Object.keys(this.map_positions).sort().filter((e:any)=>{return e != 'total'})) {
      if (this.localPosition  >= this.map_positions[d].positions[1] 
      && this.localPosition <= this.map_positions[d].positions[3]  ){
        const position = this.determinePosition(this.localPosition,this.map_positions[d].positions[1])
        if (! this.chain_focus || this.entity_focus != d){  
          this.chain_focus = this.map_positions[d].chains[0]
          this.available_focus_chains = this.map_positions[d].chains
        }
        this.entity_focus = d
        residue = { chain: this.chain_focus, entity: d, position:  position }
        found = true;
        break;
      }   
    }
    if(residue.chain !== '') {
      this.viewer.visual.select({
        data: [{
          struct_asym_id: residue.chain,
          entity_id: residue.entity,
          residue_number: residue.position,
          focus: true,
          color: {r:255, g:255, b:0}
        }
        ]
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