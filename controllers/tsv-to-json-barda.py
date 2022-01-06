import pandas as pd
import json

data = pd.read_csv("diversity-Giessen2009.txt", delimiter="\t", header=0, keep_default_na=False, na_values=['_'])
grouped_data = data.groupby(data["ORF_name"])

subject_info = pd.read_csv("subjects.csv", index_col=0)

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

for segment in final_output:
  print("Processing ", segment)
  segment_data = grouped_data.get_group(segment)
  pivoted_segment_data = pd.pivot_table(segment_data, values=amino_acids, index="file", columns="amino_acid")
  pivoted_segment_data.columns = pivoted_segment_data.columns.rename(["amino_acid", "position"])
  pivoted_segment_data.columns = pivoted_segment_data.columns.swaplevel(0, 1)
  pivoted_segment_data.sort_index(axis=1, level=0, inplace=True)
  for prep_id, row_contents in pivoted_segment_data.iterrows():
    if prep_id in subject_info.index:
      prep_object = {}
      prep_object["prep_id"] = prep_id
      prep_object["group"] = subject_info["group"][prep_id]
      prep_object["experiment"] = subject_info["sample_name"][prep_id]
      prep_object["residues"] = []
      for position in row_contents.index.unique(level="position"):
        counts = row_contents.loc[position]
        position_info = {}
        position_info["consensus_aa"] = counts.idxmax()
        position_info["consensus_aa_count"] = int(counts.max())
        position_info["position"] = position
        position_info["depth"] = int(counts.sum())
        position_info["counts"] = []
        for index, count in counts.iteritems():
          if count > 0.0:
            position_info["counts"].append({
              "aa": index,
              "count": int(count)
            })
        prep_object["residues"].append(position_info)
      final_output[segment].append(prep_object)

  # send each segment to its own file
  with open(f'{segment}.json', 'w') as json_file:
    json.dump(final_output[segment], json_file)