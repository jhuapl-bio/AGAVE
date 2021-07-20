<template>
  <div class="">
    <h2>Positions</h2>
    <div id="barPlotDiv"  ref="barPlotDiv"></div>
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
  chartHeight = 300;
  width = 0
  public margin = {
    top: 0.13 * this.chartHeight,
    bottom: 0.095 * this.chartHeight,
    left: 0.2 * this.width,
    right: 0.05 * this.width,
  };


  makeBarPlot(){
    console.log("make bar plot", this.width)
    this.svg = d3.select("#barPlotDiv").append("svg")
    .attr("id", "barPlotSVG")
    .attr("ref", "barPlotSVG")
    .style("position", "absolute")
    .style("pointer-events", "none")
    .style("z-index", 1)
    .attr("viewBox", `0 0 ${this.width} ${this.chartHeight}`)

    this.svg.append("g").attr("id", "barPlotG")
    .data(this.DataHandler)

  }

  mounted(){
    this.width = this.$refs.barPlotDiv.clientWidth;
    this.makeBarPlot()
  }

}

</script>
