from flask import Flask, render_template, request
import json
from tqdm import tqdm
import os
from flask import url_for, send_file
import base64

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

def get_matching_results(prompt, max_res=10):
    return [x for x in dataset if prompt in x["prompt"]][:max_res]
        

@app.route("/search/<prompt>")
def search(prompt):
    results = get_matching_results(prompt)
    for result in results:
        with open(result['image'], "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            result['encoded_image'] = f"data:image/png;base64,{encoded_image}"
    return render_template("results.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
