import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Route to display the form and handle the image generation
@app.route("/", methods=["GET", "POST"])
def generate_image():
    if request.method == "POST":
        prompt = request.form["prompt"]
        
        # Image details (can be adjusted based on the form inputs or logic)
        width = 512
        height = 512
        seed = 1  # Each seed generates a new image variation
        model = 'flux'  # Default model
        
        # Format the URL for the API request
        image_url = f"https://pollinations.ai/p/{prompt}?width={width}&height={height}&seed={seed}&model={model}"
        
        try:
            # Download the image from the URL
            response = requests.get(image_url)
            response.raise_for_status()  # Check if the request was successful
            
            # Save the image locally
            image_path = 'static/generated_image.jpg'
            with open(image_path, 'wb') as file:
                file.write(response.content)
            
            # Return the image URL to be displayed on the HTML page
            return render_template("index.html", image_url=image_path, prompt=prompt)
        
        except requests.exceptions.RequestException as e:
            # Handle errors (e.g., connection issues, invalid prompt)
            return render_template("index.html", error=f"Error generating image: {e}")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
