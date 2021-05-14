
export default class LocalDataHelper {

  public readTSV(filepath: string): Object {

    const data = require("../assets/data/" + filepath)

    // Tom's D3 code for parsing data before consuming it. This could be useful?

    //    	let temp = filepath.responseText;
    //     // slice off header before parsing file
    //     let ret: Object[] = [];
    //     d3.tsvParse(temp.split('\n').slice(1).join('\n')).map(function(row) {

    //         var obj: Object[] = [];
    //         // split off prep_ID column if it exists as column 1
    //         if(row[0].match(/[a-z]/i)){
    //             obj.id = row[0];
    //             obj.data = row.slice(1).map(function(value) {
    //                 return +value;
    //             });
    //         } else {
    //             obj.data = row.map(function(value) {
    //                 return +value;
    //             });
    //         }
    //         ret.push(obj);
    //     });

    //     return ret;

    return data;

  }
}
