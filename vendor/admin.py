from django.contrib import admin
from vendor.models import HistoricalPerformance, PurchaseOrder, Vendors




class VendorsAdmin(admin.ModelAdmin):
    """ Model Resource for Vendors."""

    list_display = ["name", "phone","vendor_code","is_active","created_at"]
    list_filter = ["name","phone",'is_active', 'created_at']
    search_fields = ["phone","vendor_code"]
admin.site.register(Vendors, VendorsAdmin)



class PurchaseOrderAdmin(admin.ModelAdmin):
    """ Model Admin for PurchaseOrder."""

    list_display = ["po_number", "vendor", "order_date","status","issue_date","delivery_date","is_active","created_at"]
    list_filter = ["vendor__name","status",'is_active', 'created_at']
    search_fields = ['po_number', 'vendor__name']
    date_hierarchy='delivery_date'

admin.site.register(PurchaseOrder, PurchaseOrderAdmin)

class HistoricalPerformanceAdmin(admin.ModelAdmin):
    """ Model Admin for HistoricalPerformance."""

    list_display = ["vendor", "date","on_time_delivery_rate"]
    list_filter = ["vendor","date"]
    search_fields = ["vendor__name"]
admin.site.register(HistoricalPerformance, HistoricalPerformanceAdmin)