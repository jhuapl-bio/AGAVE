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
import { Component, Vue } from 'vue-property-decorator'
import LocalDataHelper from '@/shared/LocalDataHelper'
import * as d3 from 'd3'
// import { local } from 'd3';
// import fs from 'file-system'

@Component({})
export default class Heatmap extends Vue {

  private localDataHelper = new LocalDataHelper();

  $refs!: {
    heatmapDiv:HTMLElement
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
  scaleXInner = { }
  scaleXGroup = d3.scaleBand()
  xAxisInner = { }
  xAxisGroup = { }
  divisionYScale = { }
  yAxisDivision = {}
  scaleY = d3.scaleOrdinal()
  yAxis = { }
  containerHeight = 500
  chartHeight = (this.containerHeight * 0.55)
  margin = {
    top: 0.1 * this.chartHeight,
    bottom: 0.25 * this.chartHeight,
    left: 0.15 * this.width,
    right: 0.2 * this.width
  }

  // need annotation due to `this` in return type
  greet(): string {
    return this.msg + ' world'
  }
  mounted() {
    this.makeHeatmap()
  }

  makeHeatmap() {
    // const $this = this
    this.height = Math.min(this.chartHeight)
    console.log(this.$refs.heatmapDiv, '_________________________')
    this.width = this.$refs.heatmapDiv.clientWidth
    console.log(this.width)
    const border = this.border
    const margin = this.margin

    const segments = ['HA', 'M1', 'NA', 'NP', 'NS1', 'PA', 'PB1', 'PB2']
    const boxSpacingX = (this.width - margin.left - margin.right) / segments.length
    // const boxSpacingY = (this.height - margin.bottom - margin.top) / this.classifiers.length
    const boxSpacingY = 20
    const boxWidth = ((this.width - margin.left - margin.right) / segments.length) - border
    this.boxWidth = boxWidth
    // const bottomPosition = Math.min((this.height - margin.top-margin.bottom), this.classifiers.length * 70)
    // const boxHeight = (((this.height - margin.top - margin.bottom) / this.classifiers.length) - border)
    const boxHeight = 20
    const yAxisVariables = ['a', 'b', 'c']
    this.boxHeight = boxHeight
    this.scaleY.domain(yAxisVariables)
      .range(yAxisVariables.map((d, i) => {
        const spacing = boxHeight / 2
        return (i * boxHeight) + spacing + margin.top
      }))

    this.scaleXGroup.domain(['a', 'b'])
      .range([this.margin.left, this.width - this.margin.right])
    const divisionYScale = d3.scaleBand<string>()
      .domain(['a', 'b'])
      .range([this.margin.left, this.width - this.margin.right])
    // const yAxisDivision = d3.axisLeft<string>().scale(divisionYScale).tickSizeOuter(0)
    //   .ticks(0);
    // this.yAxisDivision[element] = { L2: null, AUPRC: null }
    this.updateHeatmap()
  }
  updateHeatmap() {
    console.log('Updating Heatmap now...')
    console.log("Reading in data files of example data...")
    // const exts = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'T', 'V', 'X', 'Y']
    const exts = ['A']
    // const promises: any[] = []
    const data: Object[] = []
    exts.forEach((d) => {
      // promises.push(d3.tsv(`/assets/data/Gaydos/grouped/${d}.subset.txt`))
      data.push(this.localDataHelper.readTSV('Gaydos/grouped/HA/C.subset.txt'))
    })
    // Promise.all(promises).then((data) => {
    //   console.log('Done fetching promises')
    //   console.log(data, 'ssss')
    // }).catch((err) => {
    //   console.error(err, 'error in fetching text files')
    // })
    console.log(data, 'ssss')
    console.log(process.env.BASE_URL)
  }
}
</script>
<style>

</style>
