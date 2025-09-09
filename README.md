# Crowdsourced Prompt Engineering for AI Image Generation
Team #79: Josh Miller, Andrew Getz, Samantha Mohr, Tom George, Josh Rackham, Douglas Amirault

## DESCRIPTION
Prompt Explorer is a standalone web application built with Plotly Dash that enables interactive exploration of Stable Diffusion prompts and their variations, powered by [DiffusionDB](https://github.com/poloclub/diffusiondb). Unlike most prompt engineering tools, which rely on expensive model retraining or trial-and-error evaluation, Prompt Explorer leverages scalable search algorithms to make exploration fast and accessible. Text search is implemented with TF-IDF across the dataset’s prompts, while image search uses CLIP vision transformer embeddings with full dot-product similarity for efficient retrieval after an initial indexing step. This technical foundation provides users with a lightweight yet powerful search experience that scales well, with the flexibility to move to approximate nearest neighbors methods like LSH or HNSW for larger deployments.

What sets Prompt Explorer apart is its ability to crowd-source prompt engineering through community data while surfacing actionable stylistic insights. Users can begin exploration with either a text prompt or an image, helping overcome the common barrier of not knowing how to start. The system automatically tags stylistic modifiers using NLTK and displays them in interactive bar charts, making it easy to identify and apply proven prompt patterns. This combination of scalable dot-product search, automatic style-word tagging, and user-driven exploration transforms a traditionally opaque trial-and-error process into an intuitive, data-driven workflow for creating effective prompts.

## INSTALLATION
1. Set up a Python virtual environment in one of the following ways:
    - **Using venv**:
        - **For Windows**:
            ```
            python -m venv .venv
            .venv\Scripts\activate
            ```
        - **For MacOS/Linux**:
            ```
            python3 -m venv .venv
            source .venv/bin/activate
            ```
    - **Using [Poetry](https://python-poetry.org/docs/)**:
        ```
        poetry install
        poetry shell
        ```
2. If not using Poetry, run `pip install -r requirements.txt` to install all the required dependencies.
3. Run `python3 get_data.py` to download the dataset. For the larger dataset, simply swap out the parameter in the `get_data.py` file.

## EXECUTION 
1. Run `python3 app.py` to run the web app.
2. Navigate to [http://127.0.0.1:8050/](http://127.0.0.1:8050/) to view it in your browser.

## PRESENTATION
Here is my final presentation on this project: [team079poster-amirault](https://youtu.be/iOP4la1vd5U).