## Final Project
This repository contains code related to the final project of
[CSE 6242: Data and Visual Analytics](https://omscs.gatech.edu/cse-6242-data-visual-analytics).

## Links
- [Project Description](https://docs.google.com/document/d/e/2PACX-1vSlYrMw402tL3F95ay-AaptTdF80UOER-gne_O0kqbuuk6WXrlsjwaYjjS0Jyl95dXYyDLjh9DR1mln/pub)
- [Project Proposal](https://docs.google.com/document/d/1DTW47zXW2rzbVkHM4GLeFzOclJOMAuph4Z5-gXX5k5c/edit)
- [Project Team Tasks](https://docs.google.com/document/d/1n_YQuL9-CeGPTlXEqUlfWlNgd00ygJ2FoBVJS8xYR94/edit)
- [Project Drive](https://drive.google.com/drive/folders/1tlR_83Kof5RTz8a66ZOJtygNr57252UU)
- [DiffusionDB](https://github.com/poloclub/diffusiondb)

## Getting started

1. Set up a Python virtual environment in one of the following ways:
    - **Using venv**:
        - **For Windows**:
            ```
            python -m venv venv
            .\\venv\\Scripts\\activate
            ```
        - **For Mac/Linux**:
            ```
            python3 -m venv venv
            source venv/bin/activate
            ```
    - **Using [Poetry](https://python-poetry.org/docs/)**:
        ```
        poetry install
        poetry shell
        ```
2. If not using Poetry, run `pip install -r requirements.txt` to install all the required dependencies.
3. Run `python get_data.py` to download the dataset.
4. Run `python app.py` to run the web app.
5. Navigate to [http://127.0.0.1:8050/](http://127.0.0.1:8050/) to view it in your browser.