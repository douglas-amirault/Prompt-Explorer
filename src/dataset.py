import json
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
                    self.items.append(json.loads(line))
                except:
                    break
        print(f"LOADED: {len(self.items)} EXAMPLES")
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
            "orientation": "h"
        }
        histogram_data = {
            "data": [data],
            "layout": {
                "title": "Most Common Adjectives (Global)",
                "xaxis": {"title": "Count", "fixedrange": True},
                "yaxis": {"fixedrange": True}
            }
        }
        return histogram_data
