<template>
  <div style="padding-top: 10px; width: 97%">
    <b-row>
      <b-col sm="12">
        <div id="heatmapDiv" ref="heatmapDiv">
        </div>
      </b-col>
    </b-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from 'vue-property-decorator'
import LocalDataHelper from '@/shared/LocalDataHelper'
import Parsing from '@/shared/Parsing'
import * as d3 from 'd3'
import { BIconArrowReturnRight } from 'bootstrap-vue';
// import { local } from 'd3';
// import fs from 'file-system'

@Component({})
export default class Heatmap extends Vue {

  private localDataHelper = new LocalDataHelper();
  private Parsing = new Parsing();

  $refs!: {
    heatmapDiv:HTMLElement
  }
  @Prop({ required: false, default: 7 })
  public depth_threshold!: number; 
  @Prop({ required: false, default: 0.2 })
  public frequency_threshold!: number
  @Prop({ required: false, default: 10 })
  public column_width!:  number
  @Watch('depth_threshold')
  onDepthChanged(value: number, oldValue: number) {
    console.log("depth changed")
  }
  @Watch('frequency_threshold')
  onFrequencyChanged(value: number, oldValue: number) {
    console.log("freq threshold changed")
  }
  @Watch('column_width')
  onColWidthChanged(value: number, oldValue: number) {
    console.log("col width changed")
  }
  test = null
  showMenu = false
  msg = 'Hello'
  height = 900
  boxHeight = 0
  width = 900
  boxSpacing = 0
  boxWidth = 0
  border = 0
  svgs = { }
  scaleX = d3.scaleBand()
  scaleColor = d3.scaleLinear()
  colors = {"start": "fff", "end": '#666699'}
  xAxisInner = { }
  xAxisGroup = { }
  
  color_range = 4
  divisionYScale = { }
  yAxisDivision = {}
  scaleY = d3.scaleOrdinal()
  yAxis = { }
  containerHeight = 500
  chartHeight = (this.containerHeight * 0.55)
  margin = {
    top: 0.05 * this.chartHeight,
    bottom: 0.05 * this.chartHeight,
    left: 0.05 * this.width,
    right: 0.05 * this.width
  }

  // need annotation due to `this` in return type
  greet(): string {
    return this.msg + ' world'
  }
  mounted() {
    this.defineHeatmap()
  }

  defineHeatmap() {
    // const $this = this
    this.height = Math.min(this.chartHeight)
    this.width = this.$refs.heatmapDiv.clientWidth
    const border = this.border
    const margin = this.margin
    // const exts = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'T', 'V', 'X', 'Y']
    const exts = ['A']
    // const segments = ['HA', 'M1', 'NA', 'NP', 'NS1', 'PA', 'PB1', 'PB2']
    const segments = ['NP']
    const boxSpacingX = (this.width - margin.left - margin.right) / segments.length
    // const boxSpacingY = (this.height - margin.bottom - margin.top) / this.classifiers.length
    const boxSpacingY = 20
    
    // const bottomPosition = Math.min((this.height - margin.top-margin.bottom), this.classifiers.length * 70)
    // const boxHeight = (((this.height - margin.top - margin.bottom) / this.classifiers.length) - border)
    const boxHeight = 20
    this.boxHeight = boxHeight
    
    

    const divisionYScale = d3.scaleBand<string>()
      .domain(['a', 'b'])
      .range([this.margin.left, this.width - this.margin.right])
    // const yAxisDivision = d3.axisLeft<string>().scale(divisionYScale).tickSizeOuter(0)
    //   .ticks(0);
    // this.yAxisDivision[element] = { L2: null, AUPRC: null }
    
    const promises: Object[] = []
    // const data: {groups: Object[], positions: Object[]} = {
    //   groups: [],
    //   positions: []
    // };
    
    segments.forEach((segment)=>{
      promises.push(this.localDataHelper.readTSVNoHeader(`Gaydos/grouped/${segment}/ann-condition.txt`, ["APLSample", "Group","Experiment"]))
      exts.forEach((d) => {
        promises.push(this.localDataHelper.readTSV(`Gaydos/grouped/${segment}/${d}.subset.txt`))
      })
    })
    const $this = this    
    Promise.all(promises).then((l)=>{
      let data = {groups: l[0], positions: l[1]};

      $this.makeHeatmap(data)
      $this.updateHeatmap(data)
    })
  }
  makeHeatmap(data: any){
    const svg = d3.select("#heatmapDiv").append("svg").attr("id", "heatmapSVG")
    .attr("id", "heatmapSVG")
          .attr('viewBox', `0 0 ${this.width} ${this.chartHeight}`)
    const $this = this
    const g = svg.append("g").attr("class", "svgG")
    
    let filtered_attrs = Object.keys(data.positions[0]).filter((d:any)=>{return d !== 'prep_id'})
    let cells: any = [].concat.apply([], data.positions.map((d:any)=>{
      return filtered_attrs.map((f:string)=>{ 
        return {'prep_id': d.prep_id, 'value': d[f], 'attr': f}
      })
    }))
    const boxWidth = ((this.width - this.margin.left - this.margin.right) / filtered_attrs.length) - this.border
    this.boxWidth = boxWidth
    // const firstObj : any = [...new Set(data.positions.map( (d:any) => d.attr))]; 
    const firstObj = filtered_attrs
    let preps: any = [...new Set(cells.map( (d:any) => d.prep_id))]; 
    this.scaleX.domain(firstObj).range([this.margin.left, this.width - this.margin.right])
    
    this.scaleY.domain(preps)
    .range(preps.map((d:any, i: number) => {
      const spacing = this.boxHeight / 2
      return (i * this.boxHeight) + spacing + this.margin.top
    }))
    let color_array: string[] = [$this.colors.start, $this.colors.end]
    let range = [0, d3.max(cells, (d:any) => { return +d.value})]
    this.scaleColor.domain(range).range(color_array)
    console.log(this.scaleColor.domain(), this.scaleColor.range())
    const blocks = g.selectAll(".block").data(cells)
    const blockEnter = blocks.enter().append("g")
      .attr("transform", (d: any) => {
        let y = $this.scaleY(d.prep_id)
        let x  = $this.scaleX(d.attr)
        return "translate(" + x + "," + y + ")"
      }).attr("class", function (d) {
        return "block"
      }).attr("id", function (d: any) {
        return "g" + "-" + d.prep_id
      })
      .attr('class', "blockRect")
      .style("rx", "2px")
      .style("stroke", "black")
      .style("stroke-width", "0.5")
      .append("rect")
      .attr("fill", (d: any) => {
        return $this.scaleColor(d.value)
      })
      .attr("width", this.boxWidth)
      .attr("height", this.boxHeight)
      .attr("id", (d:any) => {
        return d.attr + "-" + d.prep_id
      })
      .on("mouseover", (d:any, u: any)=> {
        console.log(u,'over')
        // d3.select(u.attr + "-" + u.prep_id).attr("fill", 'red')
      }).on("mouseout", (d:any, u: any)=> {
        console.log(u, 'out')
        d3.select('#'+u.attr + "-" + u.prep_id).style("fill", 'yellow')
      })
      // .append("title").text(function (d) {
      //   return "Classifier: " + d.classifier_name + "\nRank: " + d.rank + "\nRead Type: " + d.read_type +
      //     "\n" + element + ": " + d[element]
      // })
    // .attr("transform", (d: any, i: number) => {
    //   console.log(d)
    //   return `translate(${this.scaleX(d.read_type)}, ${0})`
    // })
          
  } 
  updateHeatmap(data: any) {
    // console.log('Updating Heatmap now...', data)
    
  }
}
</script>
<style>

</style>
