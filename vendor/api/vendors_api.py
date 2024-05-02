""" Vendors api."""

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from vendor.models import Vendors
from vendor.serializers import VendorsSerializer


    
class VendorsCreateAPI(APIView): 
    def post(self, request):
        serializer = VendorsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Vendor successfully created", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorsListAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        vendors=Vendors.objects.all()
        serializer=VendorsSerializer(vendors, many=True)
        return Response({"message": "Vendors successfully retrieved", "data": serializer.data})

class VendorsDetailAPI(APIView):
    def get(self, request, vendor_id):
            try:
                vendor = Vendors.objects.get(id=vendor_id)
                serializer = VendorsSerializer(vendor)
                return Response(serializer.data)
            except Vendors.DoesNotExist:
                return Response({"message": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, vendor_id):
        try:
            vendor = Vendors.objects.get(id=vendor_id)

        except Vendors.DoesNotExist:
            return Response({"message":"Vender not found"}, status=status.HTTP_204_NO_FOUND)

        serializer = VendorsSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Vendor successfully updated", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request, vendor_id):
        try:
            vendor=Vendors.objects.get(id=vendor_id)
        except Vendors.DoesNotExist:
               return Response({"message": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND) 
    
        vendor.delete()
        return JsonResponse({"message": "Vendor successfully deleted"},status=status.HTTP_204_NO_CONTENT)

