import * as d3 from 'd3'
import LocalDataHelper from "@/shared/LocalDataHelper";

interface StringMap { [key: string]: string; }

export default class DataHandler {
    sort: boolean = true
    referenceSequence: number[] = []
    position_ranges: number[] = []
    xvalues: any[] = []
    yvalues: any[] = []
    cells: any = null
    cells_full: any = null
    raw_data: any = null
    groups: any[] = []
    group: any[] = []
    segment: any = 'HA'
    segments: any[] = []
    frequency_threshold: number = 0
    depth_threshold: number = 0
    public localDataHelper = new LocalDataHelper()
    position_max: any = 1
    consensus_map: any  = null
    selected_consensus: any = {}
    subtype: string = "H1N1"
    public  constructor() {
    }
    public updateReference(referenceSequence: any){
        this.referenceSequence = referenceSequence
        // this.updatePositions(d3.extent(referenceSequence.map((d: any)=>{return d.position })))
    }
    public updatePositions(positions: any[])
    {
        this.position_ranges = positions
        // this.updateCells()
    }
    public updateGroup(positions: number[])
    {
        this.groups = positions
    }
    public updateSegment(positions: number[])
    {
        this.position_ranges = positions
    }
    public updateSubtype(subtype: string)
    {
        this.subtype = subtype
    }
    public updateCells(){
        let cells_filtered= this.cells_full.filter((d:any)=>{
            return d.position >= this.position_ranges[0] && d.position <= this.position_ranges[1]
        })
        this.cells = cells_filtered
    }  
    public updateData(){
        // Format data into cells
        const $this = this
        let data = this.raw_data
        let cells: any[] = [];
        data = data.filter( (d:any) => {
            return this.group.indexOf(d.group) > -1;
        })
        
        const consensus_map: any[] = []
        data.forEach((prep:any)=>{
            consensus_map.push({experiment: prep.experiment, residues: prep.residues.map((d:any, i:number)=>{return d.consensus_aa +"." + d.position})})
            prep.residues.forEach((residue:any)=>{
            cells.push({ unique: [...new Set(residue.counts.map((d: any) => d.aa))], segment:this.segment, max: residue.consensus_aa_count, experiment: prep.experiment, depth: residue.depth, position: +residue.position, total:+residue.depth, count: residue.counts.length, aa: residue.consensus_aa, consensus_count: residue.consensus_aa_count  })
            })
        })
        this.consensus_map = consensus_map
        this.selected_consensus = this.consensus_map[0]
        const min: any = d3.min(cells.map((d:any)=>{return +d.position}))
        const max: any = d3.max(cells.map((d:any)=>{return +d.position}))
        this.position_max = max
        this.position_ranges = [min, max]
        this.cells_full = cells
    }
    public async getData(string:any, type: string){
        let data:any = null
        try{
            if (type == 'file'){
                let data: any = await this.localDataHelper.readJSON(string)
                this.groups = [...new Set(data.map((d: any) => d.group))];
                if (! this.group || this.group.length == 0){
                    this.group = [this.groups[0]]
                } else {
                    let newgroups: any = []
                    this.group.forEach((d:any)=>{
                    if (this.groups.indexOf(this.group) <= -1){
                        newgroups.push(d)
                    }
                    })
                    this.group = newgroups
                }
                this.raw_data = data
                console.log(this.raw_data)
                this.updateData()
                this.updateCells()
            } else {
                data = (this.localDataHelper.parseJSON(string))
                this.groups = [...new Set(data.map((d: any) => d.group))];
                if (! this.group || this.group.length == 0){
                    this.group = [this.groups[0]]
                } else {
                    let newgroups: any = []
                    this.group.forEach((d:any)=>{
                    if (this.groups.indexOf(this.group) <= -1){
                        newgroups.push(d)
                    }
                    })
                    this.group  = newgroups
                }
                this.raw_data = data
                this.updateData()
                this.updateCells()
            } 
        } catch(err){
            throw err
        }
    }
  
} 