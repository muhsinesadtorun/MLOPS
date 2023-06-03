from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404
from .models import Post
from .forms import PostForm
from django.contrib import messages
from tensorflow import keras
from keras import datasets, layers, models
######################from pydantic.main import BaseModel
import keras.utils as image
######################import matplotlib.pyplot as plt
import numpy as np
from joblib import load
from .metrics import *
from sklearn.metrics import classification_report

my_model = load('static/models/cnn_model.joblib')

(X_train, y_train), (X_test, y_test) = datasets.cifar10.load_data()
y_train = y_train.reshape(-1,)
y_train[:5]
X_train = X_train / 255
X_test = X_test /255
y_pred = my_model.predict(X_test)
y_test = y_test.reshape(-1,)
y_pred_classes = [np.argmax(element) for element in y_pred]

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

    #if not request.user.is_authenticated():
        # Send error page if user is not logged in
        #return Http404()   
     
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect("post:index")


def get_classification_metrics(y_true, y_pred):
    report = classification_report(y_true, y_pred)
    lines = report.split('\n')[2:-3]  # Exclude headers and averages

    precision_array = []
    recall_array = []
    f1_score_array = []
    for line in lines:
        values = line.strip().split()
        if values == []:
            break
        
        else:
            precision, recall, f1_score, support = map(float, values[1:])
            f1_score_array.append(f1_score)
            precision_array.append(precision)
            recall_array.append(recall)
    
    avg_f1_score = sum(f1_score_array) / len(f1_score_array)
    avg_precision = sum(precision_array) / len(precision_array)
    avg_recall = sum(recall_array) / len(recall_array)

    return avg_f1_score, avg_precision, avg_recall

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
    avg_f1, avg_precision, avg_recall = get_classification_metrics(y_test, y_pred_classes)
    my_metric.inc()
    test_loss, test_accuracy = my_model.evaluate(X_test, y_test)
    global_accuracy.set(test_accuracy)
    global_loss.set(test_loss)
    global_precision.set(avg_precision)
    global_recall.set(avg_recall)
    global_f1_score.set(avg_f1)
    
    return render(request, "post/model.html", context)
