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
        image_path = '/'+image_path
        document.delete()

    request.session['image_path'] = image_path

    return render(request, 'list.html',
    {'documents': documents, 
     'image_path': image_path,
     'form': form }
    )