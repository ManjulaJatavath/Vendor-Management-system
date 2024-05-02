from django.urls import path
from vendor.api.register_api import RegisterUser
from vendor.api.vendors_api import  VendorsCreateAPI, VendorsDetailAPI, VendorsListAPI
from vendor.api.purchase_order_api import  AcknowledgePurchaseOrderAPIView, PurchaseOrdersAPI, PurchaseOrdersListAPI
from vendor.api.historical_performance_api import VendorPerformanceAPIView


urlpatterns = [
    path('api/register/', RegisterUser.as_view(),name='user_rigister'),
    path('api/vendors/', VendorsListAPI.as_view(), name='vendors_list'),
    path('api/vendor/', VendorsCreateAPI.as_view(), name='vendor'),
    path('api/vendors/<int:vendor_id>/', VendorsDetailAPI.as_view(), name='vendors_detail'),
    path('api/vendors_performance/<int:vendor_id>/', VendorPerformanceAPIView.as_view(), name='vendor_performance'),
    path('api/purchase_orders/', PurchaseOrdersListAPI.as_view(), name='purchase_orders_list'),
    path('api/purchase_orders/<int:po_id>/', PurchaseOrdersAPI.as_view(), name='purchase_orders_detail'),
    path('api/acknowledge_purchase_order/<int:po_id>/', AcknowledgePurchaseOrderAPIView.as_view(), name='acknowledge_purchase_order'),


]


# urlpatterns = [
#     path('register/', views.RegisterUser.as_view()),
#     path('api/vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
#     path('api/vendors/<int:pk>/', VendorRetrieveUpdateDeleteView.as_view(), name='vendor-retrieve-update-delete'),
#     path('api/purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase-order-list-create'),
#     path('api/purchase_orders/<int:pk>/', PurchaseOrderRetrieveUpdateDeleteView.as_view(), name='purchase-order-retrieve-update-delete'),
#     path('api/historical_performance/', HistoricalPerformanceListCreateView.as_view(), name='historical-performance-list-create'),
#     path('api/vendors/<int:vendor_id>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),
#     path('api/purchase_orders/<int:pk>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge-purchase-order'),
#     ]
