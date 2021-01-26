from rest_framework import serializers
from MedicalStoreApp.models import Company, CompanyBank


class CompanySerliazer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

class CompanyBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyBank
        fields = "__all__"