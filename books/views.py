from typing import List

from rest_framework.permissions import IsAdminUser, AllowAny, BasePermission
from rest_framework.viewsets import ModelViewSet

from books.models import Book
from books.serializers import BookSerializer


class BookViewSet(ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.filter(out_of_books=False)

    def get_permissions(self) -> List[BasePermission]:
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
