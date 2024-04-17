# Crowdsourced Prompt Engineering for AI Image Generation
Team #79: Josh Miller, Andrew Getz, Samantha Mohr, Tom George, Josh Rackham, Douglas Amirault

## DESCRIPTION
This tool leverages the DiffusionDB database to create a user-friendly tool to assist with creating effective text prompts for AI image generation with StableDiffusion [1]. Our tool, Prompt Explorer, is a standalone web app built using Plotly dash and allows users to interact with and explore image generation prompts and their variations. Our text search algorithm is powered using TF-IDF, which we compute from the prompts in the dataset. This is a fairly scalable and fast implementation of search. Our image search feature uses OpenAI’s open source CLIP vision transformer embeddings. There’s a one-time fixed cost of indexing all of the image embeddings for search, but otherwise search is fairly scalable afterwards by using a full dot-product search. When scaling up, we may revisit this and switch to an approximate nearest neighbors approach like LSH or HNSW. In order to mine common descriptive phrases in search results that users may filter by, we employ the NLTK library and use it to tag style words and surface them as a bar chart to the user. 

Modern AI image generation uses large pretrained models to generate a unique image from a variety of data types, but most commonly a supplied text prompt [2]; this type of system is new to many users, who are still learning how to interact with them effectively [3], [4]. The quality of images that these models generate is dependent on the text input. Thus, prompt engineering and shortening the feedback loop with users is essential for accurate results [5], [6]. Prompt engineering is difficult due to model complexities which can yield unpredictable results, as well as the subjective nature of determining the quality of the images produced. Existing solutions to the problem of prompt engineering for image generation have severe limitations. Most of these techniques require very expensive and time-intensive processes including training machine learning models [5], designing clever methods for evaluating generated image quality, and hand labeling examples using human feedback [7]; furthermore, these are all driven almost exclusively by trial-and-error [8]. While these approaches are effective, they only benefit users with ample technical knowledge and resources. Most of these approaches do not efficiently take advantage of the fact that a significant increase in generated image quality can be gained by simply including the correct stylistic keywords in an image prompt [9], [10].

Our approach allows users to directly engage with DiffusionDB [11], a dataset of Stable Diffusion prompt and image pairs. We use DiffusionDB over other AI image datasets such as TWIGMA [12] due to its scale, quality, and availability. Some approaches generate descriptions from images, but face challenges with the complexity of visual question answering (VQA) models; therefore, we do not explore this further in our approach [13]. Instead, we allow users to explore DiffusionDB, using the collective knowledge of the community to interactively demonstrate options for improving image generation prompts. This combination of hands-on interaction, simplicity, and community input sets our approach apart in making prompt creation more straightforward and accessible for everyone. Recent systems like PromptMagician [14] make progress in this domain, but have little traction with the image generation community. 

Prompt Explorer sets itself apart from other prompt engineering tools in the AI community by: 
- Crowd-sourcing prompt engineering using a large dataset and interactive visualizations.
- Allowing users to start to search via a prompt or an image; this significantly enhances usability by allowing users to find images similar to their base image or style. Based on literature research, we’re trying to solve known feedback where users don’t know where to begin with their prompt [3]. It will encourage the user to explore proven techniques like stylistic modifiers but not negative qualifiers as we don’t have negative qualifiers in our dataset [15], [8].
- Facilitating interactive exploration of prompt keywords by filtering prompts by style words which allows the user to see what other images in the dataset are similar to your input. 
- Automatic tagging of stylistic keywords in image generation prompts.

## INSTALLATION
1. Set up a Python virtual environment in one of the following ways:
    - **Using venv**:
        - **For Windows**:
            ```
            python -m venv venv
            venv\Scripts\activate
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
3. Run `python3 get_data.py` to download the dataset.

## EXECUTION 
1. Run `python3 app.py` to run the web app.
2. Navigate to [http://127.0.0.1:8050/](http://127.0.0.1:8050/) to view it in your browser.

## DEMO VIDEO
Here's a demo video of how to get the project running locally for the smaller dataset: https://youtu.be/83tkIujtr_Q?si=HoxtxoOuKLga41GW

For the larger dataset, simply swap our the parameter in the `get_data.py` file.
---
## Final Project
This repository contains code related to the final project of
[CSE 6242: Data and Visual Analytics](https://omscs.gatech.edu/cse-6242-data-visual-analytics).

---
## Documents
- [Project Proposal](https://docs.google.com/document/d/1DTW47zXW2rzbVkHM4GLeFzOclJOMAuph4Z5-gXX5k5c/edit)
- [Progress Report](https://docs.google.com/document/d/1nrmMg8YSDYFV3myOLY-BGLmvsR97cLks/edit)
- [Final Report](UPLOAD URL HERE)
- [Final POSTer](UPLOAD URL HERE)

---
## Links
- [Project Description](https://docs.google.com/document/d/e/2PACX-1vSlYrMw402tL3F95ay-AaptTdF80UOER-gne_O0kqbuuk6WXrlsjwaYjjS0Jyl95dXYyDLjh9DR1mln/pub)
- [Project Drive](https://drive.google.com/drive/folders/1tlR_83Kof5RTz8a66ZOJtygNr57252UU)
- [DiffusionDB](https://github.com/poloclub/diffusiondb)
