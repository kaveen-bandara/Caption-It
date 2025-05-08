from flask import Flask, request, render_template, jsonify
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import io

app = Flask(__name__)

class ImageCaption:

    def __init__(self):
        self.processor = BlipProcessor.from_pretrained('Salesforce/blip-image-captioning-base')
        self.model = BlipForConditionalGeneration.from_pretrained('Salesforce/blip-image-captioning-base')

    def generate(self, img):
        if isinstance(img, str):
            img = Image.open(img)

        text = "This image shows "
        input = self.processor(img, text, return_tensors = 'pt')
        output = self.model.generate(**input)
        caption = self.processor.decode(output[0], skip_special_tokens = True)
        
        return caption
    
ic = ImageCaption()

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/caption', methods = ['POST'])
def caption():
    file = request.files['image']
    image = Image.open(io.BytesIO(file.read())).convert('RGB')
    caption = ic.generate(image)
    return jsonify({'caption': caption})

if __name__ == '__main__':
    app.run(debug = True)