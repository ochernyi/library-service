from typing import Any, Type
from urllib.request import Request

from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowSerializer,
    BorrowListSerializer,
)


class BorrowPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 10


class BorrowViewSet(ModelViewSet):
    serializer_class = BorrowSerializer
    queryset = Borrowing.objects.select_related("book", "user")
    pagination_class = BorrowPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        """Retrieve the borrows with filters"""
        queryset = self.queryset
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")
        if user_id:
            queryset = self.queryset.filter(user_id=user_id)
        if is_active is True:
            queryset = self.queryset.filter(actual_return_date__isnull=False)
        if is_active is False:
            queryset = self.queryset.filter(actual_return_date__isnull=True)
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user).distinct()

    def get_serializer_class(self) -> Type[serializers.Serializer]:
        if self.action in ["list", "retrieve"]:
            return BorrowListSerializer
        return BorrowSerializer

    def perform_create(self, serializer: BorrowSerializer) -> None:
        serializer.save(user=self.request.user)

    @transaction.atomic()
    @action(methods=["POST"], detail=True, url_path="return", serializer_class=None)
    def return_book(self, request: Request, pk: int = None) -> Response:
        """Endpoint for returning book and close the borrow"""
        borrow = self.get_object()
        if borrow.actual_return_date is not None:
            raise ValidationError("This book has already been returned.")
        if self.request.user != borrow.user:
            raise ValidationError("You can`t return book which not yours")
        borrow.actual_return_date = timezone.now()
        borrow.save()
        book = borrow.book
        book.inventory += 1
        book.save()
        return Response(
            {
                "status": "Your book was successfully returned",
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "user_id",
                type=OpenApiTypes.INT,
                description="Filter borrows by user id (ex. ?user_id=2)",
            ),
            OpenApiParameter(
                "is_active",
                type=OpenApiTypes.BOOL,
                description="Filter active borrows (ex. ?is_active=True)",
            ),
        ]
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)
