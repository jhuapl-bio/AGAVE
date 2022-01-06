import pandas as pd
import json
import argparse
from query_genbank import parse_gb, query_gb, query_uniprot_to_pdb, query_genbank_to_uniprot

'''
Convert the old format for BARDA/SWARM heatmap viewer into the newer set of JSONs format

Takes the 1 experiment limiting json format for multiple-supporting format. 

'''

# Define tsv filename
parser = argparse.ArgumentParser(description="Turns sparse input tsv file into json file that the heatmap can consume")
parser.add_argument("-i", "--input", help="Input JSON file", required=True)
parser.add_argument("-e", "--experiment", help="Define expeirment name, e.g. Gaydos, BARDA, etc.", required=True)
parser.add_argument("-org", "--organism", help="Define the single organism from the input data. Default is filename base (e.g. HA.json is HA)", required=False)
parser.add_argument("-x", "--external", help="If genbank ID is not provided, get one or more from ncbi to query with", nargs="+", required=False)
parser.add_argument("-gb", "--genbanks", help="List of one or more genbanks to add to the protein structure mapping for each organism.", nargs="+", required=False)


args = parser.parse_args()

data = pd.read_json(args['i'])
print(data)

