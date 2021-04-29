from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Genres(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100)

    def __str__(self):
        return f'{self.id},{self.name}'


class Platforms(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100)

    def __str__(self):
        return f'{self.id},{self.name}'


class Publisher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100)

    def __str__(self):
        return f'{self.id},{self.name}'


class Game(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=200)
    Release_date = models.DateField(null=True)
    Required_age = models.IntegerField(null=True)
    achievements = models.BooleanField(null=True)
    positive_ratings = models.IntegerField(null=True)
    negative_ratings = models.IntegerField(null=True)
    average_playtime = models.IntegerField(null=True)
    price = models.FloatField()
    Publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True)
    Platforms = models.ForeignKey(Platforms, on_delete=models.CASCADE, null=True)
    Genres = models.ForeignKey(Genres, on_delete=models.CASCADE, null=True)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, )
    address = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}, {self.user.email}, {self.address}, {self.user.password}'

    class Meta:
        db_table = 'customer'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Customer.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.customer.save()


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    item = models.ForeignKey(Game, on_delete=models.CASCADE)
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_date = models.DateField()

    def __str__(self):
        return f'{self.customer},{self.created_date}'


class LineItem(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey(Game, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity},{self.product},{self.cart},{self.order},{self.created_date}'
