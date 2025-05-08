from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

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

if __name__ == '__main__':

    img_path = r'Add file path here'
    ic = ImageCaption()
    caption = ic.generate(img_path)

    print("Caption of the image: ", caption)