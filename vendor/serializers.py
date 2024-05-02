from rest_framework import serializers
from .models import PurchaseOrder, Vendors, HistoricalPerformance
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        """Meta information for User Serializer."""

        model = User
        fields = ('username','password')

    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class VendorsSerializer(serializers.ModelSerializer):
    """Serializer Vendors Model."""

    class Meta:
        """Meta information for Vendors Serializer."""

        model = Vendors
        fields = ['name','phone','vendor_code']


    #         "name":"Ravikuar",
    # "phone":"8897462274", write validate
    # "vendor_code": "ABC124"



class PurchaseOrderSerializer(serializers.ModelSerializer):
    """Serializer for PurchaseOrder Model."""
    class Meta:
        """Meta information for PurchaseOrder Serializer."""
        model = PurchaseOrder
        fields = ["vendor",'po_number', 'order_date', 'delivery_date', 'status','items','quantity','quality_rating','issue_date','acknowledgment_date']





class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    """ Serializer for HistoricalPerformance model."""
    vendor = VendorsSerializer()
    class Meta:
        model = HistoricalPerformance
        fields = ['id', 'vendor', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time']