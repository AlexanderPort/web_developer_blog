from django.db import models
import datetime


class User(models.Model):
    name = models.CharField(max_length=250)
    surname = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    avatar = models.FilePathField()
    email = models.EmailField()
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    followers = models.ManyToManyField(to='self')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)

    def __str__(self):
        return f"User(name={self.name}, surname={self.surname})"

    @property
    def fullname(self):
        return f"{self.name} {self.surname}"


class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    image = models.FilePathField()
    followers = models.ManyToManyField(to=User)

    def __str__(self):
        return f"Field(name={self.name})"


class Article(models.Model):
    # category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    text = models.TextField()
    preview = models.FilePathField()
    title = models.CharField(max_length=250)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=1000)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Article(title={self.title}, author={self.author.fullname}, views={self.views})"


class Comment(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE)
    text = models.CharField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Comment(author={self.author.fullname})"

