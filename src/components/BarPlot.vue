<template>
  <b-row class="">
    <b-col class="col-lg-10 pb-1">
      <div id="barPlotDiv" :style="{height: containerHeight+'px'}" ref="barPlotDiv"></div>
      <div id="barPlotLegend" style="padding-top: 10px"  ref="barPlotLegend"></div>    
    </b-col>
    <b-col class="col-lg-2 pb-1">
      <b-field label="Scale" class="">
        <b-select
        :options="scales"
        v-model="selected_scale"
        @change="makeBarPlot()"
        >
        </b-select>
        
      </b-field>
      <b-field>
        <b-button @click="downloadSVG()">Save SVG</b-button>
      </b-field>
    </b-col>
  </b-row>
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
    this.localPosition = value
    this.makeBarPlot()
  }
  changeDataHandler(){
    this.makeBarPlot()
  }
  $refs!: {
    barPlotDiv: HTMLElement;
  };

  public svg: any = null
  containerHeight = 300;
  chartHeight = this.containerHeight
  width = 0
  localPosition = 158
  margin: any = {
    top: 0.045 * this.chartHeight,
    bottom: 0.15 * this.chartHeight,
    left: 0.05 * this.width,
    right: 0.0001 * this.width,
  };
  oversize: any  = 0
  public scales = ['Linear', 'Sqrt', 'Log']
  public selected_scale = this.scales[0]
  downloadSVG(evt:any) {
    var svg:any = document.querySelector("#barPlotSVG");
    var svg_xml = (new XMLSerializer()).serializeToString(svg),
    blob = new Blob([svg_xml], {type:'image/svg+xml;charset=utf-8'}),
    url = window.URL.createObjectURL(blob);
    var img = new Image();
    const w = this.width
    const h = this.containerHeight
    img.width = this.width
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
      ctx.fillText($this.DataHandler.segment, w / 2 , $this.margin.top / 2)
      window.URL.revokeObjectURL(url);
      var canvasdata = canvas.toDataURL('image/jpeg');
      var a: any = document.getElementById('imgId');
      a.download = "export_" + Date.now() + ".jpeg";
      a.href=canvasdata;
      a.click()  
    }
    img.src = url
    
  }

  makeBarPlot(){
    console.log("make bar plot")
    const $this = this
    d3.select("#barPlotDiv").selectAll("*").remove()
    d3.select('#barPlotLegend').selectAll("*").remove()
    
    const barplotDiv = d3.select("#barPlotDiv")
    
    this.svg = barplotDiv.append("svg")
    .attr("id", "barPlotSVG")
    .attr("ref", "barPlotSVG")
    .attr("width", this.width)
      .attr("height", this.containerHeight)
      .style("position", "absolute")
      .style("pointer-events", "none")
      .style("z-index", 1)
    // .attr("viewBox", `0 0 ${this.width } ${this.containerHeight}`)

    const body = barplotDiv.append("div")
      .attr("id","overflowDivBarPlot")
      .style("overflow-x", "scroll")
      // .style("height", this.containerHeight  )
      // .style("width", this.width / 6)
      

    const innerSvg = body.append("svg")
      .attr("id", "innerheatmapSVGBarPlot")
      .style("display", "block")
      .attr("width", this.width)
      .attr("height", this.containerHeight)

      
    let svgG: any = innerSvg.append("g").attr("id", "svgG")
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
    
    
    let chartWidth = this.width - this.margin.right
    let boxDim: any = chartWidth / preps.length
    this.chartHeight = this.containerHeight - this.margin.top - this.margin.bottom
    console.log("height", this.chartHeight, this.containerHeight)
    let scaleX: any = d3.scaleBand().domain(preps)
    .range([this.margin.left, chartWidth ])
    
    let scaleY: any = null
    if (this.selected_scale == 'Linear'){
      scaleY = d3.scaleLinear().domain([0, 1])
      .range([this.margin.top, this.chartHeight ])
    } else if (this.selected_scale == 'Sqrt' ){
      scaleY = d3.scaleSqrt().domain([0, 1])
      .range([this.margin.top, this.chartHeight ])
    }
    else {
      scaleY = d3.scaleLog().clamp(true).domain([0, 1])
      .range([this.margin.top, this.chartHeight ])
    }
      
    let scaleColor: any = d3.scaleOrdinal().domain(colors).range(colors);
    
    let xAxisB: any = d3
      .axisBottom(scaleX)
      .ticks(5)
      .tickSizeOuter(0)
      .tickSize(0)
    let xAxis: any = svgG.append("g")
    .attr("class", "xAxis")
    .attr("id", "xAxisTBar")
    .attr("transform", "translate(" + (0) + "," + (this.chartHeight + this.margin.top )  + ")")
    .style("fill", null)
    .style("stroke-width", 0.2)
    .call(xAxisB)
    xAxis.selectAll('text')
    .style('text-anchor', 'start')
    .attr('transform', 'rotate(45)').style("font-size", "1em")

    let yAxisB: any = d3
      .axisLeft(scaleY)
      .ticks(5)
      .tickSizeOuter(0)
      .tickSize(0)


    let yAxis: any = svgG.append("g")
    .attr("class", "yAxis")
    .attr("id", "yAxisTBar")
    .attr("transform", "translate(" + (this.margin.left ) + "," + (boxDim / 8) + ")")
    .style("fill", null)
    .style("stroke-width", 0.2)
    .call(yAxisB)

    let stacks: any = d3.stack().keys(aas)
    (data)
    .map((d:any)=>{
      d.forEach((v:any)=>{
        v.key = d.key
      })
      return d
    })
    svgG
    .attr("id", "barPlotG")
    .selectAll(".barG")
    .data(stacks).enter()
    .append("g")
    .classed("barG", true)
    .selectAll(".posBar")
    .data((d:any)=>{return d})
    .join(
      function (enter: any) {
        return enter
        .append("rect")
		    .classed('posBar', true)
        .attr("transform", (d: any, i: any) => {
          return "translate(" + scaleX(d.data.prep) + "," +  ( scaleY(d[0])  ) + ")";
        })
        .style("cursor", "pointer")
        .attr("width",  boxDim )
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


    // let legendHeight: number = $this.chartHeight   * 0.5
    // let legendWidth: number = this.width
    
    // let legendMargin: any = {
    //   top: legendHeight * 0.1,
    //   left: legendHeight * 0.1,
    //   right: legendHeight * 0.1,
    //   bottom: legendHeight * 0.2
    // }
    // legendHeight  = legendHeight - legendMargin.top - legendMargin.bottom
    // let legendBoxHeight: number = legendHeight  * 0.2
    // let legendBox: number = legendWidth  / aas.length

    // let g: any = d3.select("#barPlotLegend")
    // .append("svg")
    // .attr("id", "barPlotLegendSVG")
    // .attr("viewBox", `0 0 ${legendWidth} ${legendHeight}`)
    // .append("g")


    // scaleX = d3.scaleBand().domain(aas)
    // .range([0, legendWidth  ])
    
    // g.selectAll(".posBarLegRect")
    // .data(aas)
    // .enter()
    // .append("rect")
    // .attr("transform", (d:any) =>{
    //   return "translate(" + scaleX(d) + "," + (0) + ")"
    // })
    // .attr("height",  legendBoxHeight )
    // .attr("width", legendBox )
    // .style("fill", (d:any) => scaleColor(d))
    
    
    // let xAxisLegB: any = d3
    //   .axisBottom(scaleX)
    //   .ticks(20)
    //   .tickSizeOuter(0)
    //   .tickSize(0)
    // let xAxisLeg: any = g.append("g")
    // .attr("class", "xAxis")
    // .attr("id", "xAxisRBar")
    // .attr("transform", "translate(" + (0) + "," + (legendBoxHeight) + ")")
    // .style("fill", null)
    // .style("stroke-width", 0.2)
    // .call(xAxisLegB)
    // .call((g:any) => g.select(".domain").remove())
    // .selectAll('text')
    // .style('text-anchor', 'middle')
    // .attr('transform', 'rotate(0)').style("font-size", "1em")
    // try {
    //   let maxyTick: any = d3.max(yAxis.selectAll("g").nodes().map((d:any)=>{
    //       return d.getBBox().height
    //     })
    //   )      
    //   if (maxyTick > boxDim){
    //     yAxis.style("font-size", `${ boxDim / (maxyTick*5) }em`)
    //   }    
    //   maxyTick =  d3.max(xAxis.selectAll("g").nodes().map((d:any)=>{
    //       return d.getBBox().height
    //     })
    //   )
    //   if (maxyTick > this.margin.bottom){
    //     const l = this.margin.bottom
    //     xAxis.style("font-size", `${ (l) / (maxyTick*2) }em`)
    //   }   
    // } catch(err: any){
    //   console.error(err)
    // }


  }

  mounted(){
    this.width = this.$refs.barPlotDiv.clientWidth
    this.margin.right= 0.05 * this.width
    this.margin.left  = 0.1 * this.width
    this.width = this.width * 2
    this.localPosition = 158
    this.makeBarPlot()
  }

}

</script>
