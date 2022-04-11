from flask import Flask, render_template
import database
import random
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

app = Flask(__name__)


@app.route("/")
def main():
    a = []
    results = []
    eating = []
    filtered = []
    for i in range(5):
        r = random.randint(1, 100)
        a.append(str(r)+'.jpeg')
        # b= np.sort(analysis(a[i])[0])[::-1]
        b= analysis(a[i],"keras_model.h5")
        mapping = {}
        traits = ['healthy','hungry','skin diseased','smacking lips too much','drooling']
        for j in range(5):
            mapping[b[0][j]] = traits[j]

        b= np.sort(b[0])[::-1]
        final_order = [mapping[x] for x in b]
        s = f'Your cow is most likely {final_order[0]}'
        brojac=1
        while b[0]-b[brojac]<=b[0]*0.1:
            s=s+f', {final_order[brojac]}'
            brojac=brojac+1
        s = s+'.'
        results.append(s)
        d = database.get_filtered(final_order[0])
        filtered.append(f'She is most likely '+ d[0]["Illnesses"] + '.')
    return render_template ('index.html', photo_num = a, results = results, filtered = filtered)

@app.route("/eating")
def eating():
    results = []
    a=[]
    for i in range(4):
        r = random.randint(200, 305)
        a.append(str(r)+'.jpeg')
        # b= np.sort(analysis(a[i])[0])[::-1]
        b= analysis(a[i],"eating.h5")
        if b[0][0]<b[0][1]:
            s = 'Your cow is currently Mooing and enjoying all the cow stuff.'
        else:
            s = 'Your cow is currently enjoying a green green meal.' 
        results.append(s)
    return render_template('eating.html', results=results, photo_num=a)


def analysis(cu,muslukus):
    # Load the model
    model = load_model(muslukus)

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    # Replace this with the path to your image
    image = Image.open(cu)
    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = np.asarray(image)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    return prediction