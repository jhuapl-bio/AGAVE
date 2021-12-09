import * as d3 from 'd3'
import LocalDataHelper from "@/shared/LocalDataHelper";
import * as path from 'path';


interface StringMap { [key: string]: string; }

export default class DataHandler {
    sort: boolean = true
    referenceSequence: any = {}
    position_ranges: number[] = []
    xvalues: any[] = []
    pdb: any = null
    selected_data: any  = null
    selectedPosition: number = 1
    yvalues: any[] = []
    cells: any = null
    cells_full: any = null
    raw_data: any = null
    groups: any[] = []
    group: any[] = []
    samples: any[] = []
    sample: any[] = []
    protein: any = null
    proteins: any[] = []
    protein_map: any = {}
    organism: any = null
    organisms: any[] = []
    experiments: any[] = []
    isSwitched: boolean = true
    experiment: any = null
    discordantOnly: boolean = true
    frequency_threshold: number = 0
    depth_threshold: number = 0
    public localDataHelper = new LocalDataHelper()
    position_max: any = 1
    position_min: any = 1
    consensus_map: any  = null
    pdb_map: any  = {}
    selected_consensus: any = null
    public defaultDataListFile: any = path.join("data", "default.json")
    public defaultDataListFiles: any[] = [path.join("data", "default.json"), path.join("data", "BARDA_New.json"), path.join("data", "Gaydos.json")];
    data_selected: any  = null
    public  constructor() {
        this.data_selected = this.defaultDataListFile
    }
    public updateReference(referenceSequence: any){
        this.referenceSequence = referenceSequence
        
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
    public updateProtein(protein: any)
    {
        this.protein = protein
        this.pdb = this.pdb_map[this.organism][protein]
    }
    public changeExperiment(experiment: any )
    {
        this.experiment = experiment
        
    }
    public updateOrganism(organism: any )
    {
        this.organism = organism

    }
    public updateCells(){
        let cells_filtered= this.cells_full.filter((d:any)=>{
            return d.position >= this.position_ranges[0] && 
                d.position <= this.position_ranges[1] && 
                d.organism == this.organism && this.protein == d.protein
        })
        if (this.discordantOnly){
            cells_filtered = cells_filtered.filter((cell:any)=>{
                if (this.referenceSequence && cell.position in this.referenceSequence ){
                    cell.pdb_aa= `${this.referenceSequence[cell.position]}`
                } else {
                    cell.pdb_aa=`Unmapped`
                }
                if (!this.isSwitched){
                    return cell.aa !== cell.consensus_aa || (cell.count > 1 || cell.count ==1 &&  cell.depth > 0)
                } else {
                    return cell.aa !== cell.pdb_aa || (cell.count > 1 || cell.count ==1 &&  cell.depth > 0)

                }
            })
        }
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
        let genes = this.filter()
        let cells: any = []
        let seen_positions:any  = {}
        genes.forEach((gene:any)=>{
            seen_positions[gene.gene] = {}
            gene.residues.forEach((residue:any)=>{
                seen_positions[gene.gene][+residue.position]=1
            }) 
        })
        genes.forEach((gene: any)=>{
            let position_map: any = {}; 
            let current_position = 0     
            let seen_residue:any = {}
            let depths = gene.depths
            let organism = gene.organism
            // let protein = this.protein_map[organism][gene.gene]
            // this.pdb = this.pdb_map[this.organism][this.protein]
            if (!$this.pdb_map[organism]){
                $this.pdb_map[organism] = {}
            }

            gene.residues.forEach((residue:any)=>{
                let aa_count = 0
                position_map[residue.position] = 0
                seen_residue[residue.position]= 1
                let i: number = current_position;
                if (gene.pdb  ){
                    $this.pdb_map[organism][gene.gene] = gene.pdb
                }
                cells.push({ 
                    unique: residue.counts.map((d:any)=>{
                        if (residue.reference_aa == d.aa){
                            aa_count = d.count
                        }
                        return { aa: d.aa, proportion: (d.count / +residue.depth).toFixed(3)}
                    }),
                    protein:gene.gene, 
                    max: Math.max(aa_count, residue.consensus_aa_count), 
                    organism: gene.organism,
                    group: gene.group,
                    experiment: gene.sample, 
                    depth: residue.depth, 
                    position: +residue.position, 
                    total:+residue.depth, 
                    count: residue.counts.length, 
                    aa: residue.reference_aa,
                    aa_count: aa_count,
                    consensus_aa: residue.consensus_aa, 
                    consensus_count: residue.consensus_aa_count 
                })
            })
            let positions = depths.map((d:any, i:any)=>{
                return i+1
            })
            if (this.discordantOnly){
                positions = seen_positions
            }
            Object.keys(positions).forEach((position:any)=>{
                if (!seen_residue[position]){
                    let i = position-1
                    let protein = $this.protein_map[organism][gene.gene]
                    let depth = depths[i]
                    if (depth > 0){
                        let aa = protein[i]
                        cells.push({ 
                            unique: [ { aa: aa, proportion: 1}],
                            protein:gene.gene, 
                            max: depth, 
                            organism: gene.organism,
                            group: gene.group,
                            experiment: gene.sample, 
                            depth: depth, 
                            position: i+1, 
                            total:+depth, 
                            count: 1, 
                            aa: aa,
                            aa_count: depth,
                            consensus_aa: aa, 
                            consensus_count: depth
                        })
                    }
                } 
            })
        })
                  
        const min: any = d3.min(cells.map((d:any)=>{return +d.position}))
        const max: any = d3.max(cells.map((d:any)=>{return +d.position}))
        this.position_max = max
        this.position_min = min
        this.position_ranges = [1, this.protein_map[this.organism][this.protein].length]
        this.pdb = this.pdb_map[this.organism][this.protein]
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
    public filter(){
        const $this =this;
        let data =  $this.selected_data
        
        let organisms: any = Object.entries(data.proteins)
        for (const [ organismId, organismProts ] of organisms ){
            let proteins:any= Object.entries(organismProts)
            if ( !(organismId in $this.protein_map)){
                $this.protein_map[organismId] = {}
            }
            let obj_org = Object.entries(organismProts)
            for (const [prot, protValue] of obj_org){
                $this.protein_map[organismId][prot] = protValue
            }
        }
                
        
        let data_filtered = [].concat.apply([], data.entries.map((d:any)=>{
            return d.organisms.map((organism: any)=>{
                organism.experiment = d.experiment;
                organism.group = d.group;
                organism.sample = d.sample 
                return organism
            })
        }))
        $this.organisms = [ ... new Set(data_filtered.map((d:any)=>{return d.organism}))]
        
        if (!$this.organism || $this.organisms.indexOf($this.organism) == -1 ) { $this.organism = $this.organisms[0] } 
        data_filtered  = [].concat.apply([], data_filtered.filter((d:any)=>{
            return d.organism == $this.organism
        }).map((d:any)=>{
            return d.genes.map((gene:any)=>{
                gene.experiment = d.experiment;
                gene.group = d.group;
                gene.sample = d.sample;
                gene.organism = d.organism
                return gene
            })
        })
        )
        $this.samples = [ ...new Set(data_filtered.map((d: any) => {return d.sample}))];
        let sample: any  = $this.samples
        $this.groups = [...new Set(data_filtered.map((d: any) => {return  d.group}))];
        let group: any  = $this.parseGroups($this.group, $this.groups)
        $this.proteins = [ ... new Set(data_filtered.map((d:any)=>{return d.gene}))]
        
        if (!$this.protein || $this.proteins.indexOf($this.protein) == -1){ $this.protein = $this.proteins[0] }
        if (!this.sample || this.sample.length == 0) { this.sample = this.samples }
        if (!this.organism  ) { this.organism = this.organisms[0] }
        if (!this.group|| this.group.length == 0 ) { this.group= this.groups}
        data_filtered = data_filtered.filter((d:any)=>{
            return $this.group.indexOf(d.group) > - 1  && $this.organism == d.organism && $this.sample.indexOf(d.sample) > -1
        })
        if (! ($this.protein in $this.protein_map[$this.organism])){
            $this.organisms.forEach((organism)=>{
                console.log(organism)
                if ($this.protein in $this.protein_map[organism]){
                    $this.organism = organism
                }
            })
        }else {
            console.log($this.protein_map)
        }

            

        return data_filtered

    }
        
    public async getData(string:any, type: string){
        const $this = this
        let data:any = null
        string = path.join(string)
        try{
            if (type == 'file'){
                data = await $this.localDataHelper.readJSON(string)
                defineData(data)
                $this.filter()
                return 
            } else {
                data = ($this.localDataHelper.parseJSON(string))
                defineData(data)
                $this.filter()
                // resolve()
                return
            }
            
        } catch(err){
            this.raw_data = []
            // this.cells = []
            // this.group = []
            throw err
        }
        function defineData(data: any){
            $this.experiments = data.map((d:any, i:number)=>{
                return {
                    id: i,
                    label: d.name

                }
            })
            if (!$this.experiment || $this.experiments.indexOf($this.experiment) == -1) { $this.experiment = $this.experiments[0] }
            $this.raw_data = data
            $this.selected_data = data[0] // Auto select the first experiment/entry in the first level 
            
        }
        
    }
} 