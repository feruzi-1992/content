from rest_framework.routers import DefaultRouter
from .views import (
    AcademicYearViewSet,
    TermViewSet,
    ClassRoomViewSet,
    GuardianViewSet,
    StudentViewSet,
    FeeTypeViewSet,
    FeeStructureViewSet,
    InvoiceViewSet,
    PaymentViewSet,
)

router = DefaultRouter()
router.register(r'academic-years', AcademicYearViewSet)
router.register(r'terms', TermViewSet)
router.register(r'classrooms', ClassRoomViewSet)
router.register(r'guardians', GuardianViewSet)
router.register(r'students', StudentViewSet)
router.register(r'fee-types', FeeTypeViewSet)
router.register(r'fee-structures', FeeStructureViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = router.urls