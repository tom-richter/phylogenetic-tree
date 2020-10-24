import json
import argparse

from validate_dumps import get_ranks, get_name_classes

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dmp_path", help="path to folder with dmp files")
    args = parser.parse_args()

    NAMES_FILE_PATH = args.dmp_path + 'names.dmp'
    NODES_FILE_PATH = args.dmp_path + 'nodes.dmp'

    nodes_file = open(NODES_FILE_PATH, 'r')
    node_lines = nodes_file.readlines()
    names_file = open(NAMES_FILE_PATH, 'r')
    name_lines = names_file.readlines()

    ranks = ['no rank', 'superkingdom', 'genus', 'species', 'order', 'family', 'subspecies', 'subfamily', 'strain', 'serogroup', 'biotype', 'tribe', 'phylum', 'class', 'species group', 'forma', 'clade', 'suborder', 'subclass', 'varietas', 'kingdom', 'subphylum', 'forma specialis', 'isolate', 'infraorder', 'superfamily', 'infraclass', 'superorder', 'subgenus', 'superclass', 'parvorder', 'serotype', 'species subgroup', 'subcohort', 'cohort', 'genotype', 'subtribe', 'section', 'series', 'subvariety', 'morph', 'subkingdom', 'superphylum', 'subsection', 'pathogroup']
    name_classes = ['synonym', 'scientific name', 'blast name', 'genbank common name', 'in-part', 'authority', 'equivalent name', 'includes', 'common name', 'genbank synonym', 'acronym', 'genbank acronym']

    with open('output/script.sql', 'w') as f:
        f.write(get_tax_ranks_sql(ranks))
        f.write(get_name_classes_sql(name_classes))
        f.write(get_nodes_sql(node_lines, ranks))
        f.write(get_names_sql(name_lines, name_classes))

def get_tax_ranks_sql(ranks):
    ranks_sql = "INSERT INTO tax_ranks(name) VALUES"
    for rank in ranks:
        ranks_sql += " ('{}'),".format(rank) 
    ranks_sql = ranks_sql[:-1] + ";\n"
    return ranks_sql

def get_name_classes_sql(name_classes):
    name_classes_sql = "INSERT INTO tax_name_classes(name) VALUES"
    for name_class in name_classes:
        name_classes_sql += " ('{}'),".format(name_class) 
    name_classes_sql = name_classes_sql[:-1] + ";\n"
    return name_classes_sql

def get_nodes_sql(node_lines, ranks):
    nodes_sql = "INSERT INTO tax_nodes(node_id, parent_id, rank_id) VALUES"
    for line in node_lines:
        cols = line[:-3].split('\t|\t')
        nodes_sql += " ({}, {}, {}),".format(cols[0], cols[1], (ranks.index(cols[2]) + 1)) 
    nodes_sql = nodes_sql[:-1] + ";\n"
    return nodes_sql

def get_names_sql(name_lines, name_classes):
    names_sql = "INSERT INTO tax_names(node_id, name_class_id, name) VALUES"
    for line in name_lines:
        cols = line[:-3].split('\t|\t')
        names_sql += " ({}, {}, '{}'),".format(cols[0], (name_classes.index(cols[3]) + 1), cols[1]) 
    names_sql = names_sql[:-1] + ";\n"
    return names_sql

if __name__ == "__main__":
    main()
