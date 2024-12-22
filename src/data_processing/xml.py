import xml.etree.ElementTree as ET


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
