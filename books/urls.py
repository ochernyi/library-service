from rest_framework.routers import SimpleRouter

from books.views import BookViewSet

router = SimpleRouter()
router.register("books", BookViewSet, basename="books")
urlpatterns = router.urls

app_name = "books"
