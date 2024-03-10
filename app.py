import os

import base64
from flask import Flask, render_template, request
import json
import spacy
from tqdm import tqdm

app = Flask(__name__, template_folder="templates")

dataset = []
print("LOADING DATASET...")
with open("./dataset/examples.jsonl", "r") as json_file:
    for line in tqdm(json_file):
        try:
            dataset.append(json.loads(line))
        except:
            break
print(f"LOADED: {len(dataset)} EXAMPLES")

nlp = spacy.load("en_core_web_lg")

def get_matching_results(query, max_res=10):
    query_doc = nlp(query)
    query_sig_words = {token.text.lower() for token in query_doc if token.pos_ in ["NOUN", "VERB", "ADJ", "PROPN", "ADV"]}

    # filter to prompts with at least one matching 'significant' word to the query for efficiency
    if len(query_sig_words) != 0:
        filtered_dataset = [x for x in dataset if any(w in x["prompt"].lower() for w in query_sig_words)]
    else:
        filtered_dataset = dataset

    scores = [(x, query_doc.similarity(nlp(x["prompt"]))) for x in filtered_dataset]
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    result = [x[0] for x in sorted_scores][:max_res]

    return result
        
@app.route("/search/<query>")
def search(query):
    results = get_matching_results(query)
    for result in results:
        with open(result['image'], "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            result['encoded_image'] = f"data:image/png;base64,{encoded_image}"
    return render_template("results.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
