from django.db import models
from django.core.exceptions import ValidationError



class Vendors(models.Model):
    name = models.CharField(max_length=100)
    phone = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.po_number
    
    def validate_po_number(value):
        if not value.isalnum():
            raise ValidationError("PO number must be alphanumeric.")


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()


    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
    
    
    def calculate_on_time_delivery_rate(self):

        completed_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            status='completed',
            delivery_date__lte=models.F('acknowledgment_date')
        )
        total_completed_orders = completed_orders.count()
        if total_completed_orders == 0:
            return 0.0
        on_time_delivery_orders = completed_orders.filter(
            delivery_date__lte=models.F('acknowledgment_date')
        )
        on_time_delivery_rate = (on_time_delivery_orders.count() / total_completed_orders) * 100
        return on_time_delivery_rate

    def calculate_quality_rating_avg(self):

        completed_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor, status='completed', quality_rating__isnull=False
        )
        total_orders = completed_orders.count()
        if total_orders == 0:
            return 0.0
        total_ratings = sum(order.quality_rating for order in completed_orders)
        return total_ratings / total_orders

    def calculate_average_response_time(self):

        completed_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor, status='completed', acknowledgment_date__isnull=False
        )
        total_orders = completed_orders.count()
        if total_orders == 0:
            return 0.0
        total_time = sum((order.acknowledgment_date - order.issue_date).total_seconds() for order in completed_orders)
        return total_time / total_orders
    
    def calculate_fulfillment_rate(self):
        
        total_orders = PurchaseOrder.objects.filter(vendor=self.vendor).count()
        if total_orders == 0:
            return 0.0
        fulfilled_orders = PurchaseOrder.objects.filter(vendor=self.vendor, status='completed').count()
        return (fulfilled_orders / total_orders) * 100

