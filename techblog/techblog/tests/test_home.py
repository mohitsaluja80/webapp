from django.test import TestCase, RequestFactory
from django.shortcuts import render
from web.models import service, address
from techblog.views import home
import unittest
from django.test import Client
from unittest.mock import Mock
import json


c = Client()

class HomeViewTestCase(TestCase):
    def test_home_view(self):
        response = c.post('')
        self.assertEqual(200, response.status_code)

        self.assertHTMLEqual(     
                '<p>mohit.saluja@gmail.com</p>',
                '<p>mohit.saluja@gmail.com</p>'              
        )
        self.assertHTMLEqual(     
                '<h1>Cloudmesh<span>.</span></h1>',
                '<h1>Cloudmesh<span>.</span></h1>'              
        )
    def test_blogs_view(self):
        response = c.post('/blogs/')
        self.assertEqual(200, response.status_code)



if __name__ == '__main__':
    unittest.main()


# class HomeViewTestCase(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
        
#         # Create some sample data
#         self.service1 = service.objects.create(service_name='Service 1')
#         self.service2 = service.objects.create(service_name='Service 2')
#         self.address1 = address.objects.create(website_name='City 1')
#         self.address2 = address.objects.create(website_name='City 2')

#     def test_home_view(self):
#         request = self.factory.get('/')
        
#         # Call the home view
#         response = home(request)
        
#         # Check that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)
        
#         print(f"print...{response.status_code}")
#         # Check that the correct template is used
#         # self.assertTemplateUsed(response, 'index.html')
        
#         # Check that the data passed to the template is correct
#         expected_data = {
#             'serviceData': [self.service1, self.service2],
#             'addressData': [self.address1, self.address2]
#         }
#         self.assertDictEqual(response.content, expected_data)

# if __name__ == '__main__':
#     unittest.main()
