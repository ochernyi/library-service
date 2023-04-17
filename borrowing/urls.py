from rest_framework.routers import SimpleRouter
from borrowing.views import BorrowingViewSet

router = SimpleRouter()
router.register("", BorrowingViewSet, basename="borrowing")
urlpatterns = router.urls

app_name = "borrowings"
