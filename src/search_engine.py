from sklearn.feature_extraction.text import TfidfVectorizer
from .image_processor import ImageProcessor
import numpy as np
from collections import Counter
from tqdm import tqdm
from PIL import Image
from nltk import word_tokenize, pos_tag
import os
import joblib


class SearchEngine:

    def __init__(self, items, embs_loc="embs.pkl"):
        self.items = items
        self.embs_loc = embs_loc
        self.vectorizer = TfidfVectorizer()
        self.dataset_tfidf = self.vectorizer.fit_transform([x["prompt"] for x in items])
        self.image_processor = ImageProcessor()
        self.image_embeddings = self.index_images()

    def index_images(self):
        if os.path.exists(self.embs_loc):
            return joblib.load(self.embs_loc)
        buffer = []
        buffer_size = 32
        out = []
        print("EMBEDDING IMAGES")
        for item in tqdm(self.items):
            buffer.append(Image.open(item["image"]))
            if len(buffer) == buffer_size:
                images = self.image_processor.embed_images(buffer)
                out.extend(images)
                buffer = []
        if buffer:
            images = self.image_processor.embed_images(buffer)
            out.extend(images)
        print("DONE")
        out = np.asarray(out)
        joblib.dump(out, self.embs_loc)
        return out

    def get_histogram_data(self, matching_results, num_adjs=8):
        adjectives = [
            word
            for result in [m for m in matching_results]
            for word, tag in result["tagged"]
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
                "title": "Most Common Adjectives",
                "xaxis": {"title": "Count", "fixedrange": True},
                "yaxis": {"fixedrange": True},
                "paper_bgcolor":'rgba(0,0,0,0)',
                "plot_bgcolor":'rgba(0,0,0,0)', 
            },
        }
        return histogram_data

    def get_matching_results(self, query, selected_adjectives=[], threshold=0, max_results=10):
        vec = self.vectorizer.transform([query])
        search_res = self.dataset_tfidf.dot(vec.T)
        scores = search_res[:, 0].toarray().flatten()
        valid_results = [(idx, x) for idx, x in enumerate(scores) if x > threshold]
        out_inds = [
            x[0] for x in sorted(valid_results, reverse=True, key=lambda x: x[1])
        ]
        matching_results = [self.items[ind] for ind in out_inds]
        filtered_results = [result for result in matching_results if len(selected_adjectives==0) or all(adjective in result["prompt"] for adjective in selected_adjectives)]
        histogram_data = self.get_histogram_data(filtered_results)
        return filtered_results[:max_results], histogram_data

    def search_for_image(self, image, selected_adjectives=[], threshold=25, max_results=10):
        image_embedding = self.image_processor.embed_images([image])
        dot_products = np.dot(image_embedding, self.image_embeddings.T).flatten()
        valid_results = [
            (idx, x) for idx, x in enumerate(dot_products) if x > threshold
        ]
        out_inds = [
            x[0] for x in sorted(valid_results, reverse=True, key=lambda x: x[1])
        ]
        matching_results = [self.items[ind] for ind in out_inds]
        filtered_results = [result for result in matching_results if len(selected_adjectives)==0 or all(adjective in result["prompt"] for adjective in selected_adjectives)]
        histogram_data = self.get_histogram_data(filtered_results)
        return filtered_results[:max_results], histogram_data
