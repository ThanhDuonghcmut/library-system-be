from django.db import models

# Create your models here.


class Category(models.Model):
    category = models.CharField(max_length=50)


class BookBatch(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    category = models.ForeignKey(to='Category', on_delete=models.PROTECT)
    description = models.CharField(max_length=1000)
    quantity = models.PositiveBigIntegerField()
    rented = models.PositiveBigIntegerField()
    loss = models.PositiveBigIntegerField()


class Book(models.Model):
    batch_id = models.ForeignKey(
        to='BookBatch', on_delete=models.PROTECT, unique=False)
    status = models.PositiveSmallIntegerField()
