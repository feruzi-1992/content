from django.shortcuts import render
from django.db.models import Sum
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import AcademicYear, Term, ClassRoom, Guardian, Student, FeeType, FeeStructure, Invoice, Payment
from .serializers import (
    AcademicYearSerializer,
    TermSerializer,
    ClassRoomSerializer,
    GuardianSerializer,
    StudentSerializer,
    FeeTypeSerializer,
    FeeStructureSerializer,
    InvoiceSerializer,
    PaymentSerializer,
)


class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    filterset_fields = ['is_active', 'name']
    search_fields = ['name']
    ordering_fields = ['name', 'start_date', 'end_date']


class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.select_related('academic_year').all()
    serializer_class = TermSerializer
    filterset_fields = ['is_active', 'academic_year']
    search_fields = ['name', 'academic_year__name']
    ordering_fields = ['start_date', 'end_date']


class ClassRoomViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer
    search_fields = ['name']
    ordering_fields = ['name']


class GuardianViewSet(viewsets.ModelViewSet):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializer
    search_fields = ['full_name', 'phone', 'email']


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('class_room').prefetch_related('guardians').all()
    serializer_class = StudentSerializer
    filterset_fields = ['class_room', 'is_active', 'admission_number']
    search_fields = ['admission_number', 'first_name', 'last_name']


class FeeTypeViewSet(viewsets.ModelViewSet):
    queryset = FeeType.objects.all()
    serializer_class = FeeTypeSerializer
    search_fields = ['code', 'name']


class FeeStructureViewSet(viewsets.ModelViewSet):
    queryset = FeeStructure.objects.select_related('academic_year', 'class_room', 'fee_type').all()
    serializer_class = FeeStructureSerializer
    filterset_fields = ['academic_year', 'class_room', 'fee_type']


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.select_related('student', 'term').prefetch_related('payments').all()
    serializer_class = InvoiceSerializer
    filterset_fields = ['student', 'term', 'is_paid', 'reference']
    search_fields = ['reference', 'student__admission_number', 'student__first_name', 'student__last_name']

    @action(detail=True, methods=['get'], url_path='balance')
    def balance(self, request, pk=None):
        invoice = self.get_object()
        balance_amount = invoice.total_amount - invoice.amount_paid
        return Response({'invoice': invoice.reference, 'balance': balance_amount})


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('invoice', 'received_by').all()
    serializer_class = PaymentSerializer
    filterset_fields = ['method', 'received_on', 'invoice']

    def perform_create(self, serializer):
        payment = serializer.save(received_by=self.request.user if self.request.user.is_authenticated else None)
        invoice = payment.invoice
        aggregate = invoice.payments.aggregate(total=Sum('amount'))
        total_paid = aggregate.get('total') or 0
        invoice.amount_paid = total_paid
        invoice.is_paid = total_paid >= invoice.total_amount
        invoice.save(update_fields=['amount_paid', 'is_paid'])
