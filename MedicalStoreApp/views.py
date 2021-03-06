from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from MedicalStoreApp.models import Company, CompanyBank, Medicine, MedicalDetails, CompanyAccount, Employee
from MedicalStoreApp.serializers import CompanySerializer, CompanyBankSerializer, MedicineSerializer, \
    MedicalDetailsSerializer, MedicalDetailsSerializerSimple, CompanyAccountSerializer, EmployeeSerializer
import logging


class CompanyViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        company = Company.objects.all()
        serializer = CompanySerializer(company, many=True, context={"request": request})
        response_dict = {
            "error": False,
            "message": "All Company List Data",
            "data": serializer.data
        }
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = CompanySerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {
                "error": False,
                "message": "Company Data Save Successfully"
            }
        except:
            dict_response = {
                "error": True,
                "message": "Error During Saving Company Data"
            }
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        querySet = Company.objects.all()
        company = get_object_or_404(querySet, pk=pk)
        serializer = CompanySerializer(company, context={"request": request})

        serializer_data = serializer.data
        # Accessing All the Company bank details of current company id
        company_bank_details = CompanyBank.objects.filter(company_id=serializer_data["id"])
        companybank_details_serializers = CompanyBankSerializer(company_bank_details, many=True)
        serializer_data["company_bank"] = companybank_details_serializers.data
        return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})

    def update(self, request, pk=None):
        try:
            queryset = Company.objects.all()
            company = get_object_or_404(queryset, pk=pk)
            serializer = CompanySerializer(company, data=request.data, context={"request": request})
            serializer.is_valid()
            serializer.save()
            dict_response = {
                "error": False,
                "message": "Company Data Update Successfully"
            }
        except:
            dict_response = {
                "error": True,
                "message": "Error During Update Company Data"
            }
        return Response(dict_response)


class CompanyBankViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = CompanyBankSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Company Bank Data Save Successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Company Bank Data"}
        return Response(dict_response)

    def list(self, request):
        companybank = CompanyBank.objects.all()
        serializer = CompanyBankSerializer(companybank, many=True, context={"request": request})
        dict_response = {"error": False, "message": "All Company Bank List Data", "data": serializer.data}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        querySet = CompanyBank.objects.all()
        companybank = get_object_or_404(querySet, pk=pk)
        serializer = CompanyBankSerializer(companybank, context={"request": request})
        return Response({"error": False, "message": "Single Data Fetch", "data": serializer.data})

    def update(self, request, pk=None):
        querySet = CompanyBank.objects.all()
        companybank = get_object_or_404(querySet, pk=pk)
        serializer = CompanyBankSerializer(companybank, data=request.data, context={"request": request})
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data Has Been Updated"})


class CompanyNameViewSet(generics.ListAPIView):
    serializer_class = CompanySerializer

    def get_queryset(self):
        name = self.kwargs["name"]
        return Company.objects.filter(name=name)


class CompanyOnlyViewSet(generics.ListAPIView):
    serializer_class = CompanySerializer

    def get_queryset(self):
        return Company.objects.all()


class MedicineViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = MedicineSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            medicine_id = serializer.data['id']
            medicine_details_list = []
            for medicine_detail in request.data["medicine_details"]:
                print(medicine_detail)
                medicine_detail["medicine_id"] = medicine_id
                medicine_details_list.append(medicine_detail)
                print(medicine_detail)

            serializer2 = MedicalDetailsSerializer(data=medicine_details_list, many=True, context={"request": request})
            serializer2.is_valid()
            serializer2.save()

            dict_response = {"error": False, "message": "Medicine Data Save Successfully"}
        except Exception as Argument:
            dict_response = {"error": True, "message": "Error During Saving Medicine Data"}
            logging.exception("Error During Saving Medicine Data")
        return Response(dict_response)

    def list(self, request):
        medicine = Medicine.objects.all()
        serializer = MedicineSerializer(medicine, many=True, context={"request": request})

        medicine_data = serializer.data
        newmedicinelist = []

        for medicine in medicine_data:
            medicine_details = MedicalDetails.objects.filter(medicine_id=medicine["id"])
            medicine_details_serializers = MedicalDetailsSerializerSimple(medicine_details, many=True)
            medicine["medicine_details"] = medicine_details_serializers.data
            newmedicinelist.append(medicine)
        dict_response = {"error": False, "message": "All Medicine List Data", "data": newmedicinelist}

        return Response(dict_response)

    def retrieve(self, request, pk=None):
        querySet = Medicine.objects.all()
        medicine = get_object_or_404(querySet, pk=pk)
        serializer = MedicineSerializer(medicine, context={"request": request})

        medicine_data = serializer.data
        medicine_details = MedicalDetails.objects.filter(medicine_id=medicine_data["id"])
        medicine_details_serializers = MedicalDetailsSerializerSimple(medicine_details, many=True)
        medicine_data["medicine_details"] = medicine_details_serializers.data

        return Response({"error": False, "message": "Single Data Fetch", "data": medicine_data})

    def update(self, request, pk=None):
        querySet = Medicine.objects.all()
        medicine = get_object_or_404(querySet, pk=pk)
        serializer = MedicineSerializer(medicine, data=request.data, context={"request": request})
        serializer.is_valid()
        serializer.save()
        for salt_detail in request.data["medicine_details"]:
            if salt_detail["id"] == 0:
                # For insert new salt details
                print("ADD")
                del salt_detail["id"]
                serializer2 = MedicalDetailsSerializer(data=salt_detail, context={"request": request})
                serializer2.is_valid()
                serializer2.save()
            else:
                # For update salt details
                querySet2 = MedicalDetails.objects.all()
                medicine_salf = get_object_or_404(querySet2, pk=salt_detail["id"])
                del salt_detail["id"]
                serializer3 = MedicalDetailsSerializer(medicine_salf, data=salt_detail,context={"request": request})
                serializer3.is_valid()
                serializer3.save()
                print("UPDATE")

        return Response({"error": False, "message": "Data Has Been Updated"})

# Company Account Viewset
class CompanyAccountViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = CompanyAccountSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Company Account Data Save Successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Company Account Data"}
        return Response(dict_response)

    def list(self, request):
        companyAccount = CompanyAccount.objects.all()
        serializer = CompanyAccountSerializer(companyAccount, many=True, context={"request": request})
        dict_response = {"error": False, "message": "All Company Account List Data", "data": serializer.data}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        querySet = CompanyBank.objects.all()
        companyAccount = get_object_or_404(querySet, pk=pk)
        serializer = CompanyAccountSerializer(companyAccount, context={"request": request})
        return Response({"error": False, "message": "Single Data Fetch", "data": serializer.data})

    def update(self, request, pk=None):
        querySet = CompanyAccount.objects.all()
        companyAccount = get_object_or_404(querySet, pk=pk)
        serializer = CompanyAccountSerializer(companyAccount, data=request.data, context={"request": request})
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data Has Been Updated"})

# Employee Account Viewset
class EmployeeViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = EmployeeSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False, "message": "Employee Data Save Successfully"}
        except:
            dict_response = {"error": True, "message": "Error During Saving Employee Data"}
        return Response(dict_response)

    def list(self, request):
        employee = Employee.objects.all()
        serializer = EmployeeSerializer(employee, many=True, context={"request": request})
        dict_response = {"error": False, "message": "All Employee List Data", "data": serializer.data}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        querySet = Employee.objects.all()
        employee = get_object_or_404(querySet, pk=pk)
        serializer = EmployeeSerializer(employee, context={"request": request})
        return Response({"error": False, "message": "Single Data Fetch", "data": serializer.data})

    def update(self, request, pk=None):
        querySet = Employee.objects.all()
        employee = get_object_or_404(querySet, pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data, context={"request": request})
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data Has Been Updated"})

company_list = CompanyViewSet.as_view({"get": "list"})
company_create = CompanyViewSet.as_view({"post": "create"})
company_update = CompanyViewSet.as_view({"put": "update"})
companybank_create = CompanyViewSet.as_view({"post": "create"})
