from flask import Flask, request, render_template, jsonify
from PIL import Image, UnidentifiedImageError
from transformers import BlipProcessor, BlipForConditionalGeneration
import io

app = Flask(__name__)

# limit upload size to 5 MB
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# only these file extensions are allowed for security
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    if 'image' not in request.files:
        return jsonify({'error': 'No image file part in request'}), 400
    
    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        image = Image.open(io.BytesIO(file.read())).convert('RGB')
    except UnidentifiedImageError:
        return jsonify({'error': 'Invalid image file'}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to process image: {str(e)}'}), 500
    
    try:
        caption = ic.generate(image)
        return jsonify({'caption': caption})
    except Exception as e:
        return jsonify({'error': f'Caption generation failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug = True)