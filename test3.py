import numpy as np
from keras.models import load_model
import cv2
def get_prediction3(filename, wanteddirectory):
    model_path = '/home/aziz0220/mysite/chest-xray-pneumonia.h5'
    model = load_model(model_path) # Loading our model
    image = cv2.imread(wanteddirectory+filename, cv2.IMREAD_GRAYSCALE)
    resized_arr = cv2.resize(image, (150, 150))/255
    reshaped_arr = np.reshape(resized_arr, (-1, 150, 150, 1))
    prediction=model.predict(reshaped_arr)
    print(f'Predictions: {prediction}')
    if (prediction[0][0] >0.5):
        return("NORMAL",prediction[0][0])
    else:
        return("PNEUMONIE",1-(prediction[0][0]))