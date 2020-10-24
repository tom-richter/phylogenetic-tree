import json
import argparse

NAME_CLASSES = {
    'scientific name': 'scientificName',
    'synonym': 'synonyms',
    'blast name': 'blastNames',
    'genbank common name': 'genbankCommonNames',
    'in-part': 'inParts',
    'authority': 'authorities', 
    'equivalent name': 'equivalentNames', 
    'includes': 'includes', 
    'common name': 'commonNames', 
    'genbank synonym': 'genbankSynonyms', 
    'acronym': 'acronyms', 
    'genbank acronym': 'genbankAcronyms'
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dmp_path", help="path to folder with dmp files")
    parser.add_argument("print_mode", help="json print mode")
    args = parser.parse_args()

    NAMES_FILE_PATH = args.dmp_path + 'names.dmp'
    NODES_FILE_PATH = args.dmp_path + 'nodes.dmp'

    nodes_file = open(NODES_FILE_PATH, 'r')
    node_lines = nodes_file.readlines()
    names_file = open(NAMES_FILE_PATH, 'r')
    name_lines = names_file.readlines()

    create_json_tree(node_lines, name_lines, mode=args.print_mode)

def create_json_tree(node_lines, name_lines, mode='pretty'):
    nodes = create_nodes_dict(node_lines)
    names = create_names_dict(name_lines)
    tree = recursive_tree(nodes, names, '1')

    with open('output/tree.json', 'w', encoding='utf-8') as f:
        if mode == 'minimal':
            json.dump(tree, f, ensure_ascii=False, indent=None, separators=(',', ':'))
        elif mode == 'pretty':
            json.dump(tree, f, ensure_ascii=False, indent=2)

def create_nodes_dict(node_lines):
    nodes = {}

    for line in node_lines:
        cols = line[:-3].split('\t|\t')
        nodes[cols[0]] = {
            'rank': cols[2],
            'parent': cols[1],
            'children': []
        }
    
    for node in nodes:
        parent = nodes[node]['parent']
        nodes[parent]['children'].append(node)

    nodes['1']['children'].remove('1')

    return nodes

def create_names_dict(name_lines):
    names = {'1': {}}
    
    for line in name_lines:
        cols = line[:-3].split('\t|\t')
        tax_id = cols[0]
        name = cols[1]
        name_class = NAME_CLASSES[cols[3]]

        if tax_id not in names:
            names[tax_id] = {}
        
        if name_class not in names[tax_id]:
            names[tax_id][name_class] = []

        names[tax_id][name_class].append(name)

    return names

def recursive_tree(nodes, names, current_node):
    children = []

    for child_node in nodes[current_node]['children']:
        child_tree = recursive_tree(nodes, names, child_node)
        children.append(child_tree)

    number_of_children = 0

    if len(children):
        for child in children:
            if child['numOfChildren']:
                number_of_children += child['numOfChildren']
            else:
                number_of_children += 1
                
    tree = {
        'rank': nodes[current_node]['rank'],
        'scientificName': names[current_node]['scientificName'][0],
        'otherNames': {},
        'children': children,
        'numOfChildren': number_of_children
    }

    name_classes = ['synonyms', 'commonNames', 'equivalentNames', 'acronyms', 'authorities']

    for name_class in name_classes:
        if name_class in names[current_node]:
            tree['otherNames'][name_class] = names[current_node][name_class]

    return tree

if __name__ == "__main__":
    main()
