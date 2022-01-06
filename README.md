# barda

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).



## Controllers 

### Running pipelne to get json


#### SINGLE FILE Use Variant or consensus called depth at positions from vcf file(s), use tsv

python3 controllers/src/vcfs_to_json.py \
    -i $tsv_containig_variant_from_ivar \
    -o output/out.json \
    --filetype tsv \
    -cad ALT_DP \
    -crd REF_DP \
    -ct TOTAL_DP \
    --gb data/proteins/nCoV2.gb \
    --get_gb \
    --email "$yourEmail" \
    --depth $depthFile \
    --depth_type "variant"

#### Multiple SAMPLES/FILES Use Variant or consensus called depth at positions from vcf file(s), use tsv

python3 controllers/src/vcfs_to_json.py \
    -i $ivar_dir \
    -o output/out.json \
    --filetype tsv \
    -cad ALT_DP \
    -crd REF_DP \
    -ct TOTAL_DP \
    --gb data/proteins/nCoV2.gb \
    --get_gb \
    --dir \
    --email "$yourEmail" \
    --depth $depth_dir \
    --dir_depth \
    --depth_type "variant"


#### Multiple SAMPLES/FILES Use Base Depth for all positions, use tsv

python3 controllers/src/vcfs_to_json.py \
    -i $ivar_variants_dir \
    -o output/out.json \
    --filetype tsv \
    -cad ALT_DP \
    -crd REF_DP \
    -ct TOTAL_DP \
    --gb data/proteins/nCoV2.gb \
    --get_gb \
    --dir \
    --email "$yourEmail" \
    --depth $depth_dir \
    --dir_depth \
    --depth_type "full" \
    -map_pdb data/mappings//mapped_pdb.tsv



#### SINGLE FILE Use Base Depth rather than variant or consensus called depth at positions, use tsv

python3 controllers/src/vcfs_to_json.py \
    -i $tsv_from_ivar \
    -o output/out.json \
    --filetype tsv \
    -cad ALT_DP \
    -crd REF_DP \
    --gb data/proteins/nCoV2.gb \
    --get_gb \
    --email "$yourEmail" \
    --depth $depthFile \
    --depth_type "full" -map_pdb data/mappings//mapped_pdb.tsv

#### SINGLE FILE User depth defined in variant call file or consensus output, use vcf files

python3 controllers/src/vcfs_to_json.py \
    -i $vcf \
    -o output/out.json \
    --filetype vcf \
    --get_gb \
    --email $email \
    --depth $depthFile \
    --depth_type variant \
    --gb data/proteins/nCoV2.gb \
    -map_pdb data/mappings//mapped_pdb.tsv


#### SINGLE FILE Use Base Depth rather than variant or consensus called depth at positions, use vcf files

python3 controllers/src/vcfs_to_json.py \
    -i $vcf \
    -o output/out.json \
    --filetype vcf \
    -c ALT_DP  \
    --get_gb \
    --email $email \
    --depth $depthFile \
    --depth_type full \
    --gb data/proteins/nCoV2.gb \
    -map_pdb data/mappings//mapped_pdb.tsv



#### SINGLE FILE, MISSING GB FILES Use Base Depth rather than variant or consensus called depth at positions, use vcf files

python3 controllers/src/vcfs_to_json.py \
    -i $vcf \
    -o output/out.json \
    --filetype vcf \
    -cad ALT_DP \
    -crd REF_DP \ --get_gb \
    --email $email \
    --depth $depthTxtFile \
    --depth_type full \
    -map_pdb data/mappings//mapped_pdb.tsv



#### Convert old json format to newer on (IVA specificially )

python3 controllers/src/vcfs_to_json.py \
    -i $json1 \
    -o output/out.json \
    --filetype json --depth_type "variant" \
    --gb data/proteins/iva_HA_h1n1.gb data/proteins/iva_m1_m2_h1n1.gb data/proteins/iva_NA_h1n1.gb data/proteins/iva_np_h1n1.gb data/proteins/iva_NS1_NEP_h1n1.gb data/proteins/iva_pa_h1n1.gb data/proteins/iva_pb1_h1n1.gb data/proteins/iva_pb2_h1n1.gb \
    -map_pdb data/mappings//mapped_pdb.tsv



#### Merge Files (one or more output/out.jsons)

python3 controllers/src/vcfs_to_json.py -i $json1 $json2  -o out.merged.json --merge