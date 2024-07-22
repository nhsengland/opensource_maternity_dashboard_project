import os
import base64
from dash import Dash, html

app = Dash(__name__)

# Get the list of PNG file paths in the 'prelim-charts' folder
image_folder = "prelim_charts/ALL SUBMITTERS"
image_paths = [
    os.path.join(image_folder, f)
    for f in os.listdir(image_folder)
    if f.endswith(".png")
]

# Encode the PNG images as base64 strings
encoded_images = []
for image_path in image_paths:
    with open(image_path, "rb") as file:
        encoded_image = base64.b64encode(file.read()).decode("utf-8")
        encoded_images.append(encoded_image)

# Define the app layout
app.layout = html.Div(
    [
        html.H1("Image Gallery"),
        *[
            html.Img(
                src=f"data:image/png;base64,{encoded_image}",
                style={"maxWidth": "100%", "height": "auto"},
            )
            for encoded_image in encoded_images
        ],
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
