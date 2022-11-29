import argparse
import pandas as pd
import vcf
import numpy as np
# make sure you conda activate AGAVE before running this script. 
import json
import math
import pathlib
import os
from query_genbank import parse_gb, query_gb, query_uniprot_to_pdb, query_genbank_to_uniprot


pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
parser = argparse.ArgumentParser(description = "Generate json(s) for variant called data, requires AGAVE conda env to use")
parser.add_argument('-o', required = True, type=str,  help = 'output.json file')
parser.add_argument('-i', required = True,  type = str, nargs="+", help = 'vcf file(s) or tsv file(s) or json file(s). can be a directory if specified using --dir argument')
parser.add_argument('--filetype', required = False,  default="tsv", choices=["tsv", "vcf", "json"], type = str, help = 'type of file(s), tsv (default), json, or vcf')
parser.add_argument('--depth', required = False,  type = str, help = 'Depth file for all or one single sample, used if the depth_type argument called is "full". Ignore if it is "variant" ')
parser.add_argument('--varianttype', required = False,  default="tsv", type = str, help = 'type of file(s), tsv or vcf')
parser.add_argument('-ct', required = False,  type = str, help = 'If using a tsv file to record variants, this is a column that indicates the total depth at position like TOTAL_DP in ivar pipeline')
parser.add_argument('-ch', required = False,  default="REGION", type = str, help = 'If using a tsv file to record variants, this is the reference name')
parser.add_argument('-cp', required = False,  default="POS", type = str, help = 'If using a tsv file to record variants, this is the reference name')
parser.add_argument('-cr', required = False,  default="REF_AA", type = str, help = 'If using a tsv file to record variants, this is the reference aa column')
parser.add_argument('-ca', required = False,  default="ALT_AA", type = str,  help = 'If using a tsv file to record variants, this is the alternative, mutant column')
parser.add_argument('-cad', required = False,  default="ALT_DP", type = str,  help = 'Define the column for mutant depth from variant file, only used if depth_type if from the variant file')
parser.add_argument('-crd',required = False,  default="REF_DP", type = str,  help = 'Define the column for reference depth from variant file, only used if depth_type if from the variant file')
parser.add_argument('-g', required = False,  default=None, type = str, help = 'vcf file or tsv file. ')
parser.add_argument('-gm', required = False,  default="prep_id", type = str, help = 'If using tsv file, map this column in the -g file to the -ch column in variants file, Usually this is the prep id (prep_id)')
parser.add_argument('--ref', required = False,  type=str, help = 'File containing one or more reference fastas, to be referenced and mapped with the -ch line')
parser.add_argument('--dir', required = False, default=False, action='store_true', help = 'Loop through a directory for necessary files')
parser.add_argument('--dir_depth', required = False, default=False, action='store_true', help = 'Loop through directory for depth files at all positions')
parser.add_argument('-regdir', required = False, type = str, default=".*", help = 'find all files with regex pattern, only used with the -dir argument for specifying a directory')
parser.add_argument('--gb', required = False,  nargs="+", type=str, help = 'File(s) (.gb or .gp) each containing one or more protein structures. If specified, only the positions for all headers within the proteins in the file will be used, indexed back to 0')
parser.add_argument('--get_gb', required = False, default=False, action='store_true', help = 'If called, pull genbank ID externally for parsing. Only occurs if the -gb files do not have the necessary accessionw in them for organism and gene')
parser.add_argument('--email', required = False, type = str, help = 'If you need to pull genbank entry, must provide email for entrez access via biopython')
parser.add_argument('-map_sample', required = False, type = str, help = 'Mapping file for sample name to prep and groupname')
parser.add_argument('--depth_type', required = False, choices=['full', 'variant'], default="full", type=str,  help = 'Specify how depth is read, either from a depth file (like samtools depth) OR straight from the vcf file such as during consensus variant calling')
parser.add_argument('--merge', required = False, default=False, action='store_true', help = 'Merge one or more jsons (out.json e.g.) that is generated from the main functionality, then exit')
parser.add_argument('-map_pdb', required = False, type = str, help = 'Mapping file for organism (genbank) and pdb id ')
parser.add_argument('--get_pdb', required = False, default=False, action='store_true', help = 'If called, pull pdb id mapping to genbank accession')
parser.add_argument('-map_old_organism', required = False, type = str, help = 'Mapping file for organism(s) to a sample name')
parser.add_argument('--name', required = False, type = str, default="Unlisted", help = 'Name to portray for the experiment')

arg_parsed = parser.parse_args()
import glob

from Bio import SeqIO, Entrez
from Bio.Seq import Seq
from Bio.SeqFeature import SeqFeature, FeatureLocation
# print(records[0].id)  # first record
# print(records[-1].id)  # last record
def write_output(output, data):
    f = open(output, "w")

    # print(json.dumps(entry, indent=4, sort_keys=True))
    
    # f.write(json.dumps(data, indent = 4,sort_keys=True))
    f.write(json.dumps(data,  sort_keys=False))
    f.close()

def main():


    ######################################################################################################################################
    ####### Define MAIN variables for use later   ########################################################################################
    ######################################################################################################################################    




    args = vars(arg_parsed)


    if args['merge']:
        jsons = []
        print("merging files")
        for file in args['i']:
            json_1 = json.load(open(file))
            for experiment in json_1:
                jsons.append(experiment)
        write_output(args['o'], jsons)
        exit()


    # args['i'] = args['i'][0]

    if args['get_gb'] and not args['email']:
        print("please specify email since you're pulling external gb files")
        exit()
    elif args['email']:
        email = args['email']

    if args['depth_type'] != "variant" and args['depth'] is None:
        print("Using a depth file since full is called for depth type, but no depth argument specified. Please call depth from the variant depth_type OR specify a depth file or directory with --depth Exiting...")
        exit()
    data = None
    positions = dict()
    references = dict()
    protein_references = dict()
    data_depth = None
    depth_map = dict()
    
    ######################################################################################################################################
    #################################################### END #############################################################################
    ######################################################################################################################################


    data_pdb  = None
    map_pdb = dict()
    map_organism_sample = dict()
    if args['map_old_organism']:
        data_sample_organism = pd.read_csv(args['map_old_organism'],  keep_default_na=False, sep="\t", header=0)
        for index, row in data_sample_organism.iterrows():
            map_organism_sample[row['file']] = row
    if args['map_pdb']:
        data_pdb = pd.read_csv(args['map_pdb'], sep="\t", header=0,keep_default_na=False)
        for index, row in data_pdb.dropna().iterrows():
            if row['organism'] :
                if row['organism']  not in map_pdb:
                    map_pdb[row['organism']] = dict()
                if row['pdb'] and not pd.isna(row['pdb']):
                    map_pdb[row['organism']][row['gene']] = row['pdb']
    ######################################################################################################################################
    ####### Define MAIN variables for use later   ########################################################################################
    ######################################################################################################################################  
    if args['gb'] is not None and len(args['gb']) > 0:
        def iterate_file_gb(gb_file):
            with open(gb_file) as input_handle:
                for record in SeqIO.parse(input_handle, "genbank"):
                    parsed_gb = parse_gb(record, pathlib.Path(gb_file).suffix)
                    if record.id not in protein_references:
                        protein_references[record.id] = dict()
                    for gene, geneValue in parsed_gb.items():
                        protein_references[record.id][gene] = geneValue
        for gb_file in args['gb']:
            if os.path.isdir(gb_file):
                files = [f for f in os.listdir(gb_file) if f.endswith('.gb')]
                for f in files:
                    iterate_file_gb(os.path.join(gb_file, f))
            else:
                    iterate_file_gb(gb_file)
    ######################################################################################################################################
    #################################################### END #############################################################################
    ######################################################################################################################################

    ######################################################################################################################################
    ####### Define MAIN variables for use later   ########################################################################################
    ###################################################################################################################################### 
    def mark_position_variant(val):
        ref  = val[args['cr']]
        variant  = val[args['ca']]
        header = val[args['ch']]
        pos = val[args['cp']]
        experiment = val['experiment']
        group = val['group']
        sample = val['sample']
        total = 1
        depth = 1



        if args['ct']:
            depth = val[args['ct']]
        elif args['depth_type'] == 'variant':
            depth = val[args['crd']] + val[args['cad']]
        else:
            if sample in depth_map and header in depth_map[sample] and pos in depth_map[sample][header]:            
                depth = depth_map[sample][header][pos]
        if experiment not in positions:
            positions[experiment] = dict()
        if group not in positions[experiment]:
            positions[experiment][group] = dict()
        if sample not in positions[experiment][group]:
            positions[experiment][group][sample] = dict()
        if variant != ref:
            if header not in positions[experiment][group][sample]:
                positions[experiment][group][sample][header] = dict()
            if pos not in positions[experiment][group][sample][header]:
                positions[experiment][group][sample][header][pos] = dict()
            positions[experiment][group][sample][header][pos]['depth'] = depth
            positions[experiment][group][sample][header][pos]['total'] = depth
            
            if ref not in positions[experiment][group][sample][header][pos]:
                positions[experiment][group][sample][header][pos][ref] = dict()
            if variant not in positions[experiment][group][sample][header][pos][ref]:
                positions[experiment][group][sample][header][pos][ref][variant] = 0
            positions[experiment][group][sample][header][pos][ref][variant] = val[args['cad']]  
        return val
    
    ######################################################################################################################################
    #################################################### END #############################################################################
    ######################################################################################################################################


    ######################################################################################################################################
    ####### Take all uniq organisms from input vcf or tsv, query if any are missing from genbank entries so far ##########################
    ######################################################################################################################################

    def get_new_gb(uniq_organisms):
        for organism in uniq_organisms:
            if organism not in protein_references:
                print(organism, ",  not registered in gb files but in variant file, pulling from genbank")
                seq_record = query_gb(email, organism)
                parsed_gb = parse_gb(seq_record, ".gb")

                if seq_record.id not in protein_references:
                    protein_references[seq_record.id] = dict()
                for gene, geneValue in parsed_gb.items():
                    protein_references[seq_record.id][gene] = geneValue
    ######################################################################################################################################
    #################################################### END #############################################################################
    ######################################################################################################################################
    def map_depth(row):
        row = dict(sample=row[3], organism=row[0], position=int(row[1]), depth=int(row[2]))
        if row['sample'] not in depth_map:
            depth_map[row['sample']] = dict()
        if row['organism'] not in depth_map[row['sample']]:
            depth_map[row['sample']][row['organism']] = dict()
        if row['position'] not in depth_map[row['sample']][row['organism']]:
             depth_map[row['sample']][row['organism']][row['position']] = row['depth']
        return row

    #####################################################################################################################################
    ####### Parse all depth files present ###############################################################################################
    #####################################################################################################################################
    names = ['organism', 'position', 'depth']
    data_depth_list = []
    if args['depth_type'] == 'full':
        if args['dir_depth']: #Parse a directory of depth files from variant calling commmands or pipelines
            for file in os.listdir(args['depth']):
                try:
                    fullfile = os.path.join(args['depth'], file)
                    sample = file.split(".")[0]
                    with open(fullfile, "r") as f:
                        for line in f.readlines():
                            # print(line.rstrip().split("\t"))
                            l = line.rstrip().split("\t")
                            data_depth_list.append([l[0], l[1], l[2], sample])

                    # if data_depth is None:
                    #     data_depth = pd.read_csv(fullfile, sep="\t", names=names)
                    #     data_depth['sample'] = sample
                    # else:
                    #     data_partial=pd.read_csv(fullfile, sep="\t",  names=names)
                    #     data_partial['sample'] = sample             
                    #     data_depth = data_depth.append(data_partial)
                except Exception as ex:
                    print(ex)
            for entry in data_depth_list:
                map_depth(entry)
        else:
            sample = os.path.basename(args['depth'].split(".")[0])
            data_depth = pd.read_csv(args['depth'], sep="\t", names=names)
            data_depth['sample']  = sample
            data_depth.apply(map_depth, axis=1)
    else:
        values = []
        names.append("sample")
        for organism, organismValue in protein_references.items():
            for gene, geneValue in organismValue.items():
                positionsGene = geneValue['positions']
                for pos in range(positionsGene[0], positionsGene[1]+1):
                    values.append([organism, pos, 0,  'Unlisted'])
        data_depth = pd.DataFrame(values, columns=names)
        data_depth.apply(map_depth, axis=1)
    ######################################################################################################################################
    #################################################### END #############################################################################
    ######################################################################################################################################
    



    ######################################################################################################################################
    ####### READ VCF or tsv file (like ivar variant call output)  ########################################################################
    ######################################################################################################################################

    def read_vcf(fullfile, sample):
        names = ["REGION", "POS", args['cr'], args['ca'], args['crd'], args['cad']]
        # Set the default
        values = []
        
        data = pd.DataFrame([], columns=names)
        # for file in args['i']:
        vcf_reader = vcf.Reader(open(fullfile, 'r'))
        for record in vcf_reader:
            if record.is_indel:
                print("Indel found, skipping as it is not supported right now:  ", record)
                continue
            record.POS = int(record.POS)
            organism = record.CHROM
            present = None
            if sample not in depth_map:
                depth_map[sample] = dict()
            if record.CHROM not in depth_map[sample]:
                depth_map[sample][record.CHROM] = dict()
            if record.POS in depth_map[sample][record.CHROM]:
                ref_depth  = depth_map[sample][record.CHROM][record.POS]
            else:
                depth_map[sample][record.CHROM][record.POS] = 0
                ref_depth = 0
            alt_depth = 0
            alt = str(record.ALT[0])
            ref = record.REF
            info = record.INFO

            if args['depth_type'] == 'full':
                ref_depth = depth_map[sample][record.CHROM][record.POS] - int(info[args['cad']][0])
                alt_depth = info[args['cad']][0]
            else:
                ref_depth  = info[args['crd']][0]
                alt_depth  = info[args['cad']][0]
            if organism not in protein_references and args['get_gb']:
                get_new_gb([organism])
            # if args['vcf_type'] != "aa":
            present  = None
            if organism in protein_references:
                for gene, geneValue in protein_references[organism].items(): 
                    positions = geneValue['positions']
                    if record.POS >= positions[0] and record.POS <= positions[1]:
                        adjusted_position = record.POS - positions[0]  +1
                        # adjusted_position = adjusted_position - 1
                        #### Possible Positions #####
                        # 0 - right-most nt in codon
                        # 1 - midd nt of codon
                        # 2 - left nt of codon
                        nts = ""
                        nt = record.POS
                        seq = geneValue['seq']
                        pro = geneValue['protein']
                        # nt  = 21554
                        # nt = 265
                        # nt = 21552
                        # adj = nt +1 - positions[0] 
                        # posu = math.ceil(  ( (nt+1) - (positions[0]) ) / 3  )  
                        
                        adjusted_position = nt - positions[0] 
                        if adjusted_position == 0:
                            adjusted_position +=1
                        
                        
                        remainder = adjusted_position % 3
                        posu = math.ceil(   (adjusted_position )  / 3 )
                        print("Location: %s\nGene %s\n Record Positions: %s\nPosu %s \nRemainder: %s \nAdjusted position: %s \n Alt NT: %s \n " % ( geneValue['location'], gene,nt,posu, remainder, adjusted_position, alt  ))
                        # exit()
                        if posu > len(pro):
                            print("Stop codon reached, protein residue out of bounds, skipping...\n_____\n")
                            break
                        else:
                            adjusted_position = adjusted_position - 1
                            protein = pro[  posu - 1 ]
                            if remainder == 0:
                                nts=[adjusted_position-2, adjusted_position+1]
                            elif remainder == 1:
                                nts=[adjusted_position, adjusted_position+3]
                            else:                              
                                nts=[adjusted_position-1, adjusted_position+2]
                            f = SeqFeature(FeatureLocation(  nts[0], nts[1] ), type="domain"   )
                            # print(record.POS, geneValue['location'], f,"Protein: ", protein, "Codon translated: ", Seq.translate(f.extract(seq) )  )
                            # print(f.extract(seq))
                            present = geneValue
                            pulled_seq  = f.extract(seq)
                            ref = Seq.translate(pulled_seq)
                            # print(seq[1838:1845])
                            if remainder == 1:
                                alt = alt + pulled_seq[1:3]
                            elif remainder == 2:
                                alt = pulled_seq[0] + alt + pulled_seq[2]
                            else:
                                alt = pulled_seq[0:2] + alt 
                            alt_protein = Seq.translate(alt)
                            alt=alt_protein
                        break
            else:
                print(organism, ", Couldn't find the gene and codon necessary for mapping mutation, skipping at position: ", record.POS)
                alt = ref
            if not record.is_indel:
                values.append([record.CHROM, record.POS, ref, alt, int(ref_depth), int(alt_depth)  ])
        return  values
    uniq_organisms = []
    def parse_old_json(json_data, fullfile):
        items = []
        for index, row in json_data.iterrows():
            organism = map_organism_sample[fullfile]['organism']
            protein =  map_organism_sample[fullfile]['gene']
            prep_id = row['prep_id']
            group = row['group']
            experiment = row['experiment']
            if prep_id not in positions:
                positions[prep_id] = dict()
            if group not in positions[prep_id]:
                positions[prep_id][group] = dict()
            if experiment not in positions[prep_id][group]:
                positions[prep_id][group][experiment] = dict()
            if organism not in positions[prep_id][group][experiment]:
                positions[prep_id][group][experiment][organism] = dict(protein=protein)
                if organism not in uniq_organisms:
                    uniq_organisms.append(organism)
            # print(organism)
            for x in row['residues']:
                positions[prep_id][group][experiment][organism][x['position']] = x

                
    data = None
    if args['dir']:
        for directory in args['i']:
            for file in os.listdir(directory):
                if file.endswith("."+args['filetype']):
                    fullfile = os.path.join(directory, file)
                    sample = file.split(".")[0]
                    if args['filetype'] == 'vcf':
                        records = read_vcf(fullfile, sample)
                        names = ["REGION", "POS",  args['cr'], args['ca'], args['crd'], args['cad']]
                        if data is None:
                            data = pd.DataFrame(records, columns=names)
                            data['sample'] = sample
                        else:
                            data_partial = pd.DataFrame(records, columns=names)
                            data_partial['sample'] = sample
                            data = data.append(data_partial)
                    elif args['filetype'] == 'json' :
                        data_json = pd.read_json(fullfile)
                        parse_old_json(data_json, fullfile)
                    else:
                        if data is None:
                            data = pd.read_csv(fullfile, sep="\t", header=0,encoding= 'unicode_escape')
                            data['sample'] = sample
                        else:
                            data_partial=pd.read_csv(fullfile, sep="\t", header=0)
                            data_partial['sample'] = sample
                            data = data.append(data_partial)
                        uniq_organisms = data[args['ch']].unique()
                        get_new_gb(uniq_organisms)
    else:
        for file in args['i']:
            print(file)
            sample = os.path.basename(file.split(".")[0])
            if args['filetype'] == 'vcf':
                records = read_vcf(file, sample)
                names = ["REGION", "POS",  args['cr'], args['ca'], args['crd'], args['cad']]
                if data is None:
                    data = pd.DataFrame(records, columns=names)
                    data['sample'] = sample
                else:
                    data_partial = pd.DataFrame(records, columns=names)
                    data_partial['sample'] = sample
                    data = data.append(data_partial)
            elif args['filetype'] == 'json':
                data_json = pd.read_json(file)
                parse_old_json(data_json, file )
            else:
                if data is None:
                    data = pd.read_csv(file, sep="\t",encoding= 'unicode_escape')
                    data['sample'] = sample
                else:
                    data_partial = pd.DataFrame(file, columns=names)
                    data_partial['sample'] = sample
                    data = data.append(data_partial)
    if args['filetype'] == 'vcf' or args['filetype'] == 'tsv':
        uniq_organisms = data[args['ch']].unique()

    uniq_proteins = []
    uniprot_pdbs_proteins = []
    i = 0
    for organism in uniq_organisms:
        if organism not in map_pdb:
            map_pdb[organism] = dict()
        for protein_id, proteinValue in protein_references[organism].items():
            try:
                if organism in map_pdb and protein_id in map_pdb[organism]:
                    if map_pdb[organism][protein_id]:
                        proteinValue['pdb'] = map_pdb[organism][protein_id]
                    else:
                        proteinValue['pdb'] = "0"
                else:
                    print(proteinValue['id'])
                    protein = query_genbank_to_uniprot(proteinValue['id'])
                    if protein is not None and len(protein) >=1:
                        protein_list = protein[1].split("\t")
                        first_protein = protein_list[1]
                        pdb = ""
                        if args['get_gb']:
                            print("Querying the uniprot id: %s" % (first_protein))
                            pdb=query_uniprot_to_pdb(first_protein)
                            print("Received the pdb id from the above uniprot mapping: %s" % (pdb[first_protein]['data'][0]['accession']))
                            uniprot_pdbs_proteins.append([
                                proteinValue['id'], first_protein, pdb[first_protein]['data'][0]['accession']
                            ])
                        else:
                            uniprot_pdbs_proteins.append([
                                proteinValue['id'], first_protein, ""
                            ])
                        map_pdb[organism][protein_id] = pdb[first_protein]['data'][0]['accession']
                        proteinValue['pdb'] = map_pdb[organism][protein_id]
                        i+=1
            except Exception as ex:
                print(ex)
    print("Mapping genbanks/uniprot to pdbids")
    for n in uniprot_pdbs_proteins:
        print("%s\t%s\t%s"   %   (   n[0], n[1], n[2]   ))
    


    ######################################################################################################################################
    #################################################### END #############################################################################
    ######################################################################################################################################

    
    

    ######################################################################################################################################
    ####### Get mapping of Experiments to Samples from input file vcf or tsv  ############################################################
    ######################################################################################################################################

    data_map = None
    if args['map_sample']:
        data_map = pd.read_csv(args['map_sample'], sep=",", index_col="sample_name", header=0)

    
    def apply_mapping(sample, col):
        if sample in data_map.index:
            return str(data_map.loc[sample][col])
        else:
            return "Unlisted"

    ######################################################################################################################################
    #################################################### END #############################################################################
    ######################################################################################################################################
    if args['filetype'] != 'json':
        if data_map is not None:
            data['experiment'] = data['sample'].apply(apply_mapping, args=('prep_id',) )
            data['group'] = data['sample'].apply(apply_mapping, args=('group',))
        else:
            data['experiment'] = "Unlisted"
            data['group'] = "Unlisted"
        data.dropna(subset=[ args['ch'], args['cp'], args['cr']  ], inplace=True)
        data = data.reset_index()
        data.apply(mark_position_variant, axis=1)


    list_dict = []
    formated_positions = dict()
    output_list  = [  dict(entries = [], name=args['name'], proteins=dict() )]
    output = output_list[0]
    for experiment, value in positions.items():
        for group, value2 in value.items():
            for sample, v in value2.items():
                entry = dict(sample=sample, group=group, experiment=experiment, items=[] )
                uniq_organisms = list(set(value2.keys()))
                for organismName, value3 in v.items():
                    # organism = dict(
                    #     genes=[],
                    #     organism=organismName
                    # )
                    if organismName in protein_references:
                        seen = dict()
                        
                        if organismName not in output['proteins']:
                            output['proteins'][organismName] = dict()
                        if args['filetype'] != 'json':
                            for geneName, proteinValue in protein_references[organismName].items():
                                if "pdb" not in proteinValue:
                                    proteinValue['pdb'] = ""
                                gene  = dict(
                                    residues=[],
                                    depths=[],
                                    gene=geneName,
                                    organism=organismName,
                                    pdb = proteinValue['pdb']
                                )
                                for posi in range(1, 1+len(proteinValue['protein'])):
                                    # print(posi)
                                    
                                    nucleotides = None
                                    if sample in depth_map:
                                        nucleotides = depth_map[sample][organismName]
                                    else:
                                        nucleotides = depth_map['Unlisted'][organismName]

                                    nts = [ 3*posi , 3*posi + 1, 3*posi + 2]
                                    nt_depths = []
                                    for nt in nts:
                                        if nt not in nucleotides:
                                            nt_depths.append(0)
                                        else:
                                            nt_depths.append(nucleotides[nt])
                                    min_depth = min(nt_depths)
                                    gene['depths'].append(min_depth)
                                    # print(sample, posi, nts, min_depth, nt_depths, geneName)


                                if geneName not in output['proteins'][organismName]:
                                    output['proteins'][organismName][geneName]=proteinValue['protein'] 
                                
                                positions_gene = proteinValue['positions']
                                current_pos = 0  
                                protein_found = False
                                residues=[]
                                for posi in range(0,  len(proteinValue['protein'])   ):
                                    present = None

                                    for nt in range(positions_gene[0] + posi*3, positions_gene[0] + (posi*3)+3):
                                        if nt in value3:
                                            present = nt
                                            remainder = nt % 3
                                            
                                    if present:
                                        variant = value3[present]

                                        protein_found = True
                                        gene['depths'][posi] = variant['depth']
                                        ent = dict(
                                            position=posi+1, 
                                            depth=variant['depth'],
                                            nt_pos=present,
                                            reference_aa=proteinValue['protein'][ posi ],
                                            consensus_aa=proteinValue['protein'][ posi ],
                                            consensus_aa_count=1,
                                            counts=[]
                                        )
                                        for index3, ref in variant.items():
                                            if index3 != "total" and index3 != "depth":
                                                alternatives = [ dict(variant=item, value=value) for item, value in ref.items()]
                                                consensus_aa = alternatives[max(range(len(alternatives)), key=lambda index: alternatives[index]['value'] )]
                                                consensus_aa_count = consensus_aa['value']
                                                consensus_aa = consensus_aa['variant']
                                                ent['consensus_aa'] = consensus_aa
                                                ent['consensus_aa_count'] = consensus_aa_count
                                                if consensus_aa_count > variant['depth']:
                                                    ent['depth'] = consensus_aa_count
                                                summation = 0
                                                for index4, alt in ref.items():
                                                    ent['counts'].append(dict(
                                                        aa =  index4, 
                                                        count = alt
                                                    ))
                                                    summation += alt
                                                if summation < ent['depth']:
                                                    ent['counts'].append(dict(
                                                        aa =  index3, 
                                                        count = ent['depth'] - summation
                                                    ))
                                        residues.append(ent)
                                if protein_found:
                                    gene['residues'] = residues
                                    entry['items'].append(gene)
                        else:
                            proteinValue = protein_references[organismName][value3['protein']]
                            if "pdb" not in proteinValue:
                                proteinValue['pdb'] = ""
                            geneName = value3['protein']
                            gene  = dict(
                                    residues=[],
                                    depths=[],
                                    gene=value3['protein'],
                                    organism=organismName,
                                    pdb = proteinValue['pdb']
                            )
                            if geneName not in output['proteins'][organismName]:
                                output['proteins'][organismName][geneName]=proteinValue['protein'] 
                            for posi, resid in value3.items():  
                                if posi != 'protein':
                                    posi = int(posi)
                                # for residue, residueValue in residues.items():
                                if posi != 'protein' and posi - 1 < len(proteinValue['protein']):
                                    ent = dict(
                                        position=posi, 
                                        depth=resid['depth'],
                                        reference_aa=proteinValue['protein'][ posi-1 ],
                                        consensus_aa=resid['consensus_aa'],
                                        consensus_aa_count=resid['consensus_aa_count'],
                                        counts=resid['counts']
                                    )
                                    gene['residues'].append(ent)
                            # organism['genes'].append(gene)
                            entry['items'].append(gene)
                    # entry['organisms'].append(organism)
                output['entries'].append(entry)
    write_output(args['o'], output_list)
    
if __name__ == "__main__":
    main()    
