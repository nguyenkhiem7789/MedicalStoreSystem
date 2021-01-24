from rest_framework import serializers
from MedicalStoreApp.models import Company

class CompanySerliazer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ["name", "license_no", "address", "contact_no", "email", "description"]