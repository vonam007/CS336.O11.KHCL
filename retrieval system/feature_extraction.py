import numpy as np
from keras.models import Model
from keras.utils import img_to_array
from keras.applications import xception, vgg16, resnet50, mobilenet_v2, efficientnet_v2, inception_v3


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
    
class ResNet50_FE:
    def __init__(self) -> None:
        base_model = resnet50.ResNet50()
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('avg_pool').output)

    def extract_features(self, image) -> np.ndarray:
        image = image.resize((224, 224))
        image = image.convert('RGB')

        array = img_to_array(image)
        array = np.expand_dims(array, axis=0)
        array = resnet50.preprocess_input(array)

        features = self.model.predict(array)[0]
        features /= np.linalg.norm(features)

        return features

class MobileNetV2__FE:
    def __init__(self) -> None:
        base_model = mobilenet_v2.MobileNetV2()
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('global_average_pooling2d').output)

    def extract_features(self, image) -> np.ndarray:
        image = image.resize((224, 224))
        image = image.convert('RGB')

        array = img_to_array(image)
        array = np.expand_dims(array, axis=0)
        array = mobilenet_v2.preprocess_input(array)

        features = self.model.predict(array)[0]
        features /= np.linalg.norm(features)

        return features

class EfficientNetV2_FE:
    def __init__(self) -> None:
        base_model = efficientnet_v2.EfficientNetV2S() 
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('top_dropout').output)

    def extract(self, image) -> np.ndarray:
        image = image.resize((384, 384))
        image = image.convert('RGB')

        array = img_to_array(image)
        array = np.expand_dims(array, axis=0)
        array = efficientnet_v2.preprocess_input(array)

        feature = self.model.predict(array)[0]
        feature = feature / np.linalg.norm(feature)

        return feature

class InceptionV3_FE:
    def __init__(self) -> None:
        base_model = inception_v3.InceptionV3() 
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('avg_pool').output)

    def extract(self, image) -> np.ndarray:
        image = image.resize((299, 299))
        image = image.convert('RGB')

        array = img_to_array(image)
        array = np.expand_dims(array, axis=0)
        array = inception_v3.preprocess_input(array)

        feature = self.model.predict(array)[0]
        feature = feature / np.linalg.norm(feature)

        return feature
