<template>
  <b-row> 
    <b-col class="col-lg-12 pb-1">
      <div id='molstar-parentCustom' style='top: 0; left: 0; right: 0; bottom: 0'>
        <!-- <div ref="viewerCustom" class="viewer"></div> -->
        <canvas id='molstar-canvasCustom' style='top: 0; left: 0; right: 0; bottom: 0'></canvas>
        <!-- <b-input-group prepend="" class="mt-3">             
          <b-input-group-append>
            <b-button
              elevation="2"
              @click="clearCustom()"
            >Clear PDB(s)</b-button>
          </b-input-group-append>
        </b-input-group> -->
      </div>
      <div id='molstar-parent' style='top: 0; left: 0; right: 0; bottom: 0'>
          <canvas id='molstar-canvas' style='top: 0; left: 0; right: 0; bottom: 0'></canvas>
      </div>
        <b-field :label="title"></b-field>
        <b-input-group prepend="PDB ID" class="mt-3">
          <b-form-input type="text" v-model="pdb_local" ></b-form-input>
          <b-input-group-append>
            <b-button
              elevation="2"
              @click="proteinChange(pdb_local.toLowerCase())"
            >Change Protein</b-button>
          </b-input-group-append>
          <b-input-group-append>
            <b-button
              elevation="2"
              @click="proteinChange(null)"
            >Clear PDB(s)</b-button>
          </b-input-group-append>
        </b-input-group>
        <b-field label="Molecule Structure" class="column is-narrow pl-0">
          <b-switch v-model="isSwitched">
            {{ ( isSwitched ? 'Biological Assembly' : 'Asymmetric Unit' ) }}
          </b-switch>
            <b-form-file
            type="file"
            v-model="custompdb"
            id="custompdbfile"
            ref="custompdbfile"
            placeholder="Choose a pdb file or drop it here..."
            drop-placeholder="Drop file here...">
            </b-form-file>
        </b-field>
        <b-field v-if="queryingReferenceSequence" label="Querying Reference Sequence..."></b-field>
        <b-field v-if="queryingResidueMapping" label="Querying Residue Mapping.."></b-field>
        <b-field v-if="chain_focus" :label="'Chains at '+localPosition" class="column is-narrow">
          <b-select placeholder="Chain" @change="focus()"  v-model="chain_focus" :options="available_focus_chains">
          </b-select>
        </b-field>
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
import { DefaultPluginSpec, PluginSpec } from 'molstar/lib/mol-plugin/spec';
import { PluginContext  } from 'molstar/lib/mol-plugin/context';
import { PluginConfig } from 'molstar/lib/mol-plugin/config';
import { ColorNames } from 'molstar/lib/mol-util/color/names';
import { PluginCommands } from 'molstar/lib/mol-plugin/commands';
import { Structure } from 'molstar/lib/mol-model/structure';
import { Script } from 'molstar/lib/mol-script/script';
import { StructureSelection } from 'molstar/lib/mol-model/structure/query';

import { createPluginUI } from "molstar/lib/mol-plugin-ui";
import { Viewer } from 'molstar/build/viewer/molstar.js'
 
import swal from 'vue-sweetalert2'
import * as path from 'path';
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
  public viewerCustom: any;
  public chain_focus: any = null 
  public entity_focus:any = null;
  
  public available_focus_chains: any[] = []
  // public protein: string = "";
  public pdb_local:string = ""
  public map_positions:any = {}
  public queryingResidueMapping: boolean = false;
  public queryingReferenceSequence: boolean = false;
  public localPosition: number =  55;
  public localHoverPosition: number =  0;
  public referenceSequence: any = {}
  public isSwitched = true
  public assemblyId = "1"
  public positions: any[] = [];
  public custompdb: any = null
  public chains: any = {id: null,  entities: [] };
  public defaultMoleculeId = "7xly"
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
  @Prop({ required: true, default: 0 })
  public hoverPosition!: string;

  @Prop({ required: true, default: "5r7y" })
  public pdb!: string;

  @Prop({ required: true, default: null })
  public DataHandler!: DataHandler

  public title: string = "No title found"

  @Watch('position')
  onPositionChanged(value: number, oldValue: number) {
    this.localPosition = value

    this.focus(value)
  }
  
  @Watch('hoverPosition')
  onHoverPositionChanged(value: number, oldValue: number) {
    this.localHoverPosition = value
    console.log(value,"<<")
    if (value >= 0){
      // this.highlight()
    } else {
      console.log(this.viewerCustom.managers)
      // this.viewerCustom.managers.interactivity.lociHighlights.clearHighlights();
      // this.viewer.managers.interactivity.lociHighlights.clearHighlights();
      // this.viewerCustom.visual.clearHighlight()
    }
  }

  @Watch('custompdb')
  CustomPDBFile(value: any, oldValue: any) {
    const $this  = this
    let reader = new FileReader();  
    reader.addEventListener("load", parseFile, false);
    reader.readAsText(value);
    // let name  = path.parse(value.name).name
    async function parseFile(){
      let format = 'pdb'
      // await $this.viewer.plugin.loadStructureFromData(reader.result, format)
      const data = await $this.viewer.plugin.builders.data.rawData({
          data:  reader.result /* string or number[] */,
          label: value.name /* optional label */
      });
      const trajectory = await $this.viewer.plugin.builders.structure.parseTrajectory(data, format);
      await $this.viewer.plugin.builders.structure.hierarchy.applyPreset(trajectory, 'default');
    
    }

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
    // this.proteinChange(value)
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


  siteHover(item: any){
    this.localPosition = item.endIndex + this.map_positions[item.entity].positions[1]
    this.focus(this.localPosition)
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
  loadCustomPDB(url: string){

  }
  proteinChange(value: any){
    this.chain_focus = null
    if (value){
      const options: any= {
        moleculeId: value,
        assemblyId: this.assemblyId,
        hideControls: false,
        bgColor: {r:255, g:255, b:255}
      }
      this.queryAPI(options)
      // this.viewer.visual.update(options)
      // Remove some buttons that break everything
      // this.removeButtons();
    } else {
      // this.viewer.instance.clear()
    }
      
  }
  clearCustom(){
    // this.viewerCustom.plugin.clear()
    // this.viewerCustom.instance.reset()

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

  async queryAPI(moleculeId:string){
    let error: any = null
    if (moleculeId === this.defaultMoleculeId || moleculeId === undefined) {
      return;
    }
    try {
      // https://www.ebi.ac.uk/pdbe/graph-api/pdbe_pages/uniprot_mapping/4o5n/1
      this.queryingResidueMapping = true;
      // throw new Error("new err")
      let response: any = await this.getdata(`https://www.ebi.ac.uk/pdbe/graph-api/mappings/uniprot_segments/${moleculeId.toLowerCase()}`)
      this.title = "Fetching..."
      // console.log("Querying API call finished", response)
      this.map_positions = {}
      if (
        response.data && 
        response.data[moleculeId] && 
        response.data[moleculeId].UniProt){
        let data: any = response.data[moleculeId].UniProt;
        const uniprots = Object.keys(response.data[moleculeId].UniProt)
        let sum = 1;
        uniprots.forEach((accession: any)=>{
          if (data[accession].mappings){
            const mappings: any = data[accession].mappings
            this.chains = {
              id: moleculeId,
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
        this.pdb = moleculeId
      } 
    } catch(err){
      console.error(err)
      this.reportError(err, "Error in fetching Query for uniprot mappings from pdbID")
    } finally {
      this.queryingResidueMapping = false;
      try {
        this.queryingReferenceSequence = true;
        this.referenceSequence = {}
        let response: any =  await this.getdata(`https://www.ebi.ac.uk/pdbe/search/pdb/select?q=pdb_id:${moleculeId}&wt=json`)
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
                  ref_seq[i+1] = chain_id
                  
                }
              }
              this.referenceSequence = ref_seq
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
  async make_custom_pdbemolstar(options: any){
    // this object is being imported in index.html so ignore the syntax error it throws
    // @ts-ignore
    this.viewerCustom = new PDBeMolstarPlugin();
    this.viewerCustom.render(this.$refs.viewerCustom, options);
    this.viewerCustom.events.loadComplete.subscribe(() => { 
      console.log("LOADED CustomPDF")
      // this.viewerCustom.plugin.clear()
      
    })//do something after 3d view is rendered });
  }
  async make_pdbemolstar(options: any){
    // this object is being imported in index.html so ignore the syntax error it throws
    // @ts-ignore
    this.viewer = new PDBeMolstarPlugin();
    const $this = this;
    this.viewer.render(this.$refs.viewer, options);
    // Remove some buttons that break everything
    this.removeButtons();
    this.viewer.events.loadComplete.subscribe(() => { 
      console.log("LOADED")
      
    })
    console.log(this.viewer,"......")
    document.addEventListener('PDB.molstar.mouseover', (e) => { //do something on event 
      console.log(e)
    });
    
  }

  async getdata(string:string){
    let response = await axios
      .get(string)
    return response
  }

  async mounted() {
    const $this = this
    // Available options here: https://github.com/PDBeurope/pdbe-molstar/wiki/1.-PDBe-Molstar-as-JS-plugin
    // Our H3N2 HA protein is 4o5n and our H1N1 HA protein is 3lzg
    // const options: any= {
    //   moleculeId: this.pdb || this.defaultMoleculeId,
    //   assemblyId: this.assemblyId,
    //   hideControls: false,
    //   alphafoldView: true,
    //   subscribeEvents: true,
    //   bgColor: {r:255, g:255, b:255}
    // }
    // this.make_pdbemolstar(options)
    // this.make_custom_pdbemolstar({
    //   hideControls: false,
    //   assemblyId: this.assemblyId,
    //   alphafoldView: true,
    //   moleculeId: '7qur',
    //   bgColor: {r:255, g:255, b:255}
    // })
    // this.queryAPI(options)
    let options = {
        layoutIsExpanded: true,
        layoutShowControls: true,
        layoutShowRemoteState: true,
        layoutShowSequence: true,
        layoutShowLog: true,
        layoutShowLeftPanel: true,

        viewportShowExpand: true,
        viewportShowSelectionMode: true,
        viewportShowAnimation: true,

        pdbProvider: 'rcsb',
        emdbProvider: 'rcsb',
    }
    let defaultSpecs = DefaultPluginSpec();
    const MySpec: PluginSpec = {
      ...defaultSpecs,
      config: [
        [PluginConfig.VolumeStreaming.Enabled, true],
        [PluginConfig.Viewport.ShowControls, true],
        [PluginConfig.Viewport.ShowExpand, true],
        [PluginConfig.Viewport.ShowSelectionMode, true],
        [PluginConfig.Viewport.ShowSettings, true],
      ],
      layout: {
        initial: {
          isExpanded: true,
          showControls: true,
        },
      }, 
      
      canvas3d: {
          camera: {
              helper: { axes: { name: 'off', params: {} } }
          }
      },
     
    }   
    async function initViewer(target: string | HTMLElement, options: any) {
        return new Viewer(target, options)
    }
    let  canvasMain = <HTMLCanvasElement> document.getElementById('molstar-canvas');
    let parentMain = <HTMLDivElement> document.getElementById('molstar-parent');
    let canvasCustom = <HTMLCanvasElement> document.getElementById('molstar-canvasCustom');
    let  parentCustom = <HTMLDivElement> document.getElementById('molstar-parentCustom');
    // let viewer = await initViewer(canvas, options)
    // console.log(viewer)
    // viewer.loadPdb('7bv2');
    // viewer.loadEmdb('EMD-30210', { detail: 6 });
    this.viewer = await init(parentMain, canvasMain, '7bv2')
    // plugin.managers.camera.focusLoci(loci);
    console.log(this.viewer)
    this.viewer.events.log.subscribe((e:any) => { console.log(e,"plugin") })
    $this.viewerCustom = await init(parentCustom, canvasCustom, '7bv2')
    async function init(parent: string | HTMLElement, canvas: string | HTMLCanvasElement, pdbid: string) {
        
        // let format = 'pdb'
        
        const plugin = new PluginContext(MySpec);
        await plugin.init();
        // let plugin = await createPluginUI(parent)
        if (!plugin.initViewer(canvas, parent)) {
            console.error('Failed to init Mol*');
            return;
        }

        const data = await plugin.builders.data.download({ url: `https://files.rcsb.org/download/${pdbid}.pdb` }, { state: { isGhost: false } });
        const trajectory = await plugin.builders.structure.parseTrajectory(data, 'pdb');
        await plugin.builders.structure.hierarchy.applyPreset(trajectory, 'default');
        return plugin

        // const renderer = plugin.canvas3d!.props.renderer;
        // PluginCommands.Canvas3D.SetSettings(plugin, { settings: { renderer: { ...renderer, backgroundColor: ColorNames.red /* or: 0xff0000 as Color */ } } });
    }
    // this.queryAPI(this.pdb || this.defaultMoleculeId )

    
  }

  determinePosition(localPosition: number, mapPosition: number){
    return localPosition - mapPosition
  }
  getPositionFocus(localPosition: number){
    let residue: Residue =  { chain: '', entity: '', position: 0 };
    let found: boolean = false

    for(let d of Object.keys(this.map_positions).sort().filter((e:any)=>{return e != 'total'})) {
      if (localPosition  >= this.map_positions[d].positions[1] 
      && localPosition <= this.map_positions[d].positions[3]  ){
        const position = this.determinePosition(localPosition,this.map_positions[d].positions[1])
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
    return residue
  }
  lociFocus(plugin: any, position: number){
    const ligandData = plugin.managers.structure.hierarchy.selection.structures[0]?.components[0]?.cell.obj?.data;
    const selection = Script.getStructureSelection(Q => Q.struct.generator.atomGroups({
    'residue-test': Q.core.set.has([Q.set(position), Q.ammp('auth_seq_id')]),
    }), ligandData);
    const loci = StructureSelection.toLociWithSourceUnits(selection);
    plugin.managers.camera.focusLoci(loci);
    plugin.managers.interactivity.lociHighlights.highlightOnly({ loci: loci });
  }
  lociHighlight(plugin: any){
    const ligandData = plugin.managers.structure.hierarchy.selection.structures[0]?.components[0]?.cell.obj?.data;
    const selection = Script.getStructureSelection(Q => Q.struct.generator.atomGroups({
        'chain-test': Q.core.rel.eq(['A', Q.ammp('label_asym_id')])
    }), ligandData);
    const loci = StructureSelection.toLociWithSourceUnits(selection);
    // plugin.managers.camera.focusLoci(loci);
    plugin.managers.interactivity.lociHighlights.highlightOnly({ loci: loci });
    // console.log(loci,"<<<")
  }
  public highlight(){
    // this.viewer.visual.clearSelection();
    
    // let residue = {
    //   auth_asym_id:"A",
    //   struct_asym_id: 'A',
    //   entry_id: "7qur.pdb",
    //   position:60,
    //   seq_id: 60,
    //   entity_id:"1",
    //   start_residue_number: 1,
    //   end_residue_number: 200,
    //   label_asym_id: "A",
    //   instance: "ASM_1",
    //   model: 1,
    //   comp_id: "SER",
    //   auth_seq_id: 60
    // }
    let residue = this.getPositionFocus(this.localHoverPosition)
    
    this.lociHighlight(this.viewer)
    this.lociHighlight(this.viewerCustom)
    // let plugin = this.viewer 
    // const ligandData = plugin.managers.structure.hierarchy.selection.structures[0]?.components[0]?.cell.obj?.data;
    // const ligandLoci = Structure.toStructureElementLoci(ligandData as any);
    
    // plugin.managers.camera.focusLoci(ligandLoci);
    // console.log(ligandLoci)
    // plugin.managers.interactivity.lociSelects.select({ loci: ligandLoci });
    // if (residue.position > 0){
      
    //   try{
    //     this.viewer.visual.select({
    //         data: [{
    //           ...residue,
    //           focus: true,
    //           color: {r:255, g:255, b:0}
    //         }
    //         ]
    //     })
    //   } catch (err){
    //     console.error(err)
    //   }
      // try{
      //   console.log(this.viewerCustom)
      //   this.viewerCustom.visual.highlight({
      //       data: [{
      //         struct_asym_id: residue.chain,
      //         entity_id: residue.entity,
      //         residue_number: residue.position > 0 ? residue.position : -1,
      //         focus: false,
      //         color: {r:255, g:255, b:0}
      //       }
      //       ]
      //   })
      // } catch (err){
      //   console.error(err)
      // }
    // }
      
  }
  // Example of focus ability. In the future let's rig this to the d3 heatmap so that when an amino acid is clicked, the molecule focuses on it
  public focus(position:number) {
    // this.viewer.visual.clearSelection();
    // let residue = this.getPositionFocus(this.localPosition)
    // let position = residue.position
    // let residue = {
    //   auth_asym_id:"A",
    //   entry_id: "7qur.pdb",
    //   position:60,
    //   entity_id:"1",
    //   instance: "ASM_1",
    //   model: 1
    // }
    console.log(position)
    this.lociFocus(this.viewer, position)
    this.lociFocus(this.viewerCustom, position)
    
    // if(residue.auth_asym_id !== '') {
    //   try{
        
    //     this.viewer.visual.select({
    //       data: [{
    //         ...residue,
    //         focus: true,
    //         color: {r:255, g:255, b:0}
    //       }
    //       ]
    //     })      
    //   } catch (err){
    //     console.error(err)
    //   }
      // try{
      //   this.viewerCustom.visual.select({
      //     data: [{
      //       struct_asym_id: residue.chain,
      //       entity_id: residue.entity,
      //       residue_number: residue.position,
      //       focus: true,
      //       color: {r:255, g:255, b:0}
      //     }
      //     ]
      //   })  
      // } catch (err){
      //   console.error(err)
      // }
    // }
  }

  reset() {
    // this.viewer.visual.reset({ camera: true})
    // this.viewer.visual.clearSelection();
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
    height: 300px;
    width: 100%;
    float: left;
    position: relative;
  }
  #molstar-parent, #molstar-parentCustom{
    height: 800px;
    width: 100%;
    float: left;
    position: relative;
  }
  #molstar-canvas, #molstar-canvasCustom{
    height: 300px;
    width: 100%;
    float: left;
    position: relative;
  }
  .msp-plugin ::-webkit-scrollbar-thumb {
        background-color: #474748 !important;
    }
    .viewerSection {
      padding-top: 40px;
    }
    .controlsSection {
      width: 200px;
      float: left;
      padding: 40px 0 0 0;
      margin-right: 10px;
    }
    .controlBox {
      border: 1px solid lightgray;
      padding: 10px;
      margin-bottom: 20px;
    }

</style>