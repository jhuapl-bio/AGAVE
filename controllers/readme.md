# Creating subjects.csv file for grouping samples to groups and preps

echo "prep_id,group,sample_name" > ivar_variants_groups.csv &&  while read line; do base=$(basename -- $line); echo -e "1,CEIR1,${base%%.*}"; done <<< $(ls ivar_variants/*tsv) >> ivar_variants_groups.csv


# Running pipelne to get json


### SINGLE FILE Use Variant or consensus called depth at positions from vcf file(s), use tsv

python3 vcfs_to_json.py \
    -i data/ivar_variants/02-11-Pro-1122.variants.tsv \
    -o out.json \
    --filetype tsv \
    -cad ALT_DP \
    -crd REF_DP \
    -ct TOTAL_DP \
    --gb proteins/nCoV2.gb \
    --get_gb \
    --email "$yourEmail" \
    -map_sample data/ivar_variants_groups.csv \
    --depth data/samtools_depth_trimmed/02-11-Pro-1122.depth.txt \
    --depth_type "variant"

### Multiple SAMPLES/FILES Use Variant or consensus called depth at positions from vcf file(s), use tsv

python3 vcfs_to_json.py \
    -i data/ivar_variants/ \
    -o out.json \
    --filetype tsv \
    -cad ALT_DP \
    -crd REF_DP \
    -ct TOTAL_DP \
    --gb proteins/nCoV2.gb \
    --get_gb \
    --dir \
    --email "$yourEmail" \
    -map_sample data/ivar_variants_groups.csv \
    --depth data/samtools_depth_trimmed/ \
    --dir_depth \
    --depth_type "variant"


### Multiple SAMPLES/FILES Use Base Depth for all positions, use tsv

python3 vcfs_to_json.py \
    -i data/ivar_variants/ \
    -o out.json \
    --filetype tsv \
    -cad ALT_DP \
    -crd REF_DP \
    -ct TOTAL_DP \
    --gb proteins/nCoV2.gb \
    --get_gb \
    --dir \
    --email "$yourEmail" \
    -map_sample data/ivar_variants_groups.csv \
    --depth data/samtools_depth_trimmed/ \
    --dir_depth \
    --depth_type "full" -map_pdb data/mapped_pdb.tsv



### SINGLE FILE Use Base Depth rather than variant or consensus called depth at positions, use tsv

python3 vcfs_to_json.py \
    -i data/ivar_variants/02-11-Pro-1122.variants.tsv \
    -o out.json \
    --filetype tsv \
    -cad ALT_DP \
    -crd REF_DP \
    --gb proteins/nCoV2.gb \
    --get_gb \
    --email "$yourEmail" \
    -map_sample data/ivar_variants_groups.csv \
    --depth data/samtools_depth_trimmed/02-11-Pro-1122.depth.txt \
    --depth_type "full" -map_pdb data/mapped_pdb.tsv

### SINGLE FILE User depth defined in variant call file or consensus output, use vcf files

python3 vcfs_to_json.py -i data/ivar_variants/02-11-Pro-1122.ivar_variants.vcf -o out.json --filetype vcf --get_gb --email brian.merritt@jhuapl.edu -map_sample data/ivar_variants_groups.csv --depth data/samtools_depth_trimmed/02-11-Pro-1122.depth.txt --depth_type variant  --gb proteins/nCoV2.gb -map_pdb data/mapped_pdb.tsv


### SINGLE FILE Use Base Depth rather than variant or consensus called depth at positions, use vcf files

python3 vcfs_to_json.py \
    -i data/subset_ivar_variants/02-11-Pro-1122.ivar_variants.vcf -o out.json --filetype vcf -c ALT_DP  --get_gb --email brian.merritt@jhuapl.edu -map_sample data/ivar_variants_groups.csv --depth data/samtools_depth_trimmed/02-11-Pro-1122.depth.txt --depth_type full --gb proteins/nCoV2.gb -map_pdb data/mapped_pdb.tsv



### SINGLE FILE, MISSING GB FILES Use Base Depth rather than variant or consensus called depth at positions, use vcf files

python3 vcfs_to_json.py \
    -i data/subset_ivar_variants/02-11-Pro-1122.ivar_variants.vcf -o out.json --filetype vcf -cad ALT_DP \
    -crd REF_DP \ --get_gb --email brian.merritt@jhuapl.edu -map_sample data/ivar_variants_groups.csv --depth data/samtools_depth_trimmed/02-11-Pro-1122.depth.txt --depth_type full -map_pdb data/mapped_pdb.tsv



### Convert old json format to newer on (IVA specificially )

python3 vcfs_to_json.py \
    -i data/old_jsons/New/HA.json \
    -o out.json \
    --filetype json --depth_type "variant" \
    --gb proteins/iva_HA_h1n1.gb proteins/iva_m1_m2_h1n1.gb proteins/iva_NA_h1n1.gb proteins/iva_np_h1n1.gb proteins/iva_NS1_NEP_h1n1.gb proteins/iva_pa_h1n1.gb proteins/iva_pb1_h1n1.gb proteins/iva_pb2_h1n1.gb \
    -map_old_organism data/mapped_organism_sample.tsv -map_pdb data/mapped_pdb.tsv



### Merge Files (one or more out.jsons)

python3 vcfs_to_json.py -i BARDA_HA.json out.json -o out.merged.json --merge