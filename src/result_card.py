from dash import html
import base64

styles = {
    "result-image": {"max-width": "30%", "display": "inline"},
    "result-description": {"textAlign": "center", "display": "inline"},
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
                description,
                className="result-description",
                style=styles["result-description"],
            ),
        ],
        style=styles,
    )
