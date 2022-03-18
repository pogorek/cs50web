from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def following(self):
        return Follow.objects.filter(follower=self).count()

    def followers(self):
        return Follow.objects.filter(user=self).count()


class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    time_created = models.DateTimeField(auto_now_add=True)
    # likes = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')

    def __str__(self):
        return f"{self.pk} | {self.author} | {self.content}"

    class Meta:
        ordering = ['-time_created']


# class Like(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

    # def __str__(self):
    #     return f"{self.id} | {self.posts}"


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower")

    def __str__(self):
        return f"{self.user} | {self.follower}"
