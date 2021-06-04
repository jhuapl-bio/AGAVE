
export default class Parsing {

  public totalwt2frac(value: any, frequency_threshold: number, depth_threshold: number)
  {
    //--------------------------------------------------------------------------------------------------
      let max: number = -1;
      let log_scale: number = 10
      max = Math.max(value);
      var frac = 0;
      // if ( d.total === 0 ) {
      //   frac = -100;
      // } else if ( d.total < depth_threshold && (1-max/d.total) < freq_thresh) {
      //   frac = -200;
      // } else if ( max == d.total && d.total >= depth_threshold ) {
      //   frac = -300;
      // } else if ( max != d.total && d.total < depth_threshold && (1-max/d.total) >= frequency_threshold ) {
      //   frac = -400;
      // } else {
      //   frac = (log_scale+Math.log10(1-max/d.total))/log_scale;
      // }
      return frac;
  }
  
} 