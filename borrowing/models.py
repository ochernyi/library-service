from django.db import models

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="borrowings")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="borrowings")

    @property
    def is_active(self):
        return self.actual_return_date is None

    def __str__(self):
        return f"{self.book.title} borrowed by {self.user.first_name} {self.user.last_name}"
