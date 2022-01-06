import pandas as pd
import json
import argparse

'''
Turn a sparse tsv file from the swarm pipeline into json files that the heatmap can consume
Input: data tsv filepath (the counts of each residue)
       metadata csv filepath (the mapping of each prep id to experiment and group names)
Output: eight json files, one for each flu segment
Example command:
python tsv-to-json-swarm.py -i diversity-Giessen2009.txt -m subjects.txt
'''

# Define tsv filename
parser = argparse.ArgumentParser(description="Turns sparse input tsv file into json file that the heatmap can consume")
parser.add_argument("-i", "--input", help="Input tsv file from swarm", required=True)
parser.add_argument("-m", "--metadata", help="Input csv file with metadata", required=True)
args = parser.parse_args()
input = args.input
metadata = args.metadata

# Read input data
data = pd.read_csv(input, delimiter="\t", header=0, keep_default_na=False, na_values=['_'])
# Group input data by segment
grouped_data = data.groupby(data["ORF_name"])

# Read input metadata
subject_info = pd.read_csv(metadata, index_col=0)

# Define variables
amino_acids = ["A", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "[*]"]
final_output = {
  "PB2": [],
  "PB1": [],
  "PA": [],
  "HA": [],
  "NP": [],
  "NA": [],
  "M": [],
  "NS": [],
}

# Process one segment at a time
for segment in final_output:
  print("Processing ", segment)
  segment_data = grouped_data.get_group(segment)

  # Manipulate data into easier format
  pivoted_segment_data = pd.pivot_table(segment_data, values=amino_acids, index="file", columns="amino_acid")
  pivoted_segment_data.columns = pivoted_segment_data.columns.rename(["amino_acid", "position"])
  pivoted_segment_data.columns = pivoted_segment_data.columns.swaplevel(0, 1)
  pivoted_segment_data.sort_index(axis=1, level=0, inplace=True)

  # Iterate through individual prep_ids and create an object for each one
  for prep_id, row_contents in pivoted_segment_data.iterrows():
    if prep_id in subject_info.index:
      prep_object = {}
      prep_object["prep_id"] = prep_id
      prep_object["group"] = subject_info["group"][prep_id]
      prep_object["experiment"] = subject_info["sample_name"][prep_id]
      prep_object["residues"] = []

      # Iterate through positions within each prep_id and create an object for each one
      for position in row_contents.index.unique(level="position"):
        counts = row_contents.loc[position]
        position_info = {}
        position_info["consensus_aa"] = counts.idxmax()
        position_info["consensus_aa_count"] = int(counts.max())
        position_info["position"] = position
        position_info["depth"] = int(counts.sum())
        position_info["counts"] = []

        # Iterate through nonzero counts for each position and create an object for each one
        for index, count in counts.iteritems():
          if count > 0.0:
            position_info["counts"].append({
              "aa": index,
              "count": int(count)
            })

        prep_object["residues"].append(position_info)
      final_output[segment].append(prep_object)

  # Send each segment to its own file
  with open(f'{segment}.json', 'w') as json_file:
    json.dump(final_output[segment], json_file)