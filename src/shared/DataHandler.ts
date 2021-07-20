import * as d3 from 'd3'
import LocalDataHelper from "@/shared/LocalDataHelper";

interface StringMap { [key: string]: string; }

export default class DataHandler {
    sort: boolean = true
    referenceSequence: number[] = []
    position_ranges: number[] = []
    xvalues: any[] = []
    pdb: any = null
    selectedPosition: number = 0
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
    defaultDataList: any = [
        {
            id: "New",
            label: "BARDA",
            virus: "H1N1",
            subfolder: "grouped"
        },
        {
            id: "Gaydos",
            label: "Gaydos",
            virus: "H3N2",
            subfolder: "grouped"
        }
    ]
    data_selected: any  = null
    subtype: string = "H1N1"
    public  constructor() {
        this.data_selected = this.defaultDataList[0]
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
    public fullUpdate(){
        this.updateData()
        this.updateCells()
        return
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
                cells.push({ 
                    unique: residue.counts.map((d:any)=>{
                        return { aa: d.aa, proportion: (d.count / +residue.depth).toFixed(3)}
                    }),
                    segment:this.segment, 
                    max: residue.consensus_aa_count, 
                    experiment: prep.experiment, 
                    depth: residue.depth, 
                    position: +residue.position, 
                    total:+residue.depth, 
                    count: residue.counts.length, 
                    aa: residue.consensus_aa, 
                    consensus_count: residue.consensus_aa_count  
                })
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
    private parseGroups(group: any, groups: any){
        let grp
        if (! group || group.length == 0){
            grp = [groups[0]]
        } else {
            let newgroups: any = []
            group.forEach((d:any)=>{
                if (groups.indexOf(group) <= -1){
                    newgroups.push(d)
                }
            })
            if (newgroups.length == 0){
                grp = newgroups[0]
            } else {
                grp = newgroups
            }
        }
        return grp
    }
    public async getData(string:any, type: string){
        const $this = this
        let data:any = null
        try{
            if (type == 'file'){
                data = await $this.localDataHelper.readJSON(string)
                update(data)
                return 
            } else {
                data = ($this.localDataHelper.parseJSON(string))
                update(data)
                // resolve()
                return
            }
            
        } catch(err){
            this.raw_data = []
            // this.cells = []
            // this.group = []
            throw err
        }

        function update(data: any){
            $this.groups = [...new Set(data.map((d: any) => d.group))];
            let group: any  = $this.parseGroups($this.group, $this.groups)
            $this.group = group
            $this.raw_data = data
        }
    }
} 