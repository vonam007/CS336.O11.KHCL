import numpy as np
from keras.models import Model
from keras.utils import img_to_array
from keras.applications import xception, vgg16


class VGG16_FE:
    def __init__(self) -> None:
        base_model = vgg16.VGG16() 
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

    def extract(self, image) -> np.ndarray:
        image = image.resize((224, 224))
        image = image.convert('RGB')

        array = img_to_array(image)
        array = np.expand_dims(array, axis=0)
        array = vgg16.preprocess_input(array)

        feature = self.model.predict(array)[0]
        feature = feature / np.linalg.norm(feature)

        return feature
    
class Xception_FE:
    def __init__(self) -> None:
        base_model = xception.Xception()
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('avg_pool').output)

    def extract(self, image) -> np.ndarray:
        image = image.resize((299, 299)) 
        image = image.convert('RGB')

        array = img_to_array(image)
        array = np.expand_dims(array, axis=0) 
        array = xception.preprocess_input(array) 

        feature = self.model.predict(array)[0]
        feature = feature / np.linalg.norm(feature)

        return feature
    

