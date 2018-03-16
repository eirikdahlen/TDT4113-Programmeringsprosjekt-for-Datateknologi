import os
path = "C:\\Users\eirik\PycharmProjects\Høst2017\ProgProsjekt\Oving5\imager\imager\images"
os.chdir(path)

from PIL import Image, ImageEnhance, ImageOps, ImageFilter

class Artwork:

    def __init__(self, path1, path2, path3):
        self.path1 = path1
        self.path2 = path2
        self.path3 = path3

        self.image1 = Image.open(path1)
        self.image2 = Image.open(path2)
        self.image3 = Image.open(path3)

        self.listofimages = []

    def blur(self, image):
        blured = image.filter(ImageFilter.BLUR)
        return blured

    def rotate(self, degrees, image):
        rotated = image.rotate(degrees)
        return rotated

    def change_exposure(self, amount, image):
        exposured = image.point(lambda x: x * amount)
        return exposured

    def change_contrast(self, amount, image):
        contrasted = ImageEnhance.Contrast(image).enhance(amount)
        return contrasted

    def make_it_grey(self, image):
        gray = image.convert('LA')
        return gray

    def invert_colors(self, image):
        inverted = ImageOps.invert(image)
        return inverted

    def add_to_list(self, image):
        self.listofimages.append(image)


    def create_collage(self, width = 300, height=70):
        cols, rows = 3, 2

        thumbnail_width = width//cols
        thumbnail_height = height//rows
        size = thumbnail_width, thumbnail_height

        collage = Image.new('RGB', (width, height))
        images = []
        for im in self.listofimages:
            im.thumbnail(size)
            images.append(im)
        i = 0
        x = 0
        y = 0
        for col in range(cols):
            for row in range(rows):
                collage.paste(images[i], (x, y))
                i += 1
                y += thumbnail_height
            x += thumbnail_width
            y = 0

        collage.save('collage.jpeg')
        collage = Image.open('collage.jpeg')
        collage.show()

def main():
    imo1 = 'arduino.jpeg'
    imo2 = 'fibonacci.jpeg'
    imo3 = 'northernlights.jpeg'

    artist = Artwork(imo1,imo2,imo3)

    # Første bilde
    im1 = artist.change_contrast(3, artist.image1)
    im1 = artist.rotate(90, im1)
    artist.add_to_list(im1)

    # Andre bilde
    im2 = artist.change_exposure(0.5, artist.image2)
    im2 = artist.change_contrast(5, im2)
    artist.add_to_list(im2)

    #Tredje bilde
    im3 = artist.make_it_grey(artist.image3)
    im3 = artist.blur(im3)
    artist.add_to_list(im3)

    #Fjerde bilde
    im4 = artist.blur(artist.image1)
    im4 = artist.change_exposure(3, im4)
    im4 = artist.rotate(120, im4)
    artist.add_to_list(im4)

    #Femte bilde
    im5 = artist.invert_colors(artist.image2)
    im5 = artist.change_contrast(10, im5)
    artist.add_to_list(im5)

    #Sjette bilde
    im6 = artist.invert_colors(artist.image3)
    im6 = artist.change_contrast(2, im6)
    artist.add_to_list(im6)


    artist.create_collage(900,600)

main()
