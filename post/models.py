from typing import Any
from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=120, verbose_name="Title")
    content = models.TextField(verbose_name="Contents")
    publishing_date = models.DateTimeField(verbose_name="Release Date", auto_now_add=True)
    image = models.ImageField(null=True, blank=True)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'id': self.id})
        #return "/post/{}".format(self.id)
    
    def get_index_url(self):
        return reverse('post:index')
        
    def get_create_url(self):
        return reverse('post:create', kwargs={'id': self.id})

    def get_update_url(self):
        return reverse('post:update', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('post:delete', kwargs={'id': self.id})
    
    def get_model_url(self):
        return reverse('post:predict', kwargs={'id': self.id})

    class Meta:
        ordering = ['-publishing_date', 'id']
