from dash import html
import base64
import string

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
        "padding": "1px",
        "border-radius": "10px",
        "font-family": "Arial, sans-serif"
    },

    "result-title": {
        "margin-top": "0px",
        "padding": "2px",
        "font-family": "Arial, sans-serif"
    },

    "adjective": {
        "color": "blue"
    }
}

def format_description(tagged):
    formatted_description = []
    for i, (word, tag) in enumerate(tagged):
        if tag.startswith("JJ"):
            word_span = html.Span(word, style=styles["adjective"])
        else:
            word_span = html.Span(word)
        
        formatted_description.append(word_span)

        if i < len(tagged) - 1:
            next_word, next_tag = tagged[i + 1]
            if next_word not in string.punctuation:
                formatted_description.append(" ")

    return html.P(formatted_description, className="result-description", style=styles["result-description"])

def create_result_card(image_url, description, tagged):
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
                    format_description(tagged)
                ],
                style=styles["result-description"],
            ),
        ],
        style=styles["result-card"],
    )
