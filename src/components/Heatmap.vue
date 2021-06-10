<template>
  <div style="padding-top: 10px; width: 97%">
    <b-row>
      <b-col sm="12">
        <div id="heatmapDiv" ref="heatmapDiv">
          <div class="tooltip" id="tooltip" style="opacity: 0"></div>
        </div>
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
  };

  @Prop({ required: false, default: 0 })
  public depth_threshold!: number;

  @Prop({ required: true, default: "NP" })
  public segment!: string;

  @Prop({ required: false, default: 0.2 })
  public frequency_threshold!: number;

  @Prop({ required: false, default: 6 })
  public column_width!: number;

  @Prop({ required: false, default: 10 })
  public group!: string;

  @Watch("depth_threshold")
  onDepthChanged(value: number, oldValue: number) {
    console.log("depth changed");
    this.defineHeatmap();
  }

  @Watch("frequency_threshold")
  onFrequencyChanged(value: number, oldValue: number) {
    console.log("freq threshold changed");
    this.defineHeatmap();
  }

  @Watch("column_width")
  onColWidthChanged(value: number, oldValue: number) {
    console.log("col width changed");
    this.defineHeatmap();
  }

  @Watch("segment")
  onSegChanged(value: string, oldValue: string) {
    d3.select("#heatmapDiv").html("");
    this.defineHeatmap();
  }

  @Watch("group")
  onGroupChanged(value: string, oldValue: string) {
    d3.select("#heatmapDiv").html("");
    this.defineHeatmap();
  }

  test = null;
  showMenu = false;
  msg = "Hello";
  height = 900;
  boxHeight = 0;
  width = 900;
  boxSpacing = 0;
  boxWidth = 0;
  border = 0;
  svgs = {};
  scaleX = d3.scaleBand();
  scaleColor = d3.scaleLinear();
  colors = { start: "#fff", end: "#666699" };
  xAxisInner = {};
  xAxisGroup = {};

  color_range = 4;
  divisionYScale = {};
  yAxisDivision = {};
  scaleY: any= d3.scaleOrdinal();
  yAxis = {};
  containerHeight = 500;
  chartHeight = this.containerHeight * 0.55;
  margin = {
    top: 0.075 * this.chartHeight,
    bottom: 0.1 * this.chartHeight,
    left: 0.2 * this.width,
    right: 0.05 * this.width,
  };

  // need annotation due to `this` in return type
  greet(): string {
    return this.msg + " world";
  }
  mounted() {
    this.defineHeatmap();
  }

  defineHeatmap() {
    // const $this = this
    this.height = Math.min(this.chartHeight);
    this.width = this.$refs.heatmapDiv.clientWidth;
    const border = this.border;
    const margin = this.margin;
    d3.select("#heatmapDiv").selectAll("*").remove()
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
    segments.forEach((segment: string) => {
      promises.push(
        this.localDataHelper.readJSON(`Gaydos/grouped/${this.segment}.json`)
      );
    });
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
    // Get unique positions in order to calculate x axis
    
    
    // Format data into cells
    let cells: any[] = [];
    data.forEach((prep:any)=>{
      prep.residues.forEach((residue:any)=>{
        cells.push({ experiment: prep.experiment, position: +residue.position, total:+residue.depth, count: residue.counts.length, aa: residue.consensus_aa, consensus_count: residue.consensus_aa_count  })
      })
    })
    const positions_unique: any[] = [...new Set(cells.map((d:any)=>{
      return d.aa + "." + d.position
    }))];
    const x: any = d3.scaleLinear()
    .domain([0, positions_unique.length])
    .range([this.margin.left, this.width * this.column_width - this.margin.right])
    const axisPadding = 10
    const minX = x(0);
    const maxX = x(positions_unique.length);
    const overwidth = maxX - minX + this.margin.left + this.margin.right;
    const boxHeight = (this.height - this.margin.top - this.margin.bottom - axisPadding)/ preps.length 
    this.boxHeight = boxHeight;
    const boxWidth =
      (overwidth - this.margin.left - this.margin.right) / positions_unique.length -
      this.border;
    this.boxWidth = boxWidth;
    
    const heatmapdiv = d3.select("#heatmapDiv")
    const svg = heatmapdiv.append("svg")
      .attr("id", "heatmapSVG")
      .attr("width", this.width)
      .attr("height", this.chartHeight)
      .style("position", "absolute")
      .style("pointer-events", "none")
      .style("z-index", 1)
      // .attr("viewBox", `0 0 ${this.width} ${this.chartHeight}`)
    const body = heatmapdiv.append("div")
      .style("overflow-x", "scroll")
      .style("-webkit-overflow-scrolling", "touch");

    const innerSvg = body.append("svg")
      .attr("width", overwidth)
      .attr("height", this.chartHeight)
      .style("display", "block")
    const g = innerSvg.append("g").attr("class", "svgG")
      // .call(svg => svg.append("g").call(xAxis))
    // body.node().scrollBy(overwidth, 0);
    const $this = this;

    
    this.scaleX
      .domain(positions_unique)
      .range([this.margin.left, overwidth - this.margin.right]);

    this.scaleY.domain(preps).range(
      preps.map((d: any, i: number) => {
        const spacing = this.boxHeight / 2;
        return i * this.boxHeight + spacing + this.margin.top;
      })
    );

    // Do some stuff with colors
    // let color_array: any[] = [$this.colors.start, $this.colors.end];
    // let range: any[] = [
    //   0,
    //   d3.max(cells, (d: any) => {
    //     return +d.value;
    //   }),
    // ];
    // const extentcolor: any = d3.extent(cells.map((d:any)=>{
    //   return d.count / d.total
    // }))
    // console.log(extentcolor, color_array)
    // console.log(cells.map((d:any) => { return d.total}))
    // this.scaleColor.domain(extentcolor).range(color_array);

    // Add styling to the heatmap blocks
    const blocks = g.selectAll(".block").data(cells);
    
    const blockEnter = blocks
      .enter()
      .append("g")
      .attr("transform", (d: any) => {
        let y = $this.scaleY(d.experiment);
        let x = $this.scaleX(d.aa + "." + d.position);
        return "translate(" + x + "," + y + ")";
      })
      .attr("class", function (d) {
        return "block";
      })
      .attr("id", function (d: any) {
        return "g" + "_" + d.experiment.replaceAll(" ", "_");
      })
      .attr("class", "blockRect")
      // .style("rx", "2px")
      // .style("stroke", "black")
      // .style("stroke-width", "0.5")

      .append("rect")
      .attr("id", (d: any) => {
        return (
          d.experiment.replaceAll(" ", "_") + d.position
        );
      })
      .attr("fill", (d: any) => {
        return this.calculateColor(d)
      })
      .style("cursor", "pointer")
      .attr("width", this.boxWidth )
      .attr("height", this.boxHeight)
      .on("click", (d:any, u:any)=>{
        $this.$emit("changePosition", u.position)
      })
      .on("mouseenter", (d: any, u: any) => {
        d3.select(
          "#" +
            u.experiment.replaceAll(" ", "_") + u.position 
        ).attr("fill", "yellow");
        
        d3.select("#tooltip")
          .html(`Pos: ${u.aa+"."+u.position}<br> Experiment: ${u.experiment}<br>Count: ${u.count}, Total: ${u.total}`)
          .style(
            "left",
            d.clientX - this.margin.right - this.margin.left + "px"
          )
          .style(
            "top",
            d.clientY - $this.margin.top - $this.margin.bottom + "px"
          )
          .style("opacity", "1");
      })
      .on("mouseleave", (d: any, u: any) => {
        d3.select(
          "#" +
            
            u.experiment.replaceAll(" ", "_") + u.position
        )
        .attr("fill", (d: any) => {
          return this.calculateColor(d)
        });
        d3.select("#tooltip").style("opacity", "0");
      });

    const xAxisT = d3
      .axisTop(this.scaleX)
      .tickSizeOuter(0)
      .ticks(positions_unique)
      .tickFormat((interval:any,i:any) => {
        return i%2 !== 0 ? " ": interval;
      });
    const xAxisB = d3
    .axisBottom(this.scaleX)
    .tickSizeOuter(0)
    .ticks(positions_unique)
    .tickFormat((interval:any,i:any) => {
      return i%2 !== 1 ? " ": interval;
    });
    const xAxisGT = g.append("g").attr("class", "xAxis")
          .attr("transform", "translate(" + (0) + "," + (this.margin.top) + ")")
          .style("fill", null)
          .style("stroke-width", 0.2)
          .call(xAxisT)
          .selectAll('text')
          .style('text-anchor', 'middle')
          .attr('transform', 'rotate(0)').style("font-size", "0.99em");
    const xAxisGB = g.append("g").attr("class", "xAxis")
          .attr("transform", "translate(" + (0) + "," + (this.chartHeight - this.margin.bottom) + ")")
          .style("fill", null)
          .style("stroke-width", 0.2)
          .call(xAxisB)
          .selectAll('text')
          .style('text-anchor', 'middle')
          .attr('transform', 'rotate(0)').style("font-size", "0.99em");
    const yAxis = d3.axisLeft(this.scaleY)
          .ticks(preps);
    const yAxisG = g.append("g").attr("class", "yAxis")
          .attr("transform", "translate(" + this.margin.left + "," + (this.boxHeight/2)+ ")")
          .style("stroke-width", 0)
          .call(yAxis)
          .call(g => g.select(".domain").remove())
          .selectAll('text')
          .style('text-anchor', 'end')
          .attr('transform', 'rotate(0)').style("font-size", "1.2em")
    function zoomed({transform}: any) {
      blocks.attr("transform", transform);
    }
    // const ext: any[] = [[0, 0], [$this.width, $this.height]]
    // svg.call(d3.zoom().extent(ext))
      
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
    console.log("Updating Heatmap now...", data);
  }

  // pretty close to exactly Tom's color code
  calculateColor(d: any) {

   	const depth_thresh = this.depth_threshold
    const freq_thresh = this.frequency_threshold/1000
    const log_scale = 4
    const max = d.consensus_count
    let color = '';

    if ( d.total === 0 ) {
      // there is no data at this point: total = 0
      color = 'rgb(' + Math.round(235) + ',' + Math.round(235) + ',' + Math.round(235) + ')';

    } else if ( d.total < depth_thresh && (1-max/d.total) < freq_thresh) {
      // there is little data at this point: 0 < total < depth_thresh
      color = 'rgb(' + Math.round(185) + ',' + Math.round(185) + ',' + Math.round(185) + ')';

    } else if ( max == d.total && d.total >= depth_thresh ) {
      // there is enough data at this point, but zero mutations: total >= depth_thresh; wt = total
      color = 'rgb(' + Math.round(165) + ',' + Math.round(165) + ',' + Math.round(165) + ')';

    } else if ( max != d.total && d.total < depth_thresh && (1-max/d.total) >= freq_thresh ) {
      // there is little data at this point, but a lot of mutations: total < depth_thresh; 1-wt/total > freq_thresh
      color = 'rgb(' + Math.round(65) + ',' + Math.round(65) + ',' + Math.round(65) + ')';

    } else {
      const frac = (log_scale+Math.log10(1-max/d.total))/log_scale;
      // there is data at this point, and at least one mutation: total > 0; wt != total
      const x = 0.25 + 0.75*frac;
      const r = 255 * (0.472 - 0.567*x + 4.05*Math.pow(x,2)) / (1 + 8.72*x - 19.17*Math.pow(x,2) + 14.1*Math.pow(x,3));
      const g = 255 * (0.108932 - 1.22635*x + 27.284*Math.pow(x,2) - 98.577*Math.pow(x,3) + 163.3*Math.pow(x,4) - 131.395*Math.pow(x,5) + 40.634*Math.pow(x,6));
      const b = 255 / (1.97 + 3.54*x - 68.5*Math.pow(x,2) + 243*Math.pow(x,3) - 297*Math.pow(x,4) + 125*Math.pow(x,5));
      if( r < 0 || g < 0 || b < 0 ){
        color = 'rgb(253,64,160)';
      } else {
        color = 'rgb(' + Math.round(r) + ',' + Math.round(g) + ',' + Math.round(b) + ')';
      }

    }
    return color;

  }

}
</script>
<style>
</style>
