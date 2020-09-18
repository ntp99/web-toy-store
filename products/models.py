from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import models as auth_models
from django.db.models import Avg

class Product(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0, blank=False)
    minimum_age_appropriate = models.IntegerField(blank=False,default=0)
    maximum_age_appropriate = models.IntegerField(blank=False,default=-1)
    image = models.ImageField(blank=True)

    def __str__(self):
        return "{} ${}".format(self.name, self.price)

    def age_range(self):
        if self.minimum_age_appropriate == self.maximum_age_appropriate:
            return "Age {}".format(self.minimum_age_appropriate)
        elif self.maximum_age_appropriate == -1:
            return "Ages {} and up".format(self.minimum_age_appropriate)
        else:
            return "Ages {} to {}".format(self.minimum_age_appropriate, self.maximum_age_appropriate)

    def average_rating(self):
        return float(self.review_set.all().aggregate(Avg('stars'))['stars__avg'])


class Review(models.Model):
    stars = models.IntegerField(blank=False, validators=[MinValueValidator(1),MaxValueValidator(5)])
    description = models.TextField(blank=False)
    product = models.ForeignKey(Product)
    user = models.ForeignKey(auth_models.User)
