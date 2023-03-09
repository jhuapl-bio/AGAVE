declare module '*.vue' {
  import Vue from 'vue'
  // import * as d3 from 'd3'
  // import * as fs from 'file-system'
  export default Vue
}

declare module 'file-system';
declare module '@/assets/data/*.csv';
declare module '@/assets/data/*.tsv';
declare module '@/assets/data/*.txt';
declare module 'molstar/build/viewer/molstar.js'