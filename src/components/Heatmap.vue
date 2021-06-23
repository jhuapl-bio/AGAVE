<template>
  <div style="padding-top: 10px; width: 100%; ">
    
    <b-row>
      <b-col sm="12">
        <div id="heatmapDiv" ref="heatmapDiv">
          <div class="tooltip" id="tooltipHeatmap" style="opacity: 0"></div>
        </div>
      </b-col>
      <b-col sm="12">
        <div id="heatmapLegend" ref="heatmapLegend"></div>
        <b-switch v-model="isSwitched" :disabled="this.referenceSequence.sequence.length <= 0">
                {{ ( isSwitched ? 'Consensus Sequence' : 'Reference' ) }}
        </b-switch>
      </b-col>
    </b-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from "vue-property-decorator";
import LocalDataHelper from "@/shared/LocalDataHelper";
import Parsing from "@/shared/Parsing";
import * as d3 from "d3";
import { BIconArrowReturnRight } from "bootstrap-vue";
// import { local } from 'd3';
// import fs from 'file-system'

@Component({})
export default class Heatmap extends Vue {

  private localDataHelper = new LocalDataHelper();
  private parsing = new Parsing();
  $refs!: {
    heatmapDiv: HTMLElement;
    heatmapLegend: HTMLElement;
  };

  @Prop({ required: false, default: 0 })
  public depth_threshold!: number;

  @Prop({ required: true, default: "HA" })
  public segment!: string;

  @Prop({ required: false, default: 0.2 })
  public frequency_threshold!: number;

  @Prop({ required: false, default: 6 })
  public column_width!: number;

  @Prop({ required: false, default: 10 })
  public group!: string;

  @Prop({ required: false, default: { positions: [], sequence: [] } })
  public referenceSequence!: any;

  @Watch("depth_threshold")
  onDepthChanged(value: number, oldValue: number) {
    this.updateHeatmap(this.cells)
    // this.defineHeatmap();
  }
  @Watch("isSwitched")
  onDSwitchedChange(value: boolean, oldValue: boolean) {
    this.updateHeatmap(this.cells)
  }
  // @Watch("referenceSequence")
  // onReferenceSeq(value: any, oldValue: any) {
  // }

  @Watch("frequency_threshold")
  onFrequencyChanged(value: number, oldValue: number) {
    this.updateHeatmap(this.cells)
    // this.defineHeatmap();
  }

  @Watch("column_width")
  onColWidthChanged(value: number, oldValue: number) {
    this.updateHeatmap(this.cells)
  }

  @Watch("segment")
  onSegChanged(value: string, oldValue: string) {
    // d3.selectAll("#heatmapSVG").remove()
    this.defineHeatmap();
  }

  @Watch("group")
  onGroupChanged(value: string, oldValue: string) {
    d3.select("#heatmapDiv").html("");
    this.defineHeatmap();
    
  }
  isSwitched = true;
  test = null;
  reference_seq: any = [];
  showMenu = false;
  msg = "Hello";
  height = 900;
  boxHeight = 0;
  width = 900;
  boxSpacing = 0;
  boxWidth = 0;
  overwidth: number = 0;
  border = 0;
  svgs = {};
  scaleX = d3.scaleBand();
  scaleColor = d3.scaleLinear();
  colors = { start: "#fff", end: "#666699" };
  xAxisInner = {};
  xAxisGroup = {};
  xAxisGT: any = null;
  xAxisGB: any = null;
  yAxis: any = null;
  yAxisG: any = null;
  xAxisT: any = null;
  xAxisB: any = null;
  g: any  = null;
  cells: any[] = [];
  color_range = 4;
  divisionYScale = {};
  yAxisDivision = {};
  scaleY: any= d3.scaleOrdinal();
  positions_unique: any[] = [];
  positions: any[] = [];
  containerHeight = 500;
  chartHeight = this.containerHeight * 0.55;
  legendWidth = 0;
  legendHeight = 0;
  legendPadding = 15;
  svg:any = null
  margin = {
    top: 0.075 * this.chartHeight,
    bottom: 0.1 * this.chartHeight,
    left: 0.2 * this.width,
    right: 0.05 * this.width,
  };
  x: any = d3.scaleLinear()
    
  // need annotation due to `this` in return type
  greet(): string {
    return this.msg + " world";
  }
  mounted() {
    this.defineHeatmap();
  }

  defineHeatmap() {

    this.legendWidth = this.$refs.heatmapLegend.clientWidth;
    this.legendHeight = this.chartHeight / 5
    this.height = Math.min(this.chartHeight);
    this.width = this.$refs.heatmapDiv.clientWidth;
    const border = this.border;
    const margin = this.margin;
    d3.selectAll("#heatmapSVG").remove()
    d3.select("#overflowDiv").remove()
    d3.selectAll("#heatmapLegend").selectAll("*").remove()
    // const exts = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'T', 'V', 'X', 'Y']
    // const exts = ['A']
    // const segments = ['HA', 'M1', 'NA', 'NP', 'NS1', 'PA', 'PB1', 'PB2']
    const segments = ["HA", "M1", "NA", "NP"];

    const boxSpacingX = (this.width - margin.left - margin.right) / 1;
    // const boxSpacingY = (this.height - margin.bottom - margin.top) / this.classifiers.length
    const boxSpacingY = 20;

    // const bottomPosition = Math.min((this.height - margin.top-margin.bottom), this.classifiers.length * 70)
    // const boxHeight = (((this.height - margin.top - margin.bottom) / this.classifiers.length) - border)

    const divisionYScale = d3
      .scaleBand<string>()
      .domain(["a", "b"])
      .range([this.margin.left, this.width - this.margin.right]);

    const promises: Object[] = [];
    // segments.forEach((segment: string) => {
    promises.push(
      this.localDataHelper.readJSON(`Gaydos/grouped/${this.segment}.json`)
    );
    // });
    const $this = this;
    Promise.all(promises).then((l) => {
      let data = l[0];

      $this.makeHeatmap(data);
      // $this.updateHeatmap(data)
    });
  }
  
  makeHeatmap(raw_data: any) {
    let data = raw_data.filter( (d:any) => {
      return d.group == this.group;
    })
    // Get unique preps in order to calculate y axis
    let preps: any = [...new Set(data.map((d: any) => d.experiment))];
    
    // Format data into cells
    let cells: any[] = [];
    data.forEach((prep:any)=>{
      prep.residues.forEach((residue:any)=>{
        
        cells.push({ max: residue.consensus_aa_count, experiment: prep.experiment, depth: residue.depth, position: +residue.position, total:+residue.depth, count: residue.counts.length, aa: residue.consensus_aa, consensus_count: residue.consensus_aa_count  })
      })
    })
    this.cells = cells
    // Get unique positions in order to calculate x axis
    const position_max: any = d3.max(cells.map((d:any)=>{
      return d.position 
    }));
    
    const axisPadding = 10
    this.x.domain([0, position_max])
    .range([this.margin.left, this.width * this.column_width - this.margin.right])
    const minX = this.x(0);
    const maxX = this.x(position_max);
    const overwidth = maxX - minX + this.margin.left + this.margin.right;
    this.overwidth = overwidth
    const boxHeight = (this.height - this.margin.top - this.margin.bottom - axisPadding)/ preps.length 
    this.boxHeight = boxHeight;

    
    const heatmapdiv = d3.select("#heatmapDiv")
    const svg = heatmapdiv.append("svg")
      .attr("id", "heatmapSVG")
      .attr("width", this.width)
      .attr("height", this.chartHeight)
      .style("position", "absolute")
      .style("pointer-events", "none")
      .style("z-index", 1)
      // .attr("viewBox", `0 0 ${this.width} ${this.chartHeight}`)
    this.svg = svg
    const body = heatmapdiv.append("div").attr("id","overflowDiv")
      .style("overflow-x", "scroll")
      .style("-webkit-overflow-scrolling", "touch");

    const innerSvg = body.append("svg")
      .attr("id", "innerheatmapSVG")
      .attr("height", this.chartHeight)
      .style("display", "block")
    const g = innerSvg.append("g").attr("class", "svgG")
    this.g = g
    const $this = this;
    
    this.scaleY.domain(preps).range(
      preps.map((d: any, i: number) => {
        const spacing = this.boxHeight / 2;
        return i * this.boxHeight + spacing + this.margin.top;
      })
    );
    
    this.xAxisGT = g.append("g")
    .attr("class", "xAxis")
    .attr("id", "xAxisT")
    this.xAxisGB = g.append("g").attr("class", "xAxis")
    .attr("id", "xAxisB")
    this.yAxis = d3.axisLeft(this.scaleY)
          .ticks(preps);
    this.yAxisG = g.append("g").attr("class", "yAxis")
          .attr("transform", "translate(" + this.margin.left + "," + (this.boxHeight/2)+ ")")
          .style("stroke-width", 0)
          .call(this.yAxis)
          .call(g => g.select(".domain").remove())
          .selectAll('text')
          .style('text-anchor', 'end')
          .attr('transform', 'rotate(0)').style("font-size", "1.2em")

    let legendVals = [];
    for (let i = -5; i <= 0; i+=0.25) {
      legendVals.push(i)
    }
    const legend_margin: number= this.legendWidth - this.legendPadding
    const boxWidth = this.legendWidth / 4 / legendVals.length

    d3.select('#heatmapLegend')
    .append("svg")
    .attr("width", this.legendWidth)
    .attr("height", this.legendHeight)
    .attr("transform", `translate(${0},${this.legendPadding})`)
    .append("g")
    .attr("class", "legendG")
    .attr("transform", `translate(${this.legendWidth / 2},${0})`)
    .selectAll("rect")
    .data(legendVals).enter().append("rect")
    .attr("stroke-width", 0)
    .attr("x", (d:any, i:number)=>{
      return (boxWidth* i ) 
    })
    .attr("y",  0)
    .attr("id", (d:any)=>{
      return "_"+String(d).replace("-", "_").replace(".", "_")
    })
    .attr("width", boxWidth)
    .attr("height", this.legendPadding) 
    .style("fill", (d:any)=>{
      const frac = (d + 3.5 ) / 3.5    
      let col = this.frac2Color(frac)
      return col
    })
    .on("mouseenter", (d:any, u:any)=>{
      d3.select("#_"+String(u).replace("-", "_").replace(".", "_"))
      .attr("stroke-width", 2)
      .attr("stroke", "#000")
      const fract = (u + 3.5 ) / 3.5 
      d3.selectAll(".block")
      .style("fill", (block:any, i:any)=>{
        if (this.getFrac(block) >= fract){
          return "rgb(217, 33, 32)"
        } else{
          return this.calculateColor(block)
        }
        
      })
    })
    .on("mouseleave", (d:any, u:any)=>{
      d3.select("#_"+String(u).replace("-", "_").replace(".", "_"))
      .attr("stroke-width", 0)
      d3.selectAll(".block")
      .style("fill", (block:any, i:any)=>{
        return this.calculateColor(block)
      })
    })
    .style("cursor", "pointer")
    .append("title")
    .attr("class", "tt").text((d:number)=>{
      let cutoff = Math.round(3-Math.log10(Math.pow(10,d)));
      return (Math.pow(10,d)*100).toString().substring(0,cutoff)+"%";
    })
    const legendScaleY: any = d3.scaleLinear().domain([-5, 0]).range([boxWidth / 2, (boxWidth * legendVals.length ) - boxWidth/2   ])
    const legendYAxis: any = d3.axisBottom(legendScaleY)
    .ticks(6)
    .tickFormat((d:any,i:any) => {
      const val: any= parseFloat((Math.pow(10,d)*100).toFixed(3) )
      return ((val > 0.01 ? val : val.toExponential()) + "%")
    });
    d3.select("#heatmapLegend").select(".legendG")
      .append("g")
      .attr("class", "legendyAxis")
      .attr("id", "legendyAxis")
      .attr("transform", "translate(" + (0) + "," + this.legendPadding+ ")")
      .style("stroke-width", 1)
      .call(legendYAxis)
      .selectAll('text')
      .style('text-anchor', 'start')
      .attr('transform', 'rotate(0)').style("font-size", "0.79em")
    d3.select("#heatmapLegend")
      .select("svg")
      .append("text")
      .attr("x", (this.legendWidth/2 ) - (this.legendPadding))
      .attr("y", this.legendPadding)
      .attr("dy", "-0.25em")
      .attr("text-anchor", "end")
      .attr("transform", "rotate(0)")
      .attr("id", "legendYAxisTitle")
      .attr("font-size", "0.8em")
      .text("Relative Depth of Mutations")
    this.updateHeatmap(cells)
  }

  updateHeatmap(cells:any) {
    // Add styling to the heatmap blocks
    const g = this.g
    const $this = this
    if (this.isSwitched){
      const positions_unique = [...new Set(cells.map((d:any)=>{
        return d.aa + "." + d.position
      }))];
      // Get unique positions in order to calculate x axis
      const positions: any[] = [...new Set(cells.map((d:any)=>{
        return d.position 
      }))];
      this.positions_unique = positions_unique
      this.positions = positions
    } else {
      this.positions_unique = this.referenceSequence.sequence
      const positions: any[] = this.referenceSequence.positions
      this.positions = positions
    }
    const min = d3.min($this.positions)
    const max = d3.max($this.positions)
    this.x.domain([1, this.positions.length])
    .range([this.margin.left, this.width * this.column_width - this.margin.right])
    const minX = this.x(1);
    const maxX = this.x(this.positions.length);
    const overwidth = maxX - minX + this.margin.left + this.margin.right;
    this.overwidth = overwidth
    const boxWidth =
      (this.overwidth - this.margin.left - this.margin.right) / this.positions.length -
      this.border;
    this.boxWidth = boxWidth;
    this.scaleX
      .domain(this.positions)
      .range([this.margin.left, overwidth - this.margin.right]);
    this.xAxisT = d3
      .axisTop(this.scaleX)
      .tickSizeOuter(0)
      .ticks(max - min)
      .tickFormat((interval:any,i:any) => {
        return i%2 !== 0 ? " ": this.positions_unique[i];
      });
    this.xAxisB = d3
    .axisBottom(this.scaleX)
    .tickSizeOuter(0)
    .ticks(max - min)
    .tickFormat((interval:any,i:any) => {
      return i%2 !== 1 ? " ": this.positions_unique[i];
    });
    d3.select('#xAxisT')
          .attr("transform", "translate(" + (0) + "," + (this.margin.top) + ")")
          .style("fill", null)
          .style("stroke-width", 0.2)
          .call(this.xAxisT)
          .selectAll('text')
          .attr("y", -9)
          .attr("x", 0)
          .attr("dy", ".35em")
          .style("font-size", "0.8em")
          .attr("transform", "rotate(45)")
          .style("text-anchor", "end");
    d3.select('#xAxisB')
          .attr("transform", "translate(" + (0) + "," + (this.chartHeight - this.margin.bottom) + ")")
          .style("fill", null)
          .style("stroke-width", 0.2)
          .call(this.xAxisB)
          .selectAll('text')
          .attr("y", 0)
          .attr("x", 9)
          .attr("dy", ".35em")
          .style("font-size", "0.8em")
          .attr("transform", "rotate(45)")
          .style("text-anchor", "start");

    d3.select('#innerheatmapSVG')
    .attr("width", overwidth)
    const blocks = g.selectAll(".block").data(cells.filter((d:any)=>{
                return d.position >= min && d.position <= max && this.positions.indexOf(d.position) > -1
              }), (d:any, i:any)=>{
      d.experiment.replaceAll(" ", "_") + d.position + $this.segment
    })
    .join(
      function (enter: any) {
            return enter
              .append("rect")
              .attr("id", (d: any) => {
                return (
                  d.experiment.replaceAll(" ", "_") + d.position
                );
              })
              .attr("fill", (d: any) => {
                return $this.calculateColor(d)
              })
              .attr("transform", (d: any) => {
                let y = $this.scaleY(d.experiment);
                let x = $this.scaleX(d.position);
                return "translate(" + x + "," + y + ")";
              })
              .attr("class", "block")
              .style("cursor", "pointer")
              .attr("width", $this.boxWidth )
              .attr("height", $this.boxHeight)
              .on("click", (d:any, u:any)=>{
                $this.$emit("changePosition", u.position)
              })
              .on("mousemove", (event: any, u: any, n:any, i:number) => {
                // console.log(d3.select(
                //   "#" +
                //     u.experiment.replaceAll(" ", "_") + u.position 
                // )._groups[0], u.experiment, u.position, u.experiment.replaceAll(" ", "_") + u.position)
                d3.select(
                  "#" +
                    u.experiment.replaceAll(" ", "_") + u.position 
                )
                .style("fill", "yellow");
                d3.select("#tooltipHeatmap")
                  .html(`Pos: ${u.position}<br> Experiment: ${u.experiment}<br>Depth: ${u.count}, Total: ${u.total}<br> Consensus Residue: ${u.aa} ${( !$this.isSwitched ? `<br>Ref. Residue: ${$this.positions_unique[$this.positions.indexOf(u.position)]}`: '')} `)
                  .style(
                    "left",
                    () => {
                      const w: any = (d3.select("#tooltipHeatmap").node() ? (d3.select("#tooltipHeatmap").node() as any).getBoundingClientRect().width : 0 )
                      return ( d3.pointer(event, $this.svg.node() )[0] - w ) + "px"
                    }
                  )
                  .style(
                    "top",
                    () => {
                      const h: any = (d3.select("#tooltipHeatmap").node() ? (d3.select("#tooltipHeatmap").node() as any).getBoundingClientRect().height : 0 )
                      return (d3.pointer(event, $this.svg.node() )[1] - h ) + "px"
                    }
                  )
                  .style("opacity", "1");
              })
              .on("mouseleave", (d: any, u: any) => {
                d3.select(
                  "#" +
                    
                    u.experiment.replaceAll(" ", "_") + u.position
                )
                .style("fill", (d: any) => {
                  return $this.calculateColor(d)
                });
                d3.select("#tooltipHeatmap").style("opacity", "0");
              });
          },
          function (update: any) {
            return update
            .call((update: any)=>update.transition().duration(1000).attr("fill", (d: any) => {
              return $this.calculateColor(d)
            })
            .attr("transform", (d: any) => {
              let y = $this.scaleY(d.experiment);
              let x = $this.scaleX(d.position);
              return "translate(" + x + "," + y + ")";
            })
            .attr("width", $this.boxWidth )
            )            
          },
          function (exit: any) {
            console.log(exit)
            return exit.remove()
          }
        )


      
  }
  frac2Color(frac: number){
    let color = '';
    const x = 0.25 + 0.75*frac;
    const r = 255 * (0.472 - 0.567*x + 4.05*Math.pow(x,2)) / (1 + 8.72*x - 19.17*Math.pow(x,2) + 14.1*Math.pow(x,3));
    const g = 255 * (0.108932 - 1.22635*x + 27.284*Math.pow(x,2) - 98.577*Math.pow(x,3) + 163.3*Math.pow(x,4) - 131.395*Math.pow(x,5) + 40.634*Math.pow(x,6));
    const b = 255 / (1.97 + 3.54*x - 68.5*Math.pow(x,2) + 243*Math.pow(x,3) - 297*Math.pow(x,4) + 125*Math.pow(x,5));
    if( r < 0 || g < 0 || b < 0 ){
      color = 'rgb(253,64,160)'
    } else {
      color = 'rgb(' + Math.round(r) + ',' + Math.round(g) + ',' + Math.round(b) + ')';
    }
    return color
  }

  getFrac(d:any){
    const log_scale = 4
    const max = d.max
    return(log_scale+Math.log10(1-max/d.total))/log_scale;
  }
  // pretty close to exactly Tom's color code
  calculateColor(d: any) {

   	const depth_thresh = this.depth_threshold
    const freq_thresh = this.frequency_threshold
    const max = d.max
    let color = '';
    let colors: string[] = [
      'rgb(' + Math.round(235) + ',' + Math.round(235) + ',' + Math.round(235) + ')',
      'rgb(' + Math.round(185) + ',' + Math.round(185) + ',' + Math.round(185) + ')',
      'rgb(' + Math.round(165) + ',' + Math.round(165) + ',' + Math.round(165) + ')',
      'rgb(' + Math.round(65) + ',' + Math.round(65) + ',' + Math.round(65) + ')',
      'rgb(253,64,160)'
    ] 
    if ( d.total === 0 ) {
      // there is no data at this point: total = 0
      color = colors[0]

    // } else if ((1-max/d.total) < freq_thresh) {
    } else if ( d.total < depth_thresh && (1-max/d.total) < freq_thresh) {
      // there is little data at this point: 0 < total < depth_thresh
      color = colors[1]

    } else if ( max == d.total && d.total >= depth_thresh ) {
      // there is enough data at this point, but zero mutations: total >= depth_thresh; wt = total
      color = colors[2]

    } else if ( max != d.total && d.total < depth_thresh && (1-max/d.total) >= freq_thresh ) {
      // there is little data at this point, but a lot of mutations: total < depth_thresh; 1-wt/total > freq_thresh
      color = colors[3]

    } else {
      const frac = this.getFrac(d)
      // const frac = 0.25 + 0.75*(1-max/d.total)
      const scale:any = [ '#82e09b', '#a82716' ]
      // const scale:any = ['rgb(67.55129842486164,124.14024251953126,191.36399613050745)', 'rgb(16.88709677419362,32.7884100000022,31.8352059925094']
      const scaleLog:any = d3.scaleSequentialLog([0.25, 1], scale)
      // there is data at this point, and at least one mutation: total > 0; wt != total
      color = this.frac2Color(frac)
      // color = scaleLog(frac)

    }
    return color;

  }

}
</script>
<style>
</style>
