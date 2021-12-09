import pandas as pd
from Bio import SeqIO, Entrez
import re
import urllib.parse
import urllib.request

import json

def query_uniprot_to_pdb(id):
    url = 'https://www.ebi.ac.uk/pdbe/graph-api/uniprot/unipdb/' + id

    # data = urllib.parse.urlencode(params)
    # data = data.encode('utf-8')
    req = urllib.request.urlopen(url)
    data = req.read()
    JSON_object = json.loads(data.decode('utf-8'))
    return JSON_object

def query_genbank_to_uniprot(id):
    url = 'https://www.uniprot.org/uploadlists/'

    params = {
        'from': 'EMBL',
        'to': 'ACC',
        'format': 'tab',
        'query': id
    }

    data = urllib.parse.urlencode(params)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as f:
        response = f.read()
        return response.decode('utf-8').splitlines()


def query_gb(email, organism):
  Entrez.email = email
  handle = Entrez.efetch(db="nucleotide", rettype="gb", id=organism)
  seq_record = SeqIO.read(handle, "gb")
  return seq_record
def parse_gb(record, suffix ):
  protein_references = dict()
  if suffix == '.gb':
      for feature in record.features:
          if feature.type == "CDS":
              gene = "unknown"
              translation = ""
              idd="None"
              if feature.qualifiers:
                  if "translation" in feature.qualifiers:
                      translation = feature.qualifiers['translation'][0]
                  # else:
                  #     print(feature)
                  if "gene" in feature.qualifiers :
                      gene = feature.qualifiers['gene'][0]
                  if "protein_id" in feature.qualifiers:
                      idd = feature.qualifiers['protein_id'][0]
              positions_gene = list(feature.location)
              protein_references[gene] = dict(
                  positions=[min(positions_gene), max(positions_gene)], 
                  protein=translation,
                  record=record,
                  id=idd,
                  location=feature.location,
                  seq=str(feature.location.extract(record).seq)
              )
  elif suffix == '.gp':
      for feature in record.features:
          if feature.type == "CDS":
              gene = "unknown"
              seq = None
              idd = "None"
              if feature.qualifiers:
                  if "protein_id" in feature.qualifiers:
                      idd = feature.qualifiers['protein_id'][0]
                  if "gene" in feature.qualifiers :
                      gene = feature.qualifiers['gene'][0]
                  if "coded_by" in feature.qualifiers:
                      seq = re.split(":|\.\.", feature.qualifiers['coded_by'][0])
              positions_gene = list(feature.location)
              translation = str(record.seq)
              protein_references[gene] = dict(
                  positions=[1 + min(positions_gene)*3, 1+ max(positions_gene)*3], 
                  location=feature.location,
                  protein=str(feature.location.extract(record).seq),
                  record=record,
                  id=idd,
                  seq=None
              )
  return protein_references