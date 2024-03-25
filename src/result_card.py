from dash import html
import base64

styles = {
    "result-card": {
        "display": "flex", 
        "flex-direction": "row", 
        "border": "1px solid #808080",
        "padding": "10px",
        "margin": "10px 0",
        "width": "95.7%",
        "border-radius": "10px",
        "justify-content": "space-between",
         "margin-right": "10px"
    },
    
    "result-image": {
        "max-width": "30%", 
        "max-height": "200px", 
        "display": "inline"    
    },
    
    "result-description": {
        "textAlign": "left", 
        "display": "inline", 
        "background-color": "#f2f2f2", 
        "width": "50%", 
        "padding": "10px",
        "border-radius": "10px",
        "font-family": "Arial, sans-serif"
    },

    "result-title": {
        "margin-top": "0px",
        "font-family": "Arial, sans-serif"

    }
}


def create_result_card(image_url, description):
    with open(image_url, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        encoded_image = f"data:image/png;base64,{encoded_image}"
    return html.Div(
        className="result-card",
        children=[
            html.Img(
                src=encoded_image,
                alt=description,
                className="result-image",
                style=styles["result-image"],
            ),
            html.Div(
                children=[
                    html.H3("Prompt", className="result-title", style=styles["result-title"]),
                    html.P(description, className="result-description"),
                ],
                style=styles["result-description"],
            ),
        ],
        style=styles["result-card"],
    )
