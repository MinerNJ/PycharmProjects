from django import forms
class ImageForm(forms.Form):
    imagefile = forms.ImageFiel(label='Select an image to upload.')