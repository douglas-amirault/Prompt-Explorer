import dash
from dash import dcc, html, Input, Output, State, ALL
from dash.exceptions import PreventUpdate
from src.result_card import create_result_card
from src.dataset import Dataset
from src.search_engine import SearchEngine
from PIL import Image
import os
import io
import base64
import re
import json

max_results = 10

THIS_DIR = os.path.abspath(".")
blank_graph = {
    "data": [{"x": [], "y": [], "type": "bar", "orientation": "h"}],
    "layout": {"xaxis": {"fixedrange": True}, "yaxis": {"fixedrange": True}},
}

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
        dcc.Store(id='current-results-store'),
        dcc.Store(id='selected-adjectives-store', data=[]),
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
                "margin-right": "10px",
            },
        ),
        html.Div(
            [
                html.Div(
                    id="search-results",
                    style={"overflow": "auto", "width": "50%", "height": "100vh"},
                ),
                html.Div(
                    [
                        html.Div(id="filters-container", style={"margin": "20px"}),
                        dcc.Graph(id="histogram-global", figure=dataset.adjs),
                        dcc.Graph(id="histogram", figure=blank_graph),
                    ],
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "width": "50%",
                    },
                ),
            ],
            style={"display": "flex", "justify-content": "space-between"},
        ),
    ]
)


@app.callback(
    [
        Output("search-results", "children"),
        Output("histogram", "figure"),
        Output("text-search", "value"),
        Output("current-results-store", "data"),
        Output("selected-adjectives-store", "data"),
        Output("upload-image", "contents")
    ],
    [
        Input("text-search", "value"),
        Input("upload-image", "contents"),
        Input("histogram", "clickData"),
        Input("histogram-global", "clickData"),
        Input({"type": "remove-filter", "adjective": ALL}, "n_clicks"),
    ],
    [State("current-results-store", "data"),
        State("selected-adjectives-store", "data")],
)

def search(
    search_term,
    image,
    click_data,
    click_data_global,
    _,
    current_results,
    selected_adjectives,
):
    ctx = dash.callback_context
    triggered_id, triggered_prop_id = ctx.triggered[0]["prop_id"].split(".") if ctx.triggered else ("", "")

    # IMAGE UPLOAD LOGIC
    if triggered_id == "upload-image" and image:
        results, result_cards, histogram_data = image_search(image)
        return result_cards, histogram_data, "", results, [], ""

    # HANDLE REMOVAL OF FILTERS
    elif "remove-filter" in triggered_id:

        # ID adjective to be remove, update list of selected adjectives
        adj_to_remove = json.loads(triggered_id)['adjective']
        updated_adjectives = [
            adj for adj in selected_adjectives if adj != adj_to_remove
        ]

        # Instead of caching results, it will easier for our purposes to just rerun the search
        current_results, _, _ = text_search(search_term)

        # Update the current_results
        if not updated_adjectives:  # Checks if updated_adjectives list is empty
            filtered_results = current_results
        else:
            filtered_results = [
                result
                for result in current_results
                if any(adj in result["prompt"] for adj in updated_adjectives)
            ]


        # Filtered result cards
        result_cards = [
            create_result_card(os.path.join(THIS_DIR, item["image"]), item["prompt"])
            for item in filtered_results[:max_results]
        ]

        # Filtered histogram data
        histogram_data = search_engine.get_histogram_data(filtered_results)

        # Return updated state
        return (result_cards, histogram_data, search_term, filtered_results, updated_adjectives, None)

    # HISTOGRAM AND FILTER CLICK LOGIC
    elif triggered_id in ["histogram", "histogram-global"] and (
        click_data or click_data_global
    ):
        clicked_adjective = (
            click_data["points"][0]["y"]
            if triggered_id == "histogram"
            else click_data_global["points"][0]["y"]
        )
        if clicked_adjective not in selected_adjectives:
            selected_adjectives.append(clicked_adjective)
        filtered_results = [result for result in current_results if clicked_adjective in result['prompt']]
        result_cards = [
            create_result_card(os.path.join(THIS_DIR, item["image"]), item["prompt"])
            for item in filtered_results[:max_results]
        ]
        histogram_data = search_engine.get_histogram_data(filtered_results)
        return result_cards, histogram_data, search_term, filtered_results, selected_adjectives, None

    # TEXT SEARCH LOGIC
    elif triggered_id == "text-search":
        current_results, result_cards, histogram_data = text_search(search_term)
        print()
        return result_cards, histogram_data, search_term, current_results, [], None

    # NULL CASE
    return [], blank_graph, "", [], "", None


def text_search(search_term):
    if not search_term:
        return None, [], blank_graph

    # Filter data based on search term (case-insensitive)
    results, histogram_data = search_engine.get_matching_results(search_term)

    # Display results
    if len(results) == 0:
        return None, "No results found.", blank_graph

    result_cards = [
        create_result_card(os.path.join(THIS_DIR, item["image"]), item["prompt"])
        for item in results[:max_results]
    ]
    return results, result_cards, histogram_data


def image_search(image):
    # Cleanup tags before base64 data
    image = re.sub("^data:image/.+;base64,", "", image)
    # Load as PIL image so we can embed it
    loaded_image = Image.open(io.BytesIO(base64.b64decode(image)))
    # Do image search
    results, histogram_data = search_engine.search_for_image(loaded_image)

    if len(results) == 0:
        return "No results found.", blank_graph

    result_cards = [
        create_result_card(os.path.join(THIS_DIR, item["image"]), item["prompt"])
        for item in results[:max_results]
    ]

    return results, result_cards, histogram_data


@app.callback(
        Output('filters-container', 'children'),
        [Input('selected-adjectives-store', 'data')]
)
def update_display(store_data):
    # Check if store_data is not empty
    if store_data:
        # Create a div for each filter
        return html.Div(
            [
                html.Div(
                    [
                        html.Span(adjective),
                        html.Button(
                            "X", id={"type": "remove-filter", "adjective": adjective}
                        ),
                    ],
                    style={
                        "display": "flex",
                        "align-items": "center",
                        "margin": "5px",
                        "padding": "5px 10px",  # Add padding inside the box
                        "font-family": "Arial, sans-serif",
                        "background-color": "#f0f0f0",  # Light grey background
                        "border-radius": "15px"  # Rounded edges
                        #"box-shadow": "0 2px 4px rgba(0,0,0,0.1)",  # Optional: add a subtle shadow for depth
                    },
                )
                for idx, adjective in enumerate(store_data)
            ],
            style={
                "display": "flex",
                "justify-content": "center",
                "flex-direction": "row",
                "align-items": "left",
            },
        )
    else:
        # Return a message indicating no filters selected
        return html.Div(
            "No filters selected",
            style={
                "margin": "20px",
                "color": "#777",
                "font-family": "Arial, sans-serif",
                "text-align": "center"
            },
        )


if __name__ == "__main__":
    app.run_server(debug=True)
