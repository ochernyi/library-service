import asyncio
from typing import Dict, Any

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from books.models import Book
from borrowing.models import Borrowing
from borrowing.telegram import send_message


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("book", "expected_return")

    def create(self, validated_data: Dict[str, Any]) -> Borrowing:
        book_update = Book.objects.get(title=validated_data["book"])
        if book_update.inventory > 0:
            book_update.inventory -= 1
            book_update.save()
            asyncio.run(
                send_message(
                    text=f"{validated_data['user']} just borrowed '{validated_data['book']}' and will return it {validated_data['expected_return']}"
                )
            )
            return super().create(validated_data)
        raise ValidationError("This book is unavailable")


class BorrowListSerializer(BorrowSerializer):
    book = serializers.CharField(source="book.title")
    user = serializers.CharField(source="user.email")

    class Meta:
        model = Borrowing
        fields = "__all__"


class BorrowReturnSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source="book.title")

    class Meta:
        model = Borrowing
        fields = ("book",)