"""Vendors app signals."""
from django.utils import timezone
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import PurchaseOrder, HistoricalPerformance, Vendors



@receiver(post_save, sender=PurchaseOrder)
def update_metrics_on_purchase_orders_save(sender, instance, created, **kwargs):
    """ Signal handler to update metrics when a PurchaseOrder is saved."""
    vendor = instance.vendor

    try:
        historical_performance = HistoricalPerformance.objects.get(vendor=vendor)
    except HistoricalPerformance.DoesNotExist:
        historical_performance = HistoricalPerformance(vendor=vendor) 
        historical_performance.date = timezone.now()   
    historical_performance.on_time_delivery_rate = historical_performance.calculate_on_time_delivery_rate()
    historical_performance.quality_rating_avg = historical_performance.calculate_quality_rating_avg()
    historical_performance.average_response_time = historical_performance.calculate_average_response_time()
    historical_performance.fulfillment_rate = historical_performance.calculate_fulfillment_rate()
    historical_performance.save()

@receiver(post_delete, sender=PurchaseOrder)
def update_metrics_on_purchase_order_delete(sender, instance, **kwargs):
    """ Signal handler to update metrics when a PurchaseOrder is deleted."""
    vendor = instance.vendor
    try:
        historical_performance = HistoricalPerformance.objects.get(vendor=vendor)
    except HistoricalPerformance.DoesNotExist:

        return
    historical_performance.on_time_delivery_rate = historical_performance.calculate_on_time_delivery_rate()
    historical_performance.quality_rating_avg = historical_performance.calculate_quality_rating_avg()
    historical_performance.average_response_time = historical_performance.calculate_average_response_time()
    historical_performance.fulfillment_rate = historical_performance.calculate_fulfillment_rate()
    historical_performance.save()

@receiver(post_save, sender=Vendors)
def vendor_signal(sender, instance, created, **kwargs):
    """ Signal receiver for post-save of vendor instances."""
    cache.clear()
@receiver(post_save, sender=HistoricalPerformance)
def historical_performance_signal(sender, instance, created, **kwargs):
    """Signal receiver for post-save of HistoricalPerformance instances."""
    cache.clear()

