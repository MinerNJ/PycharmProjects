from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from carapp.models import PicUpload
from carapp.forms import ImageForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def list(request):
    image_path = ''
    image_path1 = ''
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            newDoc = PicUpload(imagefile=request.FILES['imagefile'])
            newDoc.save()

            return HttpResponseRedirect(reverse('list'))
    else:
        form = ImageForm()

    documents = PicUpload.objects.all()
    for document in documents:
        image_path = document.imagefile.name
        image_path1 = '/'+image_path

        document.delete()

    request.session['image_path'] = image_path

    return render(request, 'list.html',
    {'documents': documents, 
     'image_path1': image_path1,
     'form': form }
    )

#Car Damage Detection
import os 
import json

import h5py
import numpy as np
import pickle as pk
from PIL import Image

from keras.preprocessing.image import img_to_array, load_img
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.preprocessing import image
from keras.models import Model, load_model
from keras import backend as K
import tensorflow as tf

#Preparing image for processing
def prepare_img_224(img_path):
    img = load_img(img_path, target_size=(224, 224))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

#Loading valid categories for identifying cars using VGG16.
with open('static/cat_counter.pk', 'rb') as f:
    cat_counter = pk.load(f)

#Using top 27 categories for cars from VGG16
cat_list = [k for k, v in cat_counter.most_common()[:27]]

global graph
graph = tf.get_default_graph()

#Preparing flat image
def prepare_flat(img_224):
    base_model = load_model('static/vgg16.h5')
    model = Model(input=base_model.input, output=base_model.get_layer('fc1').output)
    feature = model.predict(img_224)
    flat = feature.flatten()
    flat = np.expand_dims(flat, axis=0)
    return flat

#First check - car or not?
CLASS_INDEX_PATH = 'static/imagenet_class_index.json'

def get_predictions(preds, top=5):
    
    global CLASS_INDEX
    CLASS_INDEX = json.load(open(CLASS_INDEX_PATH))
        
    results = []
    for pred in preds:
        top_indices = pred.argsort()[-top:][::-1]
        result = [tuple(CLASS_INDEX[str(i)]) + (pred[i],) for i in top_indices]
        result.sort(key=lambda x: x[2], reverse=True)
        results.append(result)
    return results

def car_categories_check(img_224):
    first_check = load_model('static/vgg16.h5')
    print ("Validating the picture of your car...")
    out = first_check.predict(img_224)
    top = get_predictions(out, top=5)
    for j in top[0]:
        if j[0:2] in cat_list:
            print("Car check passed. Proceeding to damage detector.")
            print("\n")
            return True
    return False
    
#Second check - Damaged or not?
def car_damage_check(img_flat):
    second_check = pk.load(open('static/second_check.pickle', 'rb'))
    print("Checking for damage...")
    train_labels = ['00-damage', '001-intact']
    preds = second_check.predict(img_flat)
    prediction = train_labels[preds[0]]
    
    if train_labels[preds[0]] == '00-damage':
        print("Damage check complete - proceeding to damage location and severity detector.")
        print("\n")
        return True
    else:
        return False

#Third check - damage location
def damage_locator(img_flat):
    print("Locating area damaged - front, side or rear.")
    third_check = pk.load(open('static/third_check.pickle', 'rb'))
    train_labels = ['Front', 'Rear', 'Side']
    preds = third_check.predict(img_flat)
    prediction = train_labels[preds[0]]
    print("Your car is damaged at - " + train_labels[preds[0]])
    print("Damage location assessment complete.")
    print("\n")
    return prediction

#Fourth check - damage severity
def severity_assessment(img_flat):
    print("Evaluating the severity of the damage.")
    fourth_check = pk.load(open('static/fourth_check.pickle', 'rb'))
    train_labels = ['Minor', 'Moderate', 'Severe']
    preds = fourth_check.predict(img_flat)
    prediction = train_labels[preds[0]]
    print("The damage done to your car is rated as - " + train_labels[preds[0]])
    print("Damage severity estimate complete")
    print("\n")
    return prediction

#Engine
def engine(request):

    MyCar=request.session['image_path']
    img_path = MyCar
    request.session.pop('image_path', None)
    request.session.modified = True
    with graph.as_default():

        img_224 = prepare_img_224(img_path)
        img_flat = prepare_flat(img_224)
        g1 = car_categories_check(img_224)
        g2 = car_damage_check(img_flat)

        while True:
            try:
            
                if g1 is False:
                    g1_pic = "Could not recognize picture of car. Please submit a different picture."
                    g2_pic = 'N/A'
                    g3 = 'N/A'
                    g4 = 'N/A'
                    ns = 'N/A'
                    break
                else:
                    g1_pic = "Car confirmed"
                            
                if g2 is False:
                    g1_pic = "Car appears undamaged. Please submit a \n different picture of your damaged car."
                    g2_pic = 'N/A'
                    g3 = 'N/A'
                    g4 = 'N/A'
                    ns = 'N/A'
                    break
                else:
                    g2_pic = "Car damage confirmed. See below for damage location and severity."
                    g3 = damage_locator(img_flat)
                    g4 = severity_assessment(img_flat)
                    ns='a). Create a report and send to dealer \n b). Proceed to cost estimate. \n c). View nearby dealerships.'
                    break
            except:
                break

    src='pic_upload/'
    import os
    for image_file_name in os.listdir(src):
        if image_file_name.endswith(".jpg"):
            os.remove(src + image_file_name)
        
    K.clear_session()

    return render(
        request,
        'results.html', context={'g1_pic':g1_pic,
                                 'g2_pic':g2_pic,
                                 'loc':g3,
                                 'sev':g4,
                                 'ns':ns}
    )