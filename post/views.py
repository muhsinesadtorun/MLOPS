from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404
from .models import Post
from .forms import PostForm
from django.contrib import messages
#from pydantic.main import BaseModel
import keras.utils as image
#import matplotlib.pyplot as plt
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

    #if not request.user.is_authenticated():
        # Send error page if user is not logged in
        #return Http404()
    
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, "The creation process has been successfully completed.", extra_tags='message-success')
        return HttpResponseRedirect(post.get_absolute_url())
    
    context = {
        'form': form
    }

    return render(request, "post/form.html", context)
    

def post_update(request, id):

    #if not request.user.is_authenticated():
        # Send error page if user is not logged in
        #return Http404()
        
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, "The update process has been successfully executed.")
        return HttpResponseRedirect(post.get_absolute_url()) #HttpResponseRedirect()

    context = {
        'form': form
    }

    return render(request, "post/form.html", context)


def post_delete(request, id):

    if not request.user.is_authenticated():
        # Send error page if user is not logged in
        return Http404()   
     
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