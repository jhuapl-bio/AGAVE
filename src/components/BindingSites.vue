<template>
  <div class="">
    <!-- <h3>Binding Sites for pdb molecule</h3> -->
    <b-table  
      hover 
      :items="ligands"
      sticky-header="300px"
      @row-hovered="rowHovered"
      @row-unhovered="rowunHovered"
      :fields="[
        {
          key: 'name',
          label: 'Name',
          sticky: true
        },
        {
          key: 'dataType',
          label: 'Type',
          sticky: true
        },
        {
          key: 'entity',
          label: 'Chain',
          sticky: true
        },
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
          key: 'startCode',
          label: 'Start',
          sticky: true
        },
        {
          key: 'endCode',
          label: 'End',
          sticky: true
        }
      ]"
      ></b-table>
  </div>
</template>

<script lang="ts">

import { Component, Vue, Prop, Watch } from 'vue-property-decorator'
import axios from 'axios'
import swal from 'vue-sweetalert2'

@Component({})
export default class BindingSites extends Vue {

  ligands: any[] = []

  @Prop({ required: true, default: 6 })
  public chains!: any;
  @Watch("chains", {deep:true})
  onColWidthChanged(value: any, oldValue: any) {
    console.log("chains changed")
    this.queryLigands(value)
  }
  mounted(){
    console.log(this.chains)
    this.queryLigands(this.chains)
  }
  async getdata(string:string){
    let response = await axios
      .get(string)
    return response
  }
  rowHovered(item: any){
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
    console.log("querying ligands")
    // const uniq_entities = [...new Set(chains.map((d: any) => d.entity_id))];
    let promises: any[] = []
    
    chains.entities.forEach((d:any)=>{
      let data= this.getdata(`https://www.ebi.ac.uk/pdbe/graph-api/pdbe_pages/binding_sites/${chains.id}/${d}`).then((e:any)=>{
        if (e.data){
          e.data[chains.id].data.forEach((f:any)=>{
            console.log(f)
            f.residues.map((g:any)=>{ 
              g.entity = d
              g.name = f.accession
              g.dataType = f.dataType
              return g
            })
            this.ligands = f.residues
          })
        }
      
      })
      // promises.push(this.getdata(`https://www.ebi.ac.uk/pdbe/graph-api/pdbe_pages/binding_sites/${options.moleculeId}/${d}`))
    
    })
    // Promise.all(promises).then((data:any)=>{
    //   console.log(data)
    // })
    // .catch((err)=>{
    //   console.log(err)
    // })

  }

  


}

</script>
