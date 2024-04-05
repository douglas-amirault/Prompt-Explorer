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
                    if "8 k" in prompt_lower:
                        item["prompt"] = item["prompt"].replace("8 k", "8K")
                    if "4 k" in prompt_lower:
                        item["prompt"] = item["prompt"].replace("4 k", "4K")
                    if "3 d" in prompt_lower:
                        item["prompt"] = item["prompt"].replace("3 d", "3D")
                    if "1 6 k" in prompt_lower:
                        item["prompt"] = item["prompt"].replace("1 6 k", "16K")
                    if "2 d" in prompt_lower:
                        item["prompt"] = item["prompt"].replace("2 d", "2D")
                    if "3 2 k" in prompt_lower:
                        item["prompt"] = item["prompt"].replace("3 2 k", "32K") 
                    if "y 2 k" in prompt_lower:
                        item["prompt"] = item["prompt"].replace("y 2 k", "Y2K") 

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
            for prompt in [m["prompt"] for m in self.items]
            for word, tag in pos_tag(word_tokenize(prompt))
            if tag.startswith("JJ")
        ]
        common_adjs = Counter(adjectives).most_common(num_adjs)
        data = {
            "x": [count for adj, count in common_adjs][::-1],
            "y": [adj for adj, count in common_adjs][::-1],
            "type": "bar",
            "orientation": "h",
        }
        histogram_data = {
            "data": [data],
            "layout": {
                "title": "Most Common Adjectives (Global)",
                "xaxis": {"title": "Count", "fixedrange": True},
                "yaxis": {"fixedrange": True},
            },
        }
        return histogram_data
