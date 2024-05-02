"""Purchase Oder api."""

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from vendor.models import PurchaseOrder
from vendor.serializers import PurchaseOrderSerializer


class PurchaseOrdersListAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        vender_id = request.query_params.get('vender_id')
        if vender_id:
            purchase_order = PurchaseOrder.objects.filter(vender_id=vender_id)
        else:
            purchase_order=PurchaseOrder.objects.all()
        serializer=PurchaseOrderSerializer(purchase_order, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PurchaseOrdersAPI(APIView):
    def get(self, request, po_id):
        if po_id:
            try:
                purchase_order = PurchaseOrder.objects.get(id=po_id)
                serializer = PurchaseOrderSerializer(purchase_order)
                return Response(serializer.data)
            except PurchaseOrder.DoesNotExist:
                return Response({"error": "Purchase Order not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            if 'vendor_id' in request.query_params:
                vendor_id = request.query_params['vendor_id']
                purchase_orders = PurchaseOrder.objects.filter(vendor_id=vendor_id)
            else:
                purchase_orders = PurchaseOrder.objects.all()
            serializer = PurchaseOrderSerializer(purchase_orders, many=True)
            return Response(serializer.data)

    def put(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(id=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase Order not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Purchase Order successfully updated", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, po_id=None):
        if po_id:
            try:
                purchase_order = PurchaseOrder.objects.get(id=po_id)
                purchase_order.delete()
                return Response({"message": "Purchase Order successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
            except PurchaseOrder.DoesNotExist:
                return Response({"error": "Purchase Order not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Purchase Order ID is required for deletion"}, status=status.HTTP_400_BAD_REQUEST)

class AcknowledgePurchaseOrderAPIView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def post(self, request, po_id):
        try:
            instance = self.get_queryset().get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase Order not found"}, status=status.HTTP_404_NOT_FOUND)

        acknowledgment_date = request.data.get('acknowledgment_date')

        if acknowledgment_date:
            instance.acknowledgment_date = acknowledgment_date
            instance.save()

            instance.vendor.calculate_average_response_time()

            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Acknowledgment date is required"}, status=status.HTTP_400_BAD_REQUEST)

