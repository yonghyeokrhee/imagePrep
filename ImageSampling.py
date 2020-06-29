from PIL import Image
import numpy as np
import os
import io


class ImageSampling:

    def __init__(self, path_source, path_layer, n):
        self.path_source = path_source
        self.path_layer = path_layer
        self.img_width = None
        self.img_height = None
        self.height = None
        self.width = None
        self.n = n

    def slicing(self, n):
        im = Image.open(self.path_layer)
        im_org = Image.open(self.path_source)
        self.img_width, self.img_height = im.size
        self.height = self.img_height / n
        self.width = self.img_width
        for i in range(self.img_height // int(self.height / 2)):
            box = (0, i * (self.height / 2), self.img_width, i * (self.height / 2) + self.height)
            pixel_data = im.crop(box)
            data = np.array(pixel_data)
            ind = np.abs(data/255 - 1)[:,:,0]

            yield im_org.crop(box), ind.sum()


if __name__ == '__main__':
    path_layer = 'layer/1_BSL.png'
    path_source = 'org/1_BSL.jpg'
    start_num = 0
    img_sample = ImageSampling(path_source, path_layer, 100)
    for k, (piece, tag) in enumerate(img_sample.slicing(100), start_num):
        img = Image.new('L', (int(img_sample.width), int(img_sample.height)), 255)
        img.paste(piece)
        if tag > 0:
            path = os.path.join("{}_{}_{}.png".format(path_source.split('.')[0], k, 1))
            img.save(path)
        else:
            path = os.path.join("{}_{}_{}.png".format(path_source.split('.')[0], k, 0))
            img.save(path)
