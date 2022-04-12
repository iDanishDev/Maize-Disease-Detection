from flask import Flask, render_template, request

import numpy as np
import os

from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model



filepath = 'C:/Users/aaaya/Desktop/Workspace/KJSCE/MiniProject/assets/backend_model.h5'
model = load_model(filepath)
print(model)

print("Model Loaded Successfully")



def pred_maize_disease(img_maize_crop):

    image_process = load_img(img_maize_crop, target_size = (128,128))
    print("Image Recieved")

    image_process = img_to_array(image_process)/255
    image_process = np.expand_dims(image_process, axis=0)
    
    result = model.predict(image_process)

    print("Result ",result)

    pred = np.argmax(result, axis=1)

    print(pred)




    if(pred==0):
        return "Maize - Blight",'Maize - Blight.html'

    elif(pred==1):
        return "Maize - Common Rust",'Maize - Commonrust.html'

    elif(pred==2):
        return "Maize - Gray Leaf Spot",'Maize - Grayspots.html'
        
    elif(pred==3):
        return "Maize - Healthy",'Maize - Healthy.html'








app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
        return render_template('index.html')
    
 

@app.route("/predict", methods = ['GET','POST'])
def predict():
     if request.method == 'POST':
        file = request.files['image']
        filename = file.filename        
        print("Input posted = ", filename)
        
        file_path = os.path.join('C:/Users/aaaya/Desktop/Workspace/KJSCE/MiniProject/assets/upload', filename)
        file.save(file_path)

        print("Predicting ")
        pred, output_page = pred_maize_disease(img_maize_crop=file_path)
              
        return render_template(output_page,pred_output = pred, user_image = file_path)
    
if __name__ == "__main__":
    app.run(threaded=False,port=8080) 