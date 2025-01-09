# edds-ex2

### General

Link to the overleaf doc: https://www.overleaf.com/project/67683cb9765d4cd482e8e67e.
This is the template they require us to use I think. It's quite messy with lots of unnecessary stuff in there.

Link to the GitHub repo: https://github.com/shef-ski/edds-ex2 


### Setup

Ideally use Python 3.12. 

Create a venv folder in the project directory using ``python -m venv venv``. Then, activate the venv using ``venv\Scripts\activate``. Install all libraries using ``pip install -r requirements.txt``. Optional: run ``python -m ipykernel install --user --name=myenv --display-name="jupyter edds"`` to set a kernel for Jupyter. 


### Workflow

If possible, let's try to work like this:

Work in your own Jupyter notebook, which is a copy of the most recent notebook (so you can continue where the previous person left off). At the top, explain what has been done and what the next steps are. The next person can then copy the previous notebook and continue working on the next tasks.


### Tips

Use AI models like ChatGPT to quicker understand what's going on, both in the paper and in the code.


### Links for the project

- Link to data: https://huggingface.co/datasets/community-datasets/ohsumed

- XML data from here (Used year 2022): https://www.nlm.nih.gov/databases/download/mesh.html
  
- MESH tree view: https://meshb.nlm.nih.gov/record/ui?ui=D052801
    - Not very necessary, just for browsing the tree structure of MESH
 
- Original data: https://dmice.ohsu.edu/hersh/ohsumed/
    - Contains the original data in a poorer format. Also contains additional files like the queries which might be necessary later to reproduce the *Extrinsic Evaluation* section
