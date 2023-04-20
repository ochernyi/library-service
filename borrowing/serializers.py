import asyncio
from typing import Dict, Any

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from books.models import Book
from borrowing.models import Borrowing
# from borrowing.telegram_alert import send_message_to_channel


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("book", "expected_return")

    def create(self, validated_data: Dict[str, Any]) -> Borrowing:
        book_update = Book.objects.get(title=validated_data["book"])
        if book_update.inventory > 0:
            book_update.inventory -= 1
            book_update.save()
            # asyncio.run(
            #     send_message_to_channel(
            #         text=f"{validated_data['user']} just borrowed '{validated_data['book']}' and will return it {validated_data['expected_return']}"
            #     )
            # )
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



# from django.db import transaction
# from rest_framework import serializers
# from rest_framework.exceptions import ValidationError
#
# from books.serializers import BookSerializer
# from borrowing.models import Borrowing
#
#
# class BorrowingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Borrowing
#         fields = (
#             "id",
#             "book",
#             "user",
#             "is_active",
#             "borrow_date",
#             "expected_return_date",
#         )
#
#     def validate(self, attrs: dict) -> dict:
#         data = super(BorrowingSerializer, self).validate(attrs)
#
#         if attrs["book"].inventory <= 0:
#             raise ValidationError("Book inventory is empty")
#
#         if not attrs["is_active"]:
#             raise ValidationError("Borrow already close")
#
#         return data
#
#     # @transaction.atomic()
#     # def create(self, validated_data: dict) -> dict:
#     #     book = validated_data["book"]
#     #     book.inventory -= 1
#     #     book.save()
#     #     return super().create(validated_data)
#
#
# # class BorrowingListSerializer(BorrowingSerializer):
# #     book = serializers.SlugRelatedField(many=False, read_only=True, slug_field="title")
# #     user = serializers.ReadOnlyField(source="user.full_name", read_only=True)
# #     borrow_date = serializers.ReadOnlyField()
# #
# #     class Meta:
# #         model = Borrowing
# #         fields = (
# #             "id",
# #             "user",
# #             "borrow_date",
# #             "expected_return_date",
# #             "book",
# #             "is_active",
# #         )
# #
# #
# # class BorrowingDetailSerializer(BorrowingSerializer):
# #     borrow_date = serializers.ReadOnlyField()
# #     book = BookSerializer()
# #     user_full_name = serializers.ReadOnlyField(source="user.full_name", read_only=True)
# #     user_email = serializers.ReadOnlyField(source="user.email", read_only=True)
# #     is_active = serializers.BooleanField(default=False)
# #
# #     class Meta:
# #         model = Borrowing
# #         fields = (
# #             "id",
# #             "user_full_name",
# #             "user_email",
# #             "borrow_date",
# #             "expected_return_date",
# #             "actual_return_date",
# #             "book",
# #             "is_active",
# #         )
