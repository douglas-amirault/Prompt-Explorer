import dash
from dash import dcc, html, Input, Output, State
from src.result_card import create_result_card
from src.dataset import Dataset
from src.search_engine import SearchEngine
from PIL import Image
import os
import io
import base64
import re


THIS_DIR = os.path.abspath(".")
blank_graph = {"data": [{"x": [], "y": [], "type": "bar"}], "layout": {"xaxis": {"fixedrange": True}, "yaxis": {"fixedrange": True}}}

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
                "margin-right": "10px"
            },
        ),
        html.Div(id="search-results", style={"overflow": "auto", "height": "100vh"}),
    ]
)


@app.callback(
    [
        Output("search-results", "children"),
        Output("histogram", "figure"),
        Output("text-search", "value"),
        Output("upload-image", "contents"),
    ],
    [
        Input("text-search", "value"),
        Input("upload-image", "contents"),
        Input("histogram", "clickData")
    ],
    [
        State("text-search", "value")
    ]
)

def search(search_term, image, click_data, current_search_term):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else ""

    if triggered_id == "upload-image" and image:
        results_list, histogram_data = image_search(image)
        return results_list, histogram_data, "", ""

    elif triggered_id == "histogram" and click_data:
        clicked_adjective = click_data["points"][0]["x"]
        new_search_term = f"{current_search_term} {clicked_adjective}".strip()
        results_list, histogram_data = text_search(new_search_term)
        return results_list, histogram_data, new_search_term, ""

    elif triggered_id == "text-search":
        results_list, histogram_data = text_search(search_term)
        return results_list, histogram_data, search_term, ""

    return [], blank_graph, "", ""


def text_search(search_term):
    if not search_term:
        return []

    # Filter data based on search term (case-insensitive)
    results, histogram_data = search_engine.get_matching_results(search_term)

    # Display results
    if len(results) == 0:
        return "No results found.", blank_graph

    results_list = [
        create_result_card(os.path.join(THIS_DIR, item["image"]), item["prompt"])
        for item in results
    ]
    return results_list, histogram_data


def image_search(image):
    # Cleanup tags before base64 data
    image = re.sub("^data:image/.+;base64,", "", image)
    # Load as PIL image so we can embed it
    loaded_image = Image.open(io.BytesIO(base64.b64decode(image)))
    # Do image search
    results, histogram_data = search_engine.search_for_image(loaded_image)

    if len(results) == 0:
        return "No results found.", blank_graph

    results_list = [
        create_result_card(os.path.join(THIS_DIR, item["image"]), item["prompt"])
        for item in results
    ]

    return results_list, histogram_data


if __name__ == "__main__":
    app.run_server(debug=True)
