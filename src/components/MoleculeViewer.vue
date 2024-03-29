<template>
  <b-row> 
    <b-col class="col-lg-12 pb-1">
      <div class="">
        <b-field :label="title"></b-field>
        <div >
          <b-input-group prepend="PDB ID" class="mt-3">
            <b-form-input type="text" v-model="pdb_local" ></b-form-input>
            <b-input-group-append>
              <b-button
                elevation="2"
                @click="proteinChange(pdb_local.toLowerCase())"
              >Change Protein</b-button>
            </b-input-group-append>
          </b-input-group>
        </div>
        <div ref="viewer" class="viewer"></div>
        <b-field label="Molecule Structure" class="column is-narrow pl-0">
          <b-switch v-model="isSwitched">
            {{ ( isSwitched ? 'Biological Assembly' : 'Asymmetric Unit' ) }}
          </b-switch>
        </b-field>
        <b-field v-if="queryingReferenceSequence" label="Querying Reference Sequence..."></b-field>
        <b-field v-if="queryingResidueMapping" label="Querying Residue Mapping.."></b-field>
        <b-field v-if="chain_focus" :label="'Chains at '+localPosition" class="column is-narrow">
          <b-select placeholder="Chain" @change="focus()"  v-model="chain_focus" :options="available_focus_chains">
          </b-select>
        </b-field>
      </div>
    </b-col>
    <b-col class="col-lg-12 pb-1">
        <BindingSites 
          @siteHover="siteHover" 
          :positions="positions"
          :chains=chains>
        </BindingSites>
    </b-col>
  </b-row>
</template>

<script lang="ts">

import { Component, Vue, Watch, Prop } from 'vue-property-decorator'
import axios from 'axios'
import swal from 'vue-sweetalert2'
import DataHandler from "@/shared/DataHandler";
import BindingSites from '@/components/BindingSites.vue'
interface Residue {
  chain: string
  position: number
  entity: string
}

@Component({
  components: {
    BindingSites
  }
})
export default class MoleculeViewer extends Vue {

  public viewer: any;
  public chain_focus: any = null 
  public entity_focus:any = null;
  
  public available_focus_chains: any[] = []
  // public protein: string = "";
  public pdb_local:string = ""
  public map_positions:any = {}
  public queryingResidueMapping: boolean = false;
  public queryingReferenceSequence: boolean = false;
  public localPosition: number =  55;
  public referenceSequence: any = {}
  public isSwitched = true
  public assemblyId = "1"
  public positions: any[] = [];
  public custompdb: any = null
  public chains: any = {id: null,  entities: [] };
  // public protein_per_protein: any = {
  //   "H3N2": {
  //     "HA": '4o5n',
  //     "NP": '1hoc',
  //     "NA": '2hty',
  //     'M1': '5v6g',
  //     'M': '5v6g',
  //     'PB1': '6qx3',
  //     'PB2': '6euv',
  //     'NS': '6qxe',
  //     'PA': '2w69'
  //   },
  //   "H1N1": {
  //     "HA": '3al4',
  //     "NP": '5b7b',
  //     "NA": '3nss',
  //     'M1': '3md2',
  //     'M': '3md2',
  //     'PB1': '2ztt',
  //     'PB2': '2ztt',
  //     'NS': '6dgk',
  //     'PA': '5des'
  //   }
  // }
  
  @Prop({ required: true, default: 55 })
  public position!: string;
  @Prop({ required: true, default: null })
  public pdb!: string|null;

  @Prop({ required: true, default: null })
  public DataHandler!: DataHandler

  public title: string = "No title found"

  @Watch('position')
  onPositionChanged(value: number, oldValue: number) {
    this.localPosition = value

    this.focus()
  }
  @Watch('custompdb')
  CustomPDBFile(value: any, oldValue: any) {
    console.log(value)
  }
  @Watch('referenceSequence', { immediate: true, deep: true })
  onRefSeqChange(value: any, oldValue: any) {
    if (value && Object.keys(value).length > 0){
      this.$emit("changeReferenceSequence", value)
    }
  }
  @Watch('DataHandler.pdb')
  onDataChanged(value: any, oldValue: any){
    this.pdb_local = value
    this.proteinChange(value)
  }
  @Watch('isSwitched')
  onSwitchToggled(value: any, oldValue: any) {
    if(value === true) {
      this.assemblyId = "1"
    } else {
      this.assemblyId = "preffered"
    }
    this.proteinChange(this.pdb)
  }
  @Watch('pdb')
  onPdbChanged(value: any, oldValue:any) {
    if (value === null || value === "") {
      this.proteinChange(null)
    } else {
      this.proteinChange(value)
    }
  }


  siteHover(item: any){
    this.localPosition = item.endIndex + this.map_positions[item.entity].positions[1]
    this.focus()
    if (this.localPosition >= this.DataHandler.position_ranges[0]
      && this.localPosition <= this.DataHandler.position_ranges[1]){
      item.position  = this.localPosition
      
      this.$emit("siteHover", item)
    }
  }
  
  parseError(err: any){
    console.log(err)
    if (err.toJSON){
      return err.toJSON().message
    } else {
      return  err
    } 
  }

  proteinChange(value: string|null){
    this.chain_focus = null
    const options: any= {
      assemblyId: this.assemblyId,
      hideControls: true,
      bgColor: {r:255, g:255, b:255}
    }
    if(value === null) {
      options.customData = { url: 'empty.pdb', format: 'mmcif'}
    } else {
      options.moleculeId = value
    }
    this.queryAPI(options)
    this.viewer.visual.update(options)
    // Remove some buttons that break everything
    this.removeButtons();
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
    if (options.moleculeId === undefined) {
      return;
    }
    try {
      // https://www.ebi.ac.uk/pdbe/graph-api/pdbe_pages/uniprot_mapping/4o5n/1
      this.queryingResidueMapping = true;
      // throw new Error("new err")
      let response: any = await this.getdata(`https://www.ebi.ac.uk/pdbe/graph-api/mappings/uniprot_segments/${options.moleculeId.toLowerCase()}`)
      this.title = "Fetching..."
      // console.log("Querying API call finished", response)
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
            this.chains = {
              id: options.moleculeId,
              entities: [...new Set(mappings.map((d: any) => d.entity_id))]
            }
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
        this.pdb = options.moleculeId
      } 
    } catch(err){
      console.error(err)
      this.reportError(err, "Error in fetching Query for uniprot mappings from pdbID")
    } finally {
      this.queryingResidueMapping = false;
      try {
        this.queryingReferenceSequence = true;
        this.referenceSequence = {}
        let response: any =  await this.getdata(`https://www.ebi.ac.uk/pdbe/search/pdb/select?q=pdb_id:${options.moleculeId}&wt=json`)
        if (
          response.data && 
          response.data.response && 
          response.data.response.docs){
          const chains: any = response.data.response.docs
          let ref_seq: any = {}
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
                  let chain_id = chain.molecule_sequence.substring(position,position+1)
                  // ref_seq.push( {
                  //   position: i+1,
                  //   aa: chain_id
                  // } )
                  ref_seq[i+1] = chain_id
                  
                }
              }
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
    // console.log(options)
    // options.customData = {
    //   url: "/data/test.pdb",
    //   format: "pdb"
    // }
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
      assemblyId: this.assemblyId,
      hideControls: true,
      bgColor: {r:255, g:255, b:255}
    }
    if(this.pdb === null) {
      options.customData = { url: 'empty.pdb', format: 'mmcif'}
    } else {
      options.moleculeId = this.pdb
    }
    this.make_pdbemolstar(options)
    this.queryAPI(options)
  }

  determinePosition(localPosition: number, mapPosition: number){
    return localPosition - mapPosition
  }

  focus() {
    // try {
    //   this.viewer.visual.clearSelection();
    // } catch(e) {}
    let residue: Residue =  { chain: '', entity: '', position: 0 };
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
    // const button1 = document.querySelector('[title="Toggle Controls Panel"]')
    const button2 = document.querySelector('[title="Toggle Expanded Viewport"]')
    // if(button1){
    //   button1.remove()
    // }
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