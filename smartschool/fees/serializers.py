from rest_framework import serializers
from .models import AcademicYear, Term, ClassRoom, Guardian, Student, FeeType, FeeStructure, Invoice, Payment


class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = '__all__'


class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = '__all__'


class GuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    guardians = GuardianSerializer(many=True, read_only=True)
    guardian_ids = serializers.PrimaryKeyRelatedField(queryset=Guardian.objects.all(), many=True, write_only=True, required=False)

    class Meta:
        model = Student
        fields = ['id', 'admission_number', 'first_name', 'last_name', 'class_room', 'guardians', 'guardian_ids', 'is_active', 'created_at', 'updated_at']

    def create(self, validated_data):
        guardian_ids = validated_data.pop('guardian_ids', [])
        student = super().create(validated_data)
        if guardian_ids:
            student.guardians.set(guardian_ids)
        return student

    def update(self, instance, validated_data):
        guardian_ids = validated_data.pop('guardian_ids', None)
        student = super().update(instance, validated_data)
        if guardian_ids is not None:
            student.guardians.set(guardian_ids)
        return student


class FeeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeType
        fields = '__all__'


class FeeStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeStructure
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'