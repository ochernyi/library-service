from rest_framework.routers import SimpleRouter
from borrowing.views import BorrowViewSet

router = SimpleRouter()
router.register("", BorrowViewSet, basename="borrowing")
urlpatterns = router.urls

app_name = "borrowings"
