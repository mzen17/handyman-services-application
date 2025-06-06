from django.test import TestCase
from hsabackend.models.service import Service
from hsabackend.models.job import Job
from hsabackend.models.job_service import JobService

class JobServiceModelTest(TestCase):

    def setUp(self):
        self.service = Service(
            service_name='Test Service',
            service_description='This is a test service.'
        )
        self.job = Job()
        
        self.job_service = JobService(
            job=self.job,
            service=self.service
        )

    
    def test_json_method(self):
        expected_json = {
            'id': self.job_service.pk,
            'serviceID': self.service.id,
            'serviceName': self.service.service_name,
            'serviceDescription': self.service.service_description
        }
        
        self.assertEqual(self.job_service.json(), expected_json)

    def test_get_service_info_for_detailed_invoice_method(self):
        expected_service_info = {
            "service name": self.service.service_name,
            "service description": self.service.service_description
        }
        
        self.assertEqual(self.job_service.get_service_info_for_detailed_invoice(), expected_service_info)
