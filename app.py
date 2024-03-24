import dash
from dash import dcc, html, Input, Output
from src.result_card import create_result_card
from src.dataset import Dataset
from src.search_engine import SearchEngine
from PIL import Image
import os
import io
import base64
import re


THIS_DIR = os.path.abspath(".")

print("LOADING DATASET...")
dataset = Dataset("./dataset/examples.jsonl")
search_engine = SearchEngine(
    dataset.items, embs_loc=os.path.join(THIS_DIR, "resources", "embs.pkl")
)

app = dash.Dash(__name__)

text_search_bar = dcc.Input(
    id="text-search",
    type="text",
    placeholder="Enter search string here...",
    debounce=True,
    style={
        "display": "flex",
        "text-align": "center",
        "margin": "auto",
        "width": "100%",
    },
)

image_search_button = dcc.Upload(
    id="upload-image",
    children=html.Button("📸", style={"width": "50px"}),
    accept="image/*",
    style={"display": "flex", "width": "50px"},
)


app.layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "Prompt Explorer",
                    style={"margin-left": "10px", "font-family": "Arial, sans-serif"},
                )
            ],
            style={
                "display": "flex",
                "align-items": "center",
                "width": "100%",
                "height": "50px",
                "background-color": "#ffd700",
                "border": "2px solid #000",
                "box-sizing": "border-box",
                "border-radius": "10px",
            },
        ),
        html.Div(
            [
                html.H3(
                    "Input Prompt",
                    style={
                        "margin-left": "10px",
                        "font-size": "15px",
                        "font-family": "Arial, sans-serif",
                    },
                ),
                text_search_bar,
                image_search_button,
            ],
            style={
                "justify-content": "space-between",
                "align-items": "center",
                "width": "100%",
                "height": "50px",
                "margin": "10px 0",
                "padding": "10px",
                "border": "1px solid #808080",
                "box-sizing": "border-box",
                "border-radius": "10px",
                "display": "flex",
            },
        ),
        html.Div(id="search-results", style={"overflow": "auto", "height": "100vh"}),
    ]
)


@app.callback(
    [
        Output("search-results", "children"),
        Output("text-search", "value"),
        Output("upload-image", "contents"),
    ],
    [Input("text-search", "value"), Input("upload-image", "contents")],
)
def search(search_term, image):
    if image:
        return image_search(image), "", ""
    elif search_term:
        return text_search(search_term), search_term, ""
    else:
        return [], "", ""


def text_search(search_term):
    if not search_term:
        return []

    # Filter data based on search term (case-insensitive)
    filtered_data = search_engine.get_matching_results(search_term)

    # Display results
    if len(filtered_data) == 0:
        return "No results found."

    results_list = [
        create_result_card(os.path.join(THIS_DIR, item["image"]), item["prompt"])
        for item in filtered_data
    ]
    return results_list


def image_search(image):
    # Cleanup tags before base64 data
    image = re.sub("^data:image/.+;base64,", "", image)
    # Load as PIL image so we can embed it
    loaded_image = Image.open(io.BytesIO(base64.b64decode(image)))
    # Do image search
    results = search_engine.search_for_image(loaded_image)

    if len(results) == 0:
        return "No results found."

    results_list = [
        create_result_card(os.path.join(THIS_DIR, item["image"]), item["prompt"])
        for item in results
    ]

    return results_list


if __name__ == "__main__":
    app.run_server(debug=True)
