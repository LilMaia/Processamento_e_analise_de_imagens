from PIL import Image

class ImageInfo:
    def __init__(self):
        self.image_tk : Image = None
        self.image_resized : Image = None
        self.img_original : Image  = None
        self.image : Image = None