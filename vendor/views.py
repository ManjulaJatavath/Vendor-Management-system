
        











































# def home(request):
#     authentication_classes= [TokenAuthentication]
#     Permission_classes = [IsAuthenticated]
#     return render(request, 'home.html')

# def vendor_list(request):
#     vendors = Vendors.objects.all()

#     vendor_details = {}
#     for vendor in vendors:
#         detail_url = reverse('vendor_detail', kwargs={'pk': vendor.pk})
#         vendor_details[vendor] = detail_url

#     return render(request, 'vendor_list.html', {'vendor_details': vendor_details})

# def vendor_detail(request, pk):
#     vendor = get_object_or_404(Vendors, pk=pk)
#     return render(request, 'vendor_detail.html', {'vendor': vendor})

# def purchase_order_list(request):
#     purchase_orders = PurchaseOrder.objects.all()
#     return render(request, 'purchase_order_list.html', {'purchase_orders': purchase_orders})