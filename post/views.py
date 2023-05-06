from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect
from .models import Post
from .forms import PostForm
from django.contrib import messages
from pydantic.main import BaseModel

#from keras.preprocessing import image
import keras.utils as image

import matplotlib.pyplot as plt
import numpy as np
from joblib import load

my_model = load('./models/mlopsModel.joblib')

def post_index(request):
    posts = Post.objects.all()
    return render(request, "post/index.html", {'posts': posts})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    context = {
        'post': post
    }
    return render(request, "post/detail.html", context)

def post_create(request):
    '''
    form = PostForm()
    context = {
        'form': form,
    }
    return render(request, "post/form.html", context)
    '''
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save()
        messages.success(request, "Başarili bir şekilde oluşturdunuz.", extra_tags='mesaj-basarili')
        return redirect(post.get_absolute_url())
    
    context = {
        'form': form
    }

    return render(request, "post/form.html", context)
    

def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, "Başarili bir şekilde güncellediniz.")
        return redirect(post.get_absolute_url()) #HttpResponseRedirect()

    context = {
        'form': form
    }

    return render(request, "post/form.html", context)


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect("post:index")

def post_predict(request, id):
    post = get_object_or_404(Post, id=id)
    classes = ["airplane","automobile","bird","cat","deer","dog","frog","horse","ship","truck"]
    img_path = "./media/"+post.image.name
    img = image.load_img(img_path, target_size=(32, 32))
    img_array = image.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)
    img_batch = img_batch/255
    output = my_model.predict(img_batch)
    answer = classes[np.argmax(output)]
    context = {
        'post': post,
        'answer': answer,
    }
    return render(request, "post/model.html", context)
    '''
    post = get_object_or_404(Post, id=id)
    img_path = post.image
    #img_path = "den.jpeg"
    img = image.load_img(img_path, target_size=(32, 32))
    plt.imshow(img)
    plt.show()
    img_array = image.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)
    img_batch = img_batch/255
    output = my_model.predict(img_batch)
    classes[np.argmax(output)]
    return render(request, "post/detail.html", context)
    
    img_array = image.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)
    img_batch = img_batch/255
    output = my_model.predict(img_batch)
    classes[np.argmax(output)]
    return render(request, "post/detail.html")
    '''



    #return redirect("post:index")
'''
    form = PostForm()
    context = {
        'form': form,
    }
    my_model = joblib.load('static/model/mymodel')
    img_path = "media/"
    img = image.load_img(img_path, target_size=(32, 32))
plt.imshow(img)
plt.show()
img_array = image.img_to_array(img)
img_batch = np.expand_dims(img_array, axis=0)
img_batch = img_batch/255
çıktı = deneme.predict(img_batch)
classes[np.argmax(çıktı)]
    return str(my_model.predict(x))
    '''