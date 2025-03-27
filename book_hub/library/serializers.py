from rest_framework import serializers
from .models import Book, Transaction

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['user', 'checkout_date', 'return_date', 'is_returned']