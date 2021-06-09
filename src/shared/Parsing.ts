
export default class Parsing {

  public totalwt2frac(d: any, frequency_threshold: number, depth_threshold: number)
  {
    //--------------------------------------------------------------------------------------------------
      let max: number = -1;
      let log_scale: number = 10
      // console.log(d)
      max = d.max
      var frac = 0;
      if ( d.total === 0 ) {
        frac = -100;
      } else if ( d.total < depth_threshold && (1-max/d.total) < frequency_threshold) {
        frac = -200;
      } else if ( max == d.total && d.total >= depth_threshold ) {
        frac = -300;
      } else if ( max != d.total && d.total < depth_threshold && (1-max/d.total) >= frequency_threshold ) {
        frac = -400;
      } else {
        frac = (log_scale+Math.log10(1-max/d.total))/log_scale;
      }
      return frac;
  }
  public frac2rainbow(frac: number){
    var color = '';
    switch ( frac ) {
            case -100:
                    // there is no data at this point: total = 0
                    color = 'rgb(' + Math.round(235) + ',' + Math.round(235) + ',' + Math.round(235) + ')';
                    break;
            case -200:
                    // there is little data at this point: 0 < total < depth_thresh
                    color = 'rgb(' + Math.round(185) + ',' + Math.round(185) + ',' + Math.round(185) + ')';
                    break;
            case -300:
                    // there is enough data at this point, but zero mutations: total >= depth_thresh; wt = total
                    color = 'rgb(' + Math.round(165) + ',' + Math.round(165) + ',' + Math.round(165) + ')';
                    break;
            case -400:
                    // there is little data at this point, but a lot of mutations: total < depth_thresh; 1-wt/total > freq_thresh
                    color = 'rgb(' + Math.round(65) + ',' + Math.round(65) + ',' + Math.round(65) + ')';
                    break;
            default:
                    // there is data at this point, and at least one mutation: total > 0; wt != total
                    var x = 0.25 + 0.75*frac;
                    var r = 255 * (0.472 - 0.567*x + 4.05*Math.pow(x,2)) / (1 + 8.72*x - 19.17*Math.pow(x,2) + 14.1*Math.pow(x,3));
                    var g = 255 * (0.108932 - 1.22635*x + 27.284*Math.pow(x,2) - 98.577*Math.pow(x,3) + 163.3*Math.pow(x,4) - 131.395*Math.pow(x,5) + 40.634*Math.pow(x,6));
                    var b = 255 / (1.97 + 3.54*x - 68.5*Math.pow(x,2) + 243*Math.pow(x,3) - 297*Math.pow(x,4) + 125*Math.pow(x,5));
                    if( r < 0 || g < 0 || b < 0 ){
                            color = 'rgb(253,64,160)';
                    } else {
                            color = 'rgb(' + Math.round(r) + ',' + Math.round(g) + ',' + Math.round(b) + ')';
                    }
                    break;
    }
    return color;
}
  
} 