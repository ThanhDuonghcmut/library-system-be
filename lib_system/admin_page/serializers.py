from .models import Category, Book, BookBatch
from rest_framework import serializers


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category']


class BookBatchSerializers(serializers.ModelSerializer):
    class Meta:
        model = BookBatch
        fields = ['id', 'title', 'author', 'category',
                  'description', 'quantity', 'rented', 'loss']


class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'batch_id', 'status']
