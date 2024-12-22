
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
