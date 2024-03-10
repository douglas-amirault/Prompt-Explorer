import datasets
import json
import os
from tqdm import tqdm

class DataLoader:

    def __init__(self, dataset_name, split_name, set_name="train"):
        self.dataset_name = dataset_name
        self.split_name = split_name
        self.set_name = set_name
        self.ds = datasets.load_dataset(dataset_name, split_name, set_name, streaming=True)
        for folder in ["./dataset", "./images"]:
            if not os.path.exists(folder):
                os.mkdir(folder)
        
    def download_dataset(self, max_examples=1000):
        found_prompts = set()
        with open("./dataset/examples.jsonl", "w") as json_file:
            for idx, item in tqdm(enumerate(self.ds['train'])):
                if item["prompt"] in found_prompts:
                    continue
                found_prompts.add(item["prompt"])
                item["image"].save(
                    f"./images/{idx}.jpg", format="JPEG", quality=20, subsampling=1
                )
                json_file.write(
                    json.dumps({
                        "prompt": item["prompt"], "image": f"./images/{idx}.jpg"
                    }) + "\n"
                )
                if len(found_prompts) >= max_examples:
                    break
    
