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
    style={"display": "flex", "text-align": "center", "margin": "auto", "width": "70%"},
)

image_search_button = dcc.Upload(
    id="upload-image",
    children=html.Button("📸", style={"width": "50px"}),
    accept="image/*",
    style={"display": "flex", "width": "50px"},
)

logo = html.Img(src="/assets/logo.png", style={"height": "50px", "margin-right": "10px", "padding-left": "20px"})

prompt_insights = html.Div(
    [html.H3("Prompt Analysis", style={"margin-left": "10px", "font-size": "15px", "font-family": "Arial, sans-serif"})],
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
)

insights = html.Div(
    [dcc.Graph(id="histogram")],
    style={
        "width": "100%",
        "height": "calc(100vh - 120px)",
        "margin": "10px 0",
        "padding": "10px",
        "border": "1px solid #808080",
        "box-sizing": "border-box",
        "border-radius": "10px",
        "background-color": "#f2f2f2"
    }
)

app.layout = html.Div([
    html.Div(
        [logo, html.H1("Crowdsource AI", style={"margin-left": "10px", "font-family": "Arial, sans-serif"})],
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
    html.Div([
        html.Div(
            [html.H3("Input Prompt", style={"margin-left": "10px", "font-size": "15px", "font-family": "Arial, sans-serif"}), text_search_bar, image_search_button],
            style={
                "justify-content": "space-between",
                "align-items": "center",
                "width": "50%",
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
        html.Div(
            [prompt_insights],
            style={
                "display": "flex",
                "flex-direction": "column",
                "align-items": "flex-end",
                "width": "50%"
            }
        )
    ],
        style={
            "display": "flex", 
            "justify-content": "space-between",
            "width": "100%"
        }
    ),

    html.Div([
        html.Div(
            html.Div(id="search-results", style={"overflow": "auto", "height": "100vh", "width": "100%"}), 
            style={
                "width": "50%",  
                "margin-right": "5px"
            }
        ),
        html.Div(
            [insights],
            style={
                "width": "50%", 
                "margin-left": "5px"
            }
        ),
    ],
        style={
            "display": "flex",
            "justify-content": "space-between",
        },
    ),
])

@app.callback(
    [
        Output("search-results", "children"),
        Output("histogram", "figure"),
        Output("text-search", "value"),
        Output("upload-image", "contents"),
    ],
    [Input("text-search", "value"), Input("upload-image", "contents")],
)

def search(search_term, image):
    if image:
        results_list, histogram_data = image_search(image)
        return results_list, histogram_data, "", ""
    elif search_term:
        results_list, histogram_data = text_search(search_term)
        return results_list, histogram_data, search_term, ""
    else:
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
