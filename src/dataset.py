import json
import re
from tqdm import tqdm
from collections import Counter
from nltk import word_tokenize, pos_tag


class Dataset:

    def __init__(self, data_path):
        print("LOADING DATASET")
        self.items = []
        with open("./dataset/examples.jsonl", "r") as json_file:
            for line in tqdm(json_file):
                try:
                    item = json.loads(line)
                    prompt_lower = item["prompt"].lower()

                    replacements = {
                        "8 k": "8K",
                        "4 k": "4K",
                        "3 d": "3D",
                        "1 6 k": "16K",
                        "2 d": "2D",
                        "3 2 k": "32K",
                        "y 2 k": "Y2K"
                    }

                    for key, value in replacements.items():
                        if key in prompt_lower:
                            item["prompt"] = item["prompt"].replace(key, value)

                    item["prompt"] = re.sub(r'(\d) (\d) (\d) (\d)', r'\1\2\3\4', item["prompt"])
                    item["prompt"] = re.sub(r'(\d) (\d) (\d)', r'\1\2\3', item["prompt"])
                    item["prompt"] = re.sub(r'(\d) (\d)', r'\1\2', item["prompt"])
                    
                    item["prompt"] = re.sub(r'(\d) th', r'\1th', item["prompt"])
                    item["prompt"] = re.sub(r'(\d) nd', r'\1nd', item["prompt"])
                    item["prompt"] = re.sub(r'(\d) s', r'\1s', item["prompt"])
                    item["prompt"] = re.sub(r'(\d) mm', r'\1mm', item["prompt"])

                    self.items.append(item)
                except:
                    break
        print(f"LOADED: {len(self.items)} EXAMPLES")
        print("PREPROCESSING DATASET...")
        for idx in tqdm(range(len(self.items))):
            self.items[idx]["tagged"] = pos_tag(
                word_tokenize(self.items[idx]["prompt"])
            )
        print("DONE")
        self.adjs = self.get_global_adjectives()

    def __iter__(self):
        for item in self.items:
            yield item

    def get_global_adjectives(self, num_adjs=8):
        adjectives = [
            word
            for result in [m for m in self.items]
            for word, tag in result["tagged"]
            if tag.startswith("JJ")
        ]
        common_adjs = Counter(adjectives)
        common_adjs = common_adjs.most_common(num_adjs)
        data = {
            "x": [count for adj, count in common_adjs][::-1],
            "y": [adj for adj, count in common_adjs][::-1],
            "type": "bar",
            "orientation": "h",
        }
        histogram_data = {
            "data": [data],
            "layout": {
                "title": {
                    "text": "Most Common Adjectives (Global)",
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top",
                },
                "margin": {
                    "t": 45,
                    "b": 45,
                },
                "xaxis": {"title": "Count", "fixedrange": True},
                "yaxis": {"fixedrange": True},
                "paper_bgcolor":'rgba(0,0,0,0)',
                "plot_bgcolor":'rgba(0,0,0,0)', 
            },
        }
        return histogram_data
