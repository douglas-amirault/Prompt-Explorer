import json
from tqdm import tqdm


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

    def __iter__(self):
        for item in self.items:
            yield item
