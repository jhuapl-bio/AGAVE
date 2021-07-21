<template>
  <div class="">
    <h2>Positions</h2>
    <div id="barPlotDiv" :style="{height: containerHeight+'px'}" ref="barPlotDiv"></div>
    <div id="barPlotLegend"  ref="barPlotLegend"></div>
  </div>
</template>

<script lang="ts">

import { Component, Vue, Prop, Watch } from 'vue-property-decorator'
import swal from 'vue-sweetalert2'
import * as d3 from "d3";

@Component({})
export default class BindingSites extends Vue {

  @Prop({ required: true })
  public DataHandler!: any;
  @Watch("DataHandler.selectedPosition", {deep:true})
  onDataHandlerChanged(value: any, oldValue: any) {
    console.log("value new datahandler", value)
  }
  $refs!: {
    barPlotDiv: HTMLElement;
  };

  public svg: any = null
  containerHeight = 800;
  chartHeight = this.containerHeight
  width = 0
  localPosition = 158
  margin = {
    top: 0.13 * this.chartHeight,
    bottom: 0.095 * this.chartHeight,
    left: 0.2 * this.width,
    right: 0.05 * this.width,
  };
  

  makeBarPlot(){
    console.log("make bar plot", this.width, this.DataHandler)
    const $this = this
    d3.select("#barPlotDiv").select("svg").remove()
    this.svg = d3.select("#barPlotDiv").append("svg")
    .attr("id", "barPlotSVG")
    .attr("ref", "barPlotSVG")
    .style("position", "absolute")
    .style("pointer-events", "none")
    .style("z-index", 1)
    .attr("viewBox", `0 0 ${this.width} ${this.containerHeight}`)
    let svgG:any = this.svg.append("g").attr("id", "svgG")
    let colors: string[] = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', 'red', '#000']
    let aas: string[]  = ["M", "K", "A", "I", "L", "V", "Y", "T", "F", "N", "D", "C", "G", "H", "S", "E", "P", "W", "R", "Q"]
    
    let preps: any = [...new Set(this.DataHandler.cells.map((d: any) => d.experiment))];
    // let aas: any = [...new Set(this.DataHandler.cells.map((d: any) => d.aa))];
    let data: any[] = d3.filter(this.DataHandler.cells, (d: any)=>{
      return d.position == $this.localPosition
    })
    .map((d:any)=>{
      let r: any = {prep: d.experiment}
      d.unique.map((f:any)=>{
        r[f.aa] = +f.proportion
      })
      aas.forEach((aa:any)=>{
        if (! (aa in r ) ){
          r[aa] = 0
        }
      })
      return r
    })
    let mapped_positions: any = {}

    preps.forEach((d:any)=>{
      mapped_positions[d] = 0
    })

    let scaleX: any = d3.scaleBand().domain(preps)
    .range([0, this.width])
    
    let scaleY: any = d3.scaleLinear().domain([0, 1])
    .range([0, this.chartHeight- this.margin.bottom])
    let scaleColor: any = d3.scaleOrdinal().domain(colors).range(colors);
    
    let xAxisB: any = d3
      .axisBottom(scaleX)
      .ticks(20)
      .tickSizeOuter(0)
      .tickSize(0)
    svgG.append("g")
    .attr("class", "xAxis")
    .attr("id", "xAxisTBar")
    .attr("transform", "translate(" + (0) + "," + (this.containerHeight - this.margin.bottom) + ")")
    .style("fill", null)
    .style("stroke-width", 0.2)
    .call(xAxisB)
    .selectAll('text')
    .style('text-anchor', 'start')
    .attr('transform', 'rotate(45)').style("font-size", "0.95em")
    let stacks: any = d3.stack().keys(aas)
    (data)
    .map((d:any)=>{
      d.forEach((v:any)=>{
        v.key = d.key
      })
      return d
    })
    svgG.append("g")
    .attr("id", "barPlotG")
    .selectAll("g")
    .data(stacks).enter()
    .selectAll(".posBar")
    .data((d:any)=>{return d})
    .join(
      function (enter: any) {
        return enter
        .append("rect")
		    .classed('posBar', true)
        .attr("transform", (d: any, i: any) => {
          return "translate(" + scaleX(d.data.prep) + "," +  ( scaleY(d[0]) ) + ")";
        })
        .style("cursor", "pointer")
        .attr("width", $this.width / preps.length )
        .style("stroke", "#fff")
        .attr("height",  (d:any, i:any)=>{          
          return scaleY(d[1]) - scaleY(d[0])
        })
        .style("fill", (d: any) => {
          return scaleColor(d.key)
        })
      },
      function (update: any){
        return update
      },
      function (exit: any) {
        return exit.remove()
      }
    )

    let legendHeight: number = 30
    let legendWidth: number = this.width
    let legendMargin: any = {
      top: legendHeight * 0.1,
      left: legendHeight * 0.1,
      right: legendHeight * 0.1,
      bottom: legendHeight * 0.1
    }
    let g: any = d3.select("#barPlotLegend")
    .append("svg")
    .attr("id", "barPlotLegendSVG")
    .attr("viewBox", `0 0 ${legendWidth} ${100}`)
    .append("g")
    scaleX = d3.scaleBand().domain(aas)
    .range([0, legendWidth])
    
    g.selectAll(".posBarLegRect")
    .data(aas)
    .enter()
    .append("rect")
    .attr("transform", (d:any) =>{
      return "translate(" + scaleX(d) + "," + (legendMargin.top) + ")"
    })
    .attr("height", legendHeight - legendMargin.top - legendMargin.bottom)
    .attr("width", legendWidth / aas.length )
    .style("fill", (d:any) => scaleColor(d))
    
    
    let xAxisT: any = d3
      .axisBottom(scaleX)
      .ticks(20)
      .tickSizeOuter(0)
      .tickSize(0)
    g.append("g")
    .attr("class", "xAxis")
    
    .attr("id", "xAxisTBar")
    .attr("transform", "translate(" + (0) + "," + (legendHeight - legendMargin.bottom) + ")")
    .style("fill", null)
    .style("stroke-width", 0.2)
    .call(xAxisT)
    .call((g:any) => g.select(".domain").remove())
    .selectAll('text')
    .style('text-anchor', 'middle')
    .attr('transform', 'rotate(0)').style("font-size", "1em")
    



  }

  mounted(){
    this.width = this.$refs.barPlotDiv.clientWidth;
    this.localPosition = 158
    this.makeBarPlot()
  }

}

</script>
