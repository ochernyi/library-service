from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient

from books.models import Book
from borrowing.models import Borrowing
from users.models import User

BORROWS_URL = reverse("borrowings:borrowing-list")


class ReturnBookTests(TestCase):
    def setUp(self):
        self.fixture_data = {}
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@test.com", password="testpassword"
        )
        self.borrowed_book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=1,
            inventory=2,
            daily_fee=10.0,
        )
        self.borrow = Borrowing.objects.create(
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date() + timezone.timedelta(days=7),
            actual_return_date=None,
            book=self.borrowed_book,
            user=self.user,
        )

        self.BORROW_RETURN_URL = reverse(
            "borrowings:borrowing-return-book", kwargs={"pk": self.borrow.pk}
        )

        self.client.force_authenticate(self.user)

    def test_return_book_successfully(self):
        data = {"return_book": True}
        response = self.client.post(self.BORROW_RETURN_URL, data, format="json")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {"status": "Your book was successfully returned"}
        )
        self.borrowed_book.refresh_from_db()
        self.assertEqual(self.borrowed_book.inventory, 3)
        self.borrow.refresh_from_db()
        self.assertIsNotNone(self.borrow.actual_return_date)

    def test_return_book_already_returned(self):
        self.borrow.actual_return_date = timezone.now().date()
        self.borrow.save()
        data = {"return_book": True}
        response = self.client.post(self.BORROW_RETURN_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data[0],
            ErrorDetail(string="This book has already been returned.", code="invalid"),
        )

    def test_return_book_permission_denied(self):
        self.client.force_authenticate(user=None)
        data = {"return_book": True}
        response = self.client.post(self.BORROW_RETURN_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_return_book_wrong_user(self):
        other_user = User.objects.create_user(
            email="otheruser@test.com", password="testpassword"
        )
        self.client.force_authenticate(user=other_user)
        data = {"return_book": True}
        response = self.client.post(self.BORROW_RETURN_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
