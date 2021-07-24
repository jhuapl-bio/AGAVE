<template>
  <div class="">
    <!-- <h3>Binding Sites for pdb molecule</h3> -->
    <b-table  
      hover 
      :items="ligands"
      v-if="ligands && ligands.length > 0"
      sticky-header="22rem"
      @row-clicked="rowClicked"
      v-b-tooltip.hover.right title="Click to view in heatmap and molecule viewer"
      style="cursor: pointer"
      :fields="[
        
        {
          key: 'startIndex',
          label: 'Start Index',
          sticky: true
        },
        {
          key: 'endIndex',
          label: 'End Index',
          sticky: true
        },
        {
          key: 'dataType',
          label: 'Type',
          sticky: true
        },
        {
          key: 'startCode',
          label: 'Start',
          sticky: true
        },
        {
          key: 'endCode',
          label: 'End',
          sticky: true
        },
        {
          key: 'name',
          label: 'Name',
          sticky: true
        },
        {
          key: 'entity',
          label: 'Chain',
          sticky: true
        }
      ]"
      >
      </b-table>
      <p class="warning" v-else-if="ligandQuerying">Getting Ligand information</p>
      <p class="warning" v-else>No ligand information available</p>
  </div>
</template>

<script lang="ts">

import { Component, Vue, Prop, Watch } from 'vue-property-decorator'
import axios from 'axios'
import swal from 'vue-sweetalert2'

@Component({})
export default class BindingSites extends Vue {

  ligands: any[] = []
  ligandQuerying = false
  @Prop({ required: true, default: 6 })
  public chains!: any;
  @Watch("chains", {deep:true})
  onColWidthChanged(value: any, oldValue: any) {
    this.queryLigands(value)
  }
  mounted(){
    this.queryLigands(this.chains)
  }
  async getdata(string:string){
    let response = await axios
      .get(string)
    return response
  }
  rowClicked(item: any){
    let event: any = item
    event.focus = true
    this.$emit('siteHover', item)
  }
  rowunHovered(item: any){
    let event: any = item
    event.focus = false
    this.$emit('siteHover', item)
  }
  async queryLigands(chains: any){
    let promises: any[] = []
    let ligands: any[] = []
    this.ligandQuerying = true
    chains.entities.forEach((d:any)=>{
      promises.push(this.getdata(`https://www.ebi.ac.uk/pdbe/graph-api/pdbe_pages/binding_sites/${chains.id}/${d}`))
    })
    Promise.allSettled(promises).then((responses:any)=>{
      responses.forEach((response:any)=>{
        if (response.status == 'fulfilled'){
          if (response.value.data){
            let data:any = response.value.data
            data[chains.id].data.forEach((f:any)=>{
              f.residues.map((g:any, i: any)=>{ 
                g.entity = f.additionalData.entityId
                g.name = f.accession
                g.dataType = f.dataType
                return g
              })
              ligands.push(...f.residues)
            })
          }
        }
      })
      this.ligands = ligands
      this.ligandQuerying = false
    }).catch((err:any)=>{
      console.log(err)
    })
  }

  


}

</script>
