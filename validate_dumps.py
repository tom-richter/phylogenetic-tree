import re
import argparse

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
    validate_all(node_lines, name_lines)

def validate_all(node_lines, name_lines):
    ranks = get_ranks(node_lines)
    print('All ranks ({}):\n{}'.format(len(ranks), ranks))
    name_classes = get_name_classes(name_lines)
    print('\nAll name classes ({}):\n{}'.format(len(name_classes), name_classes))
    print('\nNodes without scientific name:\n{}'.format(get_nodes_without_scientific_name(name_lines)))
    print('\nNodes not virus with acronym:\n{}'.format(get_nodes_not_virus_with_acronym(name_lines)))

def get_ranks(node_lines):
    ranks = []
    
    for line in node_lines:
        
        cols = line[:-3].split('\t|\t')

        if cols[2] not in ranks:
            ranks.append(cols[2])

    return ranks

def get_name_classes(name_lines):
    name_classes = []
    
    for line in name_lines:
        cols = line[:-3].split('\t|\t')

        if cols[3] not in name_classes:
            name_classes.append(cols[3])

    return name_classes


def get_nodes_without_scientific_name(name_lines):
    last_line = name_lines[-1]
    nodes_without_scientific_name = []
    current_node_id = '1'
    has_scientific_name = False

    for line in name_lines:
        cols = line[:-3].split('\t|\t')

        if line == last_line and cols[3] == 'scientific name':
            has_scientific_name = True

        if cols[0] != current_node_id or line == last_line:

            if not has_scientific_name:
                nodes_without_scientific_name.append(current_node_id)

            current_node_id = cols[0]
            has_scientific_name = False

        if cols[3] == 'scientific name':
            has_scientific_name = True

    return nodes_without_scientific_name

def get_nodes_not_virus_with_acronym(name_lines):
    last_line = name_lines[-1]
    nodes_not_virus_with_acronym = []
    current_node_id = '1'
    has_acronym = False
    names = ''

    for line in name_lines:
        cols = line[:-3].split('\t|\t')

        if line == last_line:
            names += cols[1]

        if cols[0] != current_node_id or line == last_line:

            if has_acronym and not re.search(r'[Vv]irus', names):
                nodes_not_virus_with_acronym.append(current_node_id)

            current_node_id = cols[0]
            has_acronym = False
            names = ''

        if cols[3] == 'acronym':
            has_acronym = True

        names += cols[1]

    return nodes_not_virus_with_acronym

if __name__ == "__main__":
    main()
