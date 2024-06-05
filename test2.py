from tensorflow.keras.preprocessing import image
from keras.models import load_model
import numpy as np

def predict_class(image_path, model):
    img = image.load_img(image_path, target_size=(150, 150))
    img_tensor = image.img_to_array(img)
    img_tensor /= 255.0
    img_tensor = np.expand_dims(img_tensor, axis=0)
    prediction = model.predict(img_tensor)
    if prediction[0][0] < prediction[0][1] and prediction[0][2] < prediction[0][1]:
        return ("Bacteral Pneumonia",prediction[0][1])
    else:
        if prediction[0][0] < prediction[0][2] and prediction[0][1] < prediction[0][2]:
            return ("Viral Pneumonia",prediction[0][2])
        else :
            return ("Normal",prediction[0][0])
def get_prediction2(filename, wanteddirectory):
    model_path = '/app/sequencialfor3classes.h5'
    model = load_model(model_path)
    image_path = wanteddirectory+filename
    return predict_class(image_path, model)
