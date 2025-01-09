import xml.etree.ElementTree as ET
import pandas as pd
import os

# Default paths
path_train = "data/OHSUMED/train-00000-of-00001.parquet"
path_train = os.path.abspath(path_train)

path_test = "data/OHSUMED/test-00000-of-00001.parquet"
path_test = os.path.abspath(path_test)


def load_parquet_as_df(data_path: str) -> pd.DataFrame:
    df = pd.read_parquet(data_path)
    return df


def is_sensitive(mesh_terms_str, c12_terms, c13_terms):
    """
    Given a string of MeSH terms (delimited by semicolons), return 1
    if any term (minus subheadings) is in c12_terms or c13_terms; else 0.
    """
    # 1. Split on semicolon
    terms = mesh_terms_str.split(';')

    # 2. Clean each term
    clean_terms = []
    for t in terms:
        t = t.strip()            # remove whitespace
        t = t.split('/')[0]      # remove slash-delimited subheadings
        clean_terms.append(t)

    # 3. Check if any cleaned term is in c12_terms or c13_terms
    for ct in clean_terms:
        if ct in c12_terms or ct in c13_terms:
            return 1
    return 0


def get_keywords_from_xml(MESH_XML_FILE: str):

    c12_terms = set()
    c13_terms = set()

    tree = ET.parse(MESH_XML_FILE)
    root = tree.getroot()  # This should be the <MeSHDescriptorSet> element

    for descriptor in root.findall('DescriptorRecord'):
        # Extract the descriptor name
        name_element = descriptor.find('DescriptorName/String')
        if name_element is None:
            continue
        descriptor_name = name_element.text.strip()

        # Extract the tree numbers
        tree_numbers = descriptor.findall('TreeNumberList/TreeNumber')

        # Check each tree number for whether it starts with C12 or C13
        for tn in tree_numbers:
            tn_text = tn.text.strip()
            if tn_text.startswith("C12.200"):  # C12.200 is the precise code for C12
                c12_terms.add(descriptor_name)
            if tn_text.startswith("C12.050"):  # C12.050 is the precise code for C13
                c13_terms.add(descriptor_name)

    return c12_terms, c13_terms