"""Vendor Performance APIView api."""
from rest_framework import generics
from rest_framework.response import Response
from vendor.models import HistoricalPerformance
from rest_framework import status
from vendor.serializers import HistoricalPerformanceSerializer

class VendorPerformanceAPIView(generics.RetrieveAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer

    def get(self, request, vendor_id):
        try:
            vendor_performance = HistoricalPerformance.objects.get(vendor_id=vendor_id)
            serializer = self.get_serializer(vendor_performance)
            data = serializer.data
            data['message'] = "Vendor performance metrics retrieved successfully"
            return Response(data)
        except HistoricalPerformance.DoesNotExist:
            return Response({"message": "Vendor performance metrics not found"}, status=status.HTTP_404_NOT_FOUND)
