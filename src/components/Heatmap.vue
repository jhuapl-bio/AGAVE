<template>
  <div style="width: 100%; ">    
    <b-row>
      <b-col class="col-lg-12 pb-1 d-flex">
        <div v-if="!DataHandler || DataHandler.cells.length < 1">
          <hr>
          <strong class="text-danger" >No data available</strong>
        </div>
        <div id="heatmapLabels" ref="heatmapLabels"></div>
        <div id="heatmapDiv" ref="heatmapDiv"  class="d-flex overflow-auto">
          <div class="tooltip"  id="tooltipHeatmap" style="opacity: 0; font-size: 16px; display:block">
            <div  id="tooltipcontent"></div>
            <b-table  striped hover :items="tooltiptable"
            :fields="[
              {
                key: 'aa',
                label: 'AA'
              },
              {
                key: 'proportion',
                label: 'Proportion',
              },
            ]"
            ></b-table>
          </div>
        </div>
      </b-col>
      <b-col class="col-lg-12 pb-1">
        <div id="heatmapSlider"  ref="heatmapSlider"></div>
      </b-col>
      <b-col class="col-lg-12 pb-1">
        <div id="heatmapLegend" ref="heatmapLegend"></div>
        <b-button @click="downloadSVG()">Save SVG</b-button>
        <a hidden id='imgId' target="_blank">Save SVG</a>
        <b-switch v-model="isFlipped" hidden :disabled="!DataHandler.cells" >
                {{ ( isFlipped ? 'Flip Axis' : 'Flip Axis' ) }}
        </b-switch>
      </b-col>
    </b-row>
    
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from "vue-property-decorator";
import LocalDataHelper from "@/shared/LocalDataHelper";
import * as d3 from "d3";
import * as canvas from 'canvas'
import DataHandler from "@/shared/DataHandler";

@Component({
  components: {}
})

export default class Heatmap extends Vue {

  public isFlipped = true
  $refs!: {
    heatmapDiv: HTMLElement;
    heatmapLegend: HTMLElement;
    heatmapSVG: HTMLElement;
  };
  @Prop({ required: false, default: 9 })
  public column_width!: number;
  @Prop({ required: true, default: null })
  public DataHandler!: DataHandler;
  @Prop({ required: false, default: true })
  public isSwitched!: any;
  @Prop({ required: false, default: true })
  public sortBy!: any;
  
  customfile: any = null
  scrollDirection: string = "x"
  partitions = 1
  position_max: number = 1
  position_ranges: number[] = [1,this.position_max]
  test = null;
  reference_seq: any = [];
  showMenu = false;
  msg = "Hello";
  tooltiptable: any = [];
  height = 900;
  boxHeight = 0;
  width = 900;
  boxWidth = 0;
  oversize: number = 0;
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
  context: any  = null;
  g: any  = null;
  color_range = 4;
  divisionYScale = {};
  yAxisDivision = {};
  scaleY: any= d3.scaleOrdinal();
  positions_unique: any[] = [];
  positions: any[] = [];
  preps: any  = null;
  containerHeight = 800;
  chartHeight = Math.min(this.containerHeight * 1);
  legendWidth = 0;
  legendHeight = 0;
  legendPadding = 15;
  svg:any = null
  margin = {
    top: 0.13 * this.chartHeight,
    bottom: 0.095 * this.chartHeight,
    left: 0.02 * this.width,
    right: 0.02 * this.width,
  };
  x: any = d3.scaleLinear()
  labelPaddingLeft: number = 15; // Bootstrap columns add 15px of padding which must be accounted for in yAxis transforms
    
  // Watchers that will update heatmap when user changes settings
  @Watch("sortBy")
  onSortByChanged(value: boolean, oldValue: boolean) {
    this.updateHeatmap()
  }
  @Watch("isSwitched")
  onSwitchChanged(value: boolean, oldValue: boolean) {
    this.updateHeatmap()
  }
 
  @Watch("column_width")
  onColWidthChanged(value: number, oldValue: number) {
    this.updateHeatmap()
  }

  // If user changes data used in heatmap
  changeDataHandler(){
    this.defineHeatmap()
  }

  parseError(err: any){
    console.log(err)
    if (err.toJSON){
      return err.toJSON().message
    } else {
      return  err
    } 
  }

  // Export button
  downloadSVG() {
    var svg:any = document.querySelector("#innerheatmapSVG");
    var svg_xml = (new XMLSerializer()).serializeToString(svg),
    blob = new Blob([svg_xml], {type:'image/svg+xml;charset=utf-8'}),
    url = window.URL.createObjectURL(blob);
    var img = new Image();
    const w = this.oversize
    const h = this.height
    img.width = this.oversize;
    img.height = h;
    const $this = this
    img.onload = function(){
      var canvas:any = document.createElement('canvas');
      d3.select('canvas').append("text").attr('transform', `translate(${w/2},${$this.margin.top/2})`).text("yyyyyyyyyyyyyyyyyyyyyyyyyy")
      canvas.width = w;
      canvas.height = h;

      var ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0, w, h);
      ctx.font = "20px Arial";
      ctx.fillText($this.DataHandler.protein, w / 2 , $this.margin.top / 2)
      window.URL.revokeObjectURL(url);
      var canvasdata = canvas.toDataURL('image/jpeg');
      var a: any = document.getElementById('imgId');
      a.download = "export_" + Date.now() + ".jpeg";
      a.href=canvasdata;
      a.click()  
    }
    img.src = url
    
  }

  // Vue lifecycle hook
  mounted() {
    if (this.DataHandler.cells){
      this.defineHeatmap()
    }
  }

  // Heatmap initialization, must be called again when user changes the data displayed
  defineHeatmap() {
    
    // Remove heatmap if it already exists
    d3.selectAll("#heatmapSVG").remove()
    d3.select("#overflowDiv").remove()
    d3.selectAll("#heatmapSliderSVG").remove()
    d3.selectAll("#heatmapLegend").selectAll("*").remove()
    d3.select("#labelsSVG").remove()

    // Create heatmap

    let cells = this.DataHandler.cells
  
    // Get unique positions in order to calculate x axis
    const position_max: any = d3.max(cells.map((d:any)=>{
      return d.position 
    }));
    this.position_max = position_max
    this.position_ranges = [1, position_max]

    // Get unique preps in order to calculate y axis
    let preps: any = [...new Set(cells.map((d: any) => d.experiment))];
    this.preps = preps
    
    // Create x axis
    if (this.scrollDirection == 'x'){
      this.x.domain([0, position_max])
      .range([this.margin.left, this.width * this.column_width - this.margin.right])
      const minD = this.x(0);
      const maxD = this.x(position_max);
      this.oversize = maxD - minD + this.margin.left + this.margin.right;
    } else {
      this.x.domain([0, position_max])
      .range([this.margin.top, this.height * this.column_width - this.margin.bottom])
      const minD = this.x(0);
      const maxD = this.x(position_max);
      this.oversize = maxD - minD + this.margin.top + this.margin.bottom;
    }

    // Create heatmap svg
    const heatmapdiv = d3.select("#heatmapDiv")
    const svg = heatmapdiv.append("svg")
      .attr("id", "heatmapSVG")
      .attr("ref", "heatmapSVG")
      .style("position", "absolute")
      .style("pointer-events", "none")
      .style("z-index", 1)
      .attr("viewBox", `0 0 ${this.width} ${this.chartHeight}`)
    this.svg = svg
    const body = heatmapdiv.append("div").attr("id","overflowDiv")
      .style("overflow-x", "scroll")
      .style("height", this.chartHeight)
    const innerSvg = body.append("svg")
      .attr("id", "innerheatmapSVG")
      .style("display", "block")
    if (this.scrollDirection == 'x'){
      innerSvg.attr("height", this.chartHeight)
    } else {
      innerSvg.attr("width", this.width)
    }
    const g = innerSvg.append("g").attr("class", "svgG")
    this.g = g
    const $this = this;
    this.xAxisGT = g.append("g")
    .attr("class", "xAxis")
    .attr("id", "xAxisT")
    this.xAxisGB = g.append("g").attr("class", "xAxis")
    .attr("id", "xAxisB")
    
    // Create labels svg
    const labelsDiv = d3.select("#heatmapLabels")
    const labelsSVG =labelsDiv.append("svg")
      .attr("id", "labelsSVG")
      .attr("ref", "labelsSVG")
      .style("pointer-events", "none")
      .style("z-index", 1)
      .style("height", "100%")
    const labelsG = labelsSVG.append("g").attr("class", "svgG")
    this.yAxisG = labelsG.append("g").attr("class", "yAxis").attr("id", "yAxis")
          
    // Create color legend
    try {
      this.legendWidth = Math.max(this.$refs.heatmapLegend.clientWidth, this.width);
      this.width =  Math.max(this.$refs.heatmapDiv.clientWidth, this.width);
    }catch (err){
      console.log(err)
    }
    this.legendHeight = this.chartHeight / 20
    this.height = Math.min(this.chartHeight);    

    let legendVals = [];
    for (let i = -5; i <= 0; i+=0.25) {
      legendVals.push(i)
    }
    const boxWidth = this.legendWidth / 4 / legendVals.length
    const legend_BoxHeight = this.legendHeight - this.legendPadding
    d3.select('#heatmapLegend')
    .append("svg")
    .attr("viewBox", `0 0 ${this.legendWidth} ${this.legendHeight}`)
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
    .attr("height", legend_BoxHeight) 
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
      .attr("transform", "translate(" + (0) + "," + legend_BoxHeight+ ")")
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
    
    // Create heatmap slider
    let contextheight = 70
    this.context = d3.select("#heatmapSlider")
    .append("svg").attr("id", "heatmapSliderSVG")
    .attr("viewBox", `0 0 ${this.width} ${contextheight}`)
    .append("g")
    .attr("class", "context")
    .attr("transform", `translate(${0},${0})`)
    let scaleX = d3.scaleLinear().domain([0, position_max])
    .range([0, this.width])
    let boxHeight = contextheight / preps.length
    let scaleY = d3.scaleOrdinal().domain(preps)
    .range(preps.map((d: any, i: number) => {
        const spacing = boxHeight / 2;
        return (i * boxHeight ) ;
      })
    );    
    let subBars = this.context.selectAll(".subBar").data(this.DataHandler.cells)
    .join(
      function (enter: any) {
        return enter
        .append("rect")
		    .classed('subBar', true)
        .attr("transform", (d: any, i: any) => {
          return "translate(" + scaleX(d.position) + "," + scaleY(d.experiment) + ")";
        })
             
        .style("cursor", "pointer")
        .attr("width", $this.width / position_max )
        .attr("height",  boxHeight )
        .attr("fill", (d: any) => {
          return $this.calculateColor(d)
        })
      },
      function (update: any){
        return update
        .attr("transform", (d: any, i: any) => {
          return "translate(" + scaleX(d.position) + "," + scaleY(d.prep) + ")";
        })
        .attr("fill", (d: any) => {
          return $this.calculateColor(d)
        })
      },
      function (exit: any) {
        return exit.remove()
      }
    )
    var brush: any= d3.brushX()
    .extent([[0, 0], [this.width, contextheight]])
    .on("end", brushended)
    // .on("brush", brushed);
    function brushended(event: any) {
      if (event && !event.selection) {
        $this.DataHandler.updatePositions(d3.extent($this.DataHandler.cells_full, (d:any)=>{return d.position}))
        $this.DataHandler.updateCells()
        $this.updateHeatmap()
      } else {
        brushed(event)
      }
    }
    this.context.append("g")
      .attr("class", "x brush")
      .call(brush)
      .selectAll("rect")
      .attr("y", -6)
      .attr("height", contextheight + 7);
    function brushed({selection}:any) {
      if (selection){
        let ranges: any = selection.map(scaleX.invert, scaleX).map((d:any) => { return Math.round(d) })
        $this.DataHandler.updatePositions(ranges)
        $this.DataHandler.updateCells()
      }
      $this.updateHeatmap()
    }

    this.updateHeatmap()
  }

  // Heatmap update, should be called when user changes the heatmap settings
  updateHeatmap() {

    console.log("updating heatmap")
    let scrollAttr: any  = { x: null, y: null, marginA: null, marginB: null }    
    let protein = this.DataHandler.protein
    let organism = this.DataHandler.organism
    const $this = this
    let cells: any = this.DataHandler.cells
    this.position_ranges = this.DataHandler.position_ranges
    this.positions_unique = this.DataHandler.protein_map[organism][protein].split("")
 
    // Set x axis positions to discordants only if ui box is checked
    if (!this.DataHandler.discordantOnly){
      this.positions = d3.range(1, this.positions_unique.length)
    } else {
      const positions: any[] = [...new Set(cells.map((d:any)=>{
          return d.position 
      }))];
      this.positions = positions
    }

    // Set x axis positions to a range if ui slider is set
    const positions_range = d3.extent(this.positions)
    cells = cells.filter((d:any)=>{ return +d.position >= positions_range[0] && +d.position <= positions_range[1]  })
    let reference_seq = this.DataHandler.referenceSequence
    const min = Math.max(this.DataHandler.position_ranges[0], d3.min($this.positions))
    const max = Math.min(this.position_max, d3.max($this.positions))
    this.positions = this.positions.filter((d:any)=>{ return d <= max && d >= min}).sort(function(a, b) {
      return a - b;
    });
    if (this.scrollDirection == 'x'){
      scrollAttr['x'] = this.positions
      scrollAttr.xTicks = this.positions_unique;
      scrollAttr['y'] = this.preps
      scrollAttr.marginA = this.margin.left
      scrollAttr.marginB = this.margin.right
      scrollAttr.long =  this.width     
    } else {
      scrollAttr['x'] = this.preps
      scrollAttr['y'] = this.positions
      scrollAttr.long =  this.height
      scrollAttr.xTicks = this.preps
      scrollAttr.marginA = this.margin.top
      scrollAttr.marginB = this.margin.bottom
    }
    let seen_positions: any = {}
    cells.forEach((cell:any, i:number)=>{
      if (!this.isSwitched){
        seen_positions[cell.position] = `${cell.consensus_aa}.${cell.position}`
      } else {
        if (reference_seq){
          cell.pdb_aa =`${reference_seq[cell.position]}`
        } else {
          seen_positions[cell.position] = `Unmapped.${cell.position}`
          cell.pdb_aa =`Unmapped`
        }
      }
    })
    if (reference_seq) {
      Object.keys(reference_seq).forEach((index: any) => {
        seen_positions[index] = `${reference_seq[index]}.${index}`
      })
    }
    
    // Set height of cells
    let boxHeight = (this.height - this.margin.top - this.margin.bottom )/ scrollAttr.y.length 
    // Set width of heatmap
    this.x.domain([min, max])
    .range([scrollAttr.marginA, ( scrollAttr.long ) * this.column_width - scrollAttr.marginB])
    const minD = this.x(min);
    const maxD = this.x(max);
    let over = this.width
    if (this.positions.length  > 20){
      over = maxD - minD + scrollAttr.marginA + scrollAttr.marginB;
    }
    this.oversize = over

    // Set width of cells
    const boxWidth = 
      (over - scrollAttr.marginA - scrollAttr.marginB) / (  this.positions.length > 0 ? scrollAttr[this.scrollDirection].length : 1) -
      this.border;
    this.boxWidth = boxWidth;

    // Set distance between x axis labels
    this.scaleX
      .domain(this.positions)
      .range([scrollAttr.marginA, over - scrollAttr.marginB]);

    // Sort y axis labels by date if not flipped or name if flipped
    if (! this.sortBy){
      try {
        scrollAttr.y = scrollAttr.y.sort((a: any, b:any) => {
          let datea = a.split("-")
          let dateb = b.split("-")
          return datea[datea.length -1].localeCompare(dateb[dateb.length -1])
        })
      } catch(err){
        console.log(err)
        scrollAttr.y = scrollAttr.y.sort()
      }
    } else {
      scrollAttr.y = scrollAttr.y.sort()
    }

    // Set distance between y axis labels
    this.scaleY.domain(scrollAttr.y).range(
      scrollAttr['y'].map((d: any, i: number) => {
        const spacing = this.boxHeight / 2;
        return (i * this.boxHeight ) + this.margin.top;
      })
    );
    this.yAxis = d3.axisLeft(this.scaleY)
          .ticks(scrollAttr.y.length+1);

    // Set top x axis labels
    this.xAxisT = d3
      .axisTop(this.scaleX)
      .tickSizeOuter(0)
      .ticks(max-min)
      .tickFormat((interval:any,i:any) => {
        return i%2 !== 0 ? " ": seen_positions[interval];
      });

    // Set bottom x axis labels
    this.xAxisB = d3
    .axisBottom(this.scaleX)
    .tickSizeOuter(0)
    .ticks(max-min)
    .tickFormat((interval:any,i:any) => {
      return i%2 !== 1 ? " ": seen_positions[interval];
    });

    // Add styling to y axis
    let scaleYText: any = d3.select("#yAxis")
          .attr("transform", "translate(" + this.labelPaddingLeft + "," + (this.boxHeight/2)+ ")")
          .style("stroke-width", 0)
          .call(this.yAxis)
          .call(g => g.select(".domain").remove())
          .selectAll('text')
          .classed("scaleYText", true)
          .style('text-anchor', 'start')
          .attr('transform', 'rotate(0)')
          .style("font-size", "14px")
    
    // Add styling to top x axis
    let scaleXTestT: any = d3.select('#xAxisT')
          .attr("transform", "translate(" + (0) + "," + (this.margin.top) + ")")
          .style("fill", null)
          .style("stroke-width", 0.2)
          .call(this.xAxisT)
          .selectAll('text')
          .attr("y", -9)
          .attr("x", 0)
          .attr("dy", ".35em")
          .attr("transform", "rotate(45)")
          .style("text-anchor", "end")
          .style("font-size", "14px");
    
    // Add styling to bottom x axis
    let scaleXTestB: any = d3.select('#xAxisB')
          .attr("transform", "translate(" + (0) + "," + (this.chartHeight - this.margin.bottom) + ")")
          .style("fill", null)
          .style("stroke-width", 0.2)
          .call(this.xAxisB)
          .selectAll('text')
          .classed("scaleXText", true)
          // .attr("y", 0)
          // .attr("x", 9)
          // .attr("dy", ".35em")
          .attr("transform", "rotate(45)")
          .style("text-anchor", "start")
          .style("font-size", "16px");
    
    // Set x and y axis font size
    try {
      let maxYTick: any = d3.max(scaleXTestB.nodes().map((d:any)=>{
          return d.getBBox().height
        })
      )
      let scaleyMax: any = d3.max(scaleYText.nodes().map((d:any)=>{
          return d.getBBox().height
      }))
      scaleYText.style("font-size", Math.min(scaleyMax, boxHeight))
      let maxXTick: any = d3.max(scaleXTestB.nodes().map((d:any)=>{
        
          return d.getBBox().width
        })
      )
      if (maxXTick > boxWidth){
        scaleXTestB.style("font-size", Math.min(14, maxXTick, boxWidth))
        scaleXTestT.style("font-size", Math.min(14, maxXTick, boxWidth))
      }  
      
    } catch(err: any){
      console.error(err)
    }

    // Set container of y axis to be width of svg
    const scaleYTextWidth = scaleYText.node().getBBox().width + this.labelPaddingLeft
    d3.select("#labelsSVG").attr("viewBox", `0 0 ${scaleYTextWidth} ${this.chartHeight}`)
    
    d3.select('#innerheatmapSVG')
    .attr("width", over)
    .style("fill", "white")

    // Cell styling + event handlers
    this.g.selectAll(".block")
    .data(cells, (d:any, i:any)=>{
        "_"+d.experiment.replaceAll(" ", "_").replaceAll("-", "_") + d.position +d.prep_id+ $this.DataHandler.protein + d.pdb_aa
    })
    .join(
      function (enter: any) {
            return enter
              .append("rect")
              .attr("id", (d: any) => {
                return (
                  "_"+d.experiment.replaceAll(" ", "_").replaceAll("-", "_") + d.position
                );
              })
              .attr("fill", (d: any) => {
                return $this.calculateColor(d)
              })
              .attr("transform", (d: any) => {
                let x: any; let y: any;
                if ($this.scrollDirection == 'x'){
                  y = $this.scaleY(d.experiment);
                  x = $this.scaleX(d.position);
                } else {
                  x = $this.scaleY(d.experiment);
                  y = $this.scaleX(d.position);
                }
                return "translate(" + x + "," + y + ")";
              })
              .attr("class", "block")
              .style("cursor", "pointer")
              .attr("width", $this.boxWidth )
              .attr("height", $this.boxHeight)
              .on("click", (d:any, u:any)=>{
                $this.DataHandler.selectedPosition = u.position
                $this.$emit("changePosition", u.position)
              })
              .on("mousemove", (event: any, u: any, n:any, i:number) => {
                $this.highlightCell(event, u)
              })
              .on("mouseleave", (d: any, u: any) => {
                $this.unHighlight(event, u)
              });
          },
          function (update: any) {
            return update
            .call((update: any) => {
              update.transition().duration(1000).attr("fill", (d: any) => {
              return $this.calculateColor(d)
              })
            })
            .attr("transform", (d: any) => {
              let x: any; let y: any
              if ($this.scrollDirection == 'x') {
                y = $this.scaleY(d.experiment);
                x = $this.scaleX(d.position);
              } else {
                x = $this.scaleY(d.experiment);
                y = $this.scaleX(d.position);
              }
              return "translate(" + x + "," + y + ")";
            })
            .attr("width", $this.boxWidth )
          },
          function (exit: any) {
            return exit.remove()
          }
        )}

  // Called when user mouses over a heatmap cell
  highlightCell(event: any, u: any){
    const $this = this
    d3.select(
      "#" +
        "_"+u.experiment.replaceAll(" ", "_").replaceAll("-", "_") + u.position 
    )
    .style("fill", "yellow");
    const ratio: number = 1- ( u.aa_count / u.depth)
    $this.focusColumn(u.position, false)

    d3.select("#tooltipHeatmap")
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
          return (d3.pointer(event, $this.svg.node() )[1] -h / 2  ) + "px"
        }
      )
      .style("opacity", "1").select("#tooltipcontent")
      .html(`Pos: ${u.position}<br>
      Experiment: ${u.experiment}<br>
      Depth: ${u.depth}<br>
      Total: ${u.total}<br>
      Reference Residue: ${u.aa}<br>
      Protein: ${u.protein}<br>
      PDB Residue: ${u.pdb_aa}<br>
      Consensus Residue: ${u.consensus_aa}<br>
      Consensus / Total: ${ratio.toFixed(3)} ${( !$this.isSwitched ? `<br>Ref. Residue: ${$this.positions_unique[$this.positions.indexOf(u.position)]}`: '')} `)
      $this.tooltiptable = u.unique.map((d:any)=>{
        if (d.aa == u.aa){
          d._rowVariant = 'info'
        } else if (u.aa !== d.aa && d.aa == u.consensus_aa){
          d._rowVariant = 'danger'
        }
        return d
      })
  }

  // Called when user's mouse leaves a heatmap cell
  unHighlight(event: any, u: any){
    const $this = this
    d3.select(
      "#" +
        
        "_"+u.experiment.replaceAll(" ", "_").replaceAll("-", "_") + u.position
    )
    .style("fill", (d: any) => {
      return $this.calculateColor(d)
    });
    this.unfocusColumn(u.position)
    d3.select("#tooltipHeatmap").style("opacity", "0");
  }

  // Called when user's mouse enters a heatmap column
  focusColumn(position: any, focus: boolean){
    let scaleXpost: any = this.scaleX(position)
    let listScales: any[] = [scaleXpost, scaleXpost + this.boxWidth] 
    d3.selectAll(".focus").remove()
    let minMax: any[] = d3.extent(this.scaleY.range())
    this.g.selectAll(".focus").data(listScales).enter().append("line")
    .attr("x1", (d:any)=>{return d})
    .attr("x2",(d:any)=>{return d})
    .attr("y1", minMax[0] )
    .style("stroke", "black")
    .style("stroke-width", 0.5)
    .attr("y2", this.boxHeight + minMax[1] )
    .attr("class", "focus")
    if (focus){
      let obj: any = document.querySelector("#overflowDiv")
      if (obj){
        let post: any = this.scaleX(position.toString())
        obj.scrollLeft = post - this.width/2
      }
    }
  }

  // Called when user's mouse leaves a heatmap column
  unfocusColumn(position:number){
    d3.selectAll(".focus").remove()
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

  // Helper function for calculateColor
  getFrac(d:any){
    const log_scale = 4
    // const max = d.max
    const max =  d.max
    if (d.total !== max){
      return(log_scale+Math.log10(1-max/d.total))/log_scale;
    } else {
      return 0.9999999
    }
  }

  // pretty close to exactly Tom's color code
  calculateColor(d: any) {

   	const depth_thresh = this.DataHandler.depth_threshold
    const freq_thresh = this.DataHandler.frequency_threshold
    const max = d.aa_count
    let color = '';
    let colors: string[] = [
      'rgb(' + Math.round(245) + ',' + Math.round(242) + ',' + Math.round(242) + ')',
      'rgb(' + Math.round(185) + ',' + Math.round(185) + ',' + Math.round(185) + ')',
      'rgb(' + Math.round(235) + ',' + Math.round(235) + ',' + Math.round(235) + ')',
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

    } else if ( (max != d.total && d.total < depth_thresh && (1-max/d.total) >= freq_thresh ) || max == d.total && d.total < depth_thresh ) {
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
