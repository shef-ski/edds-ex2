import xml.etree.ElementTree as ET
import pandas as pd
import os

# Default paths (OUTDATED)
# path_train = "data/OHSUMED/train-00000-of-00001.parquet"
# path_train = os.path.abspath(path_train)
# path_test = "data/OHSUMED/test-00000-of-00001.parquet"
# path_test = os.path.abspath(path_test)


def compute_metrics(eval_pred):
    """
    Computes precision, recall, f1, f2, and accuracy for DistilBERT.
    """
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average="binary")
    accuracy = accuracy_score(labels, preds)
    
    # F2 = (1 + 2^2) * (precision * recall) / (2^2 * precision + recall)
    f2 = (5 * precision * recall) / ((4 * precision + recall) + 0.00001)  # avoid div by 0
    
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "f2": f2,
        "accuracy": accuracy,
    }


def parse_ohsumed_file(path: str):

    # Initialisiere Variablen für den Datensatz
    records = []
    current_record = {}

    # Datei zeilenweise einlesen
    with open(path, 'r') as file:
        for line in file:
            line = line.strip() 
            if line.startswith('.I'):  # Each Dataset starts with .I
                if current_record:  #if there is a dataset allready, save it
                    records.append(current_record)
                current_record = {'Sequatial identifier': line.split(' ')[1]}  #initilize new dataset
            else:
                match line[:2]:  # first two chars decide which info is parsed
                    case '.U':
                        current_record['Medline ID'] = next(file).strip()
                    case '.S':
                        current_record['Source'] = next(file).strip()
                    case '.M':
                        current_record['mesh_terms'] = next(file).strip()
                    case '.T':
                        current_record['Title'] = next(file).strip()
                    case '.P':
                        current_record['Publication type'] = next(file).strip()
                    case '.A':
                        current_record['Author'] = next(file).strip()
                    case '.W':
                        current_record['Abstract'] = next(file).strip()
        if current_record:
            records.append(current_record)

    # convert to df
    df = pd.DataFrame(records)

    #cast columns (maybe unnecessary)
    df['Medline ID'] = df['Medline ID'].astype(int)
    df['mesh_terms'] = df['mesh_terms'].astype(object)

    return df.set_index("Medline ID")


def parse_judged_data(path:str):

    df = pd.read_csv(path, sep="\t", header=None, names=["query", "Medline ID", "document-i", "relevance1", "relevance2", "relevance3"])
    #if in one of the 3 relevance couluns is a p (partly relevant) or d (definitely relevant), the document is labled as relavant (1) in a new relevance column
    df["relevance"] = df[["relevance1", "relevance2", "relevance3"]].apply(
    lambda row: 1 if any(val in ['p', 'd'] for val in row.fillna(0)) else 0,
    axis=1
    )
    df = df.drop(["relevance1", "relevance2", "relevance3"], axis=1)
    df['Medline ID'] = df['Medline ID'].astype(int)
    return df


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