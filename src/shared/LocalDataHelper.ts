import * as d3 from 'd3'

interface StringMap { [key: string]: string; }

export default class LocalDataHelper {

  public async readTSV(filepath: string)
  {

    // const data = require("/data/" + filepath)
    const data_tsv = await d3.tsv(`/data/${filepath}`)
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

    return data_tsv

  }
  public async readTSVNoHeader(filepath: string, header: string[])
  {
    // const data_tsv = await d3.tsv(`/data/${filepath}`)
    let text = await d3.text(`/data/${filepath}`)
    // text = header + "\n" + text
    var data = d3.tsvParseRows(text)
    var objects = data.map(function(values) {
      return header.reduce(function(o: StringMap, k: string, i: number) {
          o[k] = values[i];
          return o;
      }, {});
    });
    
    return objects
  }
} 