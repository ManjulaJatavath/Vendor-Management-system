from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from vendor.models import HistoricalPerformance, PurchaseOrder, Vendors
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from datetime import timedelta


class RegistrationAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = 'user'
        self.password = 'password'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)

    def test_for_user_registration(self):
        url = reverse('user_rigister')
        data = {
            'username': 'Manjula',
            'password': '123'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)  
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class VendorsAPITestCase(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)

    def test_for_vendors_list(self):
        url = reverse('vendors_list')
        authorization_header = 'Token ' + self.token.key
        response = self.client.get(url, HTTP_AUTHORIZATION=authorization_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vendors_create(self):
        url = reverse('vendor')
        data = {
            "name":"Manjula",
            "phone":"8897462274",
            "vendor_code": "ABC124"
        }
        authorization_header = 'Token ' + self.token.key
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=authorization_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_vendors_detail(self):
        vendor = Vendors.objects.create(
            name='Manju',
            phone='1234567890',
            address='Hyderabad',
            vendor_code='V456',
        )
        url = reverse('vendors_detail', args=[vendor.id])
        authorization_header = 'Token ' + self.token.key
        response = self.client.get(url, HTTP_AUTHORIZATION=authorization_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class VendorPerformanceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = 'user'
        self.password = 'password'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_retrieve_vendor_performance(self):
        vendor = Vendors.objects.create(
            name='Vendor',
            phone='1234567890',
            address='Address',
            vendor_code='TEST123'
        )
        HistoricalPerformance.objects.create(
            vendor=vendor,
            date= "2024-05-02T07:34:06Z",
            on_time_delivery_rate=95.0,
            quality_rating_avg=4.5,
            average_response_time=24.0,
            fulfillment_rate=98.0
        )
        url = reverse('vendor_performance', args=[vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PurchaseOrderAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='password')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('purchase_orders_list')
        self.valid_data = {
            'po_number': 'PO123',
            'vendor': 1, 
            'order_date': timezone.now(),
            'issue_date': timezone.now(),  
            'delivery_date': timezone.now() + timedelta(days=10),  
            'acknowledgment_date': timezone.now() + timedelta(days=10), 
            'items': {},  # Add items Json Data here it is required
            'quantity': 10,
            'quality_rating': 3,
            'status': 'Pending',
        }

    def test_purchase_order_details_get(self):
        vendor = Vendors.objects.create(name='Vendor')
        purchase_order = PurchaseOrder.objects.create(
            po_number='PO123',
            vendor=vendor,  
            order_date=timezone.now(),
            delivery_date=timezone.now() + timezone.timedelta(days=10),
            issue_date=timezone.now(),
            items={},  # same here json data
            quantity=10,
            status='Pending',
        )
        url = reverse('purchase_orders_detail', args=[purchase_order.id])
        response = self.client.get(url) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class AcknowledgePurchaseOrderAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        vendor = Vendors.objects.create(name="Name")
        self.po = PurchaseOrder.objects.create(
            id=1, 
            vendor=vendor,
            order_date=timezone.now(),  
            delivery_date=timezone.now(),  
            acknowledgment_date=None,
            items={"item1": "description1", "item2": "description2"},
            quantity=19 ,
            status='Pending',
            issue_date=timezone.now()
        )
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

def test_acknowledge_purchase_order(self):
    url = reverse('acknowledge_purchase_order', args=[self.po.id])
    data = {'acknowledgment_date': '2024-05-10T00:00:00Z'} 
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    updated_po = PurchaseOrder.objects.get(id=self.po.id)
    expected_date = datetime.strptime('2024-05-10', '%Y-%m-%d').date()
    self.assertEqual(updated_po.acknowledgment_date.date(), expected_date)
    acknowledgment_date = timezone.make_aware(datetime(2024, 5, 10))
    updated_po.acknowledgment_date = acknowledgment_date
    updated_po.save()