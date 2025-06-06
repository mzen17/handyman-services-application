from rest_framework.test import APIRequestFactory
from rest_framework import status
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.db.models import QuerySet
from django.db.models import Q
from unittest.mock import call
from django.core.exceptions import ValidationError
from hsabackend.views.organizations import complete_onboarding, createOrganization, deleteOrganization, getOrganizationDetail, editOrganizationDetail, get_payment_link, set_payment_link
from hsabackend.models.organization import Organization
from hsabackend.models.customer import Customer
from hsabackend.models.service import Service
from hsabackend.models.material import Material
from hsabackend.models.contractor import Contractor
from hsabackend.models.job import Job
from hsabackend.models.job_service import JobService
from hsabackend.models.job_material import JobMaterial
from hsabackend.models.job_contractor import JobContractor

class orgViewTests(APITestCase):
    def test_unauth_user_attacks_all_endpoints(self):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = False
        factory = APIRequestFactory()

        # get org test
        request = factory.get('/api/get/organization')
        request.user = mock_user  
        response = getOrganizationDetail(request)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # create organization test
        request = factory.post('/api/create/organization')
        request.user = mock_user  
        response = createOrganization(request)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # edit organization test
        request = factory.post('/api/edit/organization')
        request.user = mock_user  
        response = editOrganizationDetail(request)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # delete organization test
        request = factory.post('/api/delete/organization')
        request.user = mock_user  
        response = deleteOrganization(request)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('hsabackend.views.organizations.Organization.objects.get')
    def test_auth_org_retrive_works(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        factory = APIRequestFactory()

        org_object = MagicMock(spec=Organization)
        org.json.return_value = {}
        org.return_value = org_object

        request = factory.get('api/get/organization')
        request.user = mock_user
        response = getOrganizationDetail(request)
        
        assert response.status_code == status.HTTP_200_OK

    @patch('hsabackend.utils.auth_wrapper.Organization')
    @patch('hsabackend.views.organizations.Organization')
    def test_create_org_if_auth_and_valid(self, org1,org2):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        factory = APIRequestFactory()

        org_object = MagicMock(spec=Organization)
        manager = MagicMock()
        org1.objects = manager
        manager.get.return_value = org_object

        obj = MagicMock(name='obj')
        org1.return_value = obj

        manager1 = MagicMock()
        org2.objects = manager1


        qs = MagicMock(spec=QuerySet)
        manager.filter.return_value = qs
        qs.count.return_value = 0

        mock_data = {
            "name": "Superman HQ",
            "email": "supermanHQ@supermanHQ.co",
            "city": "BobTown",
            "requestor_state": "Iowa",
            "requestor_zip": "52213",
            "requestor_address": "222 Box",
            "ownerFn": "Dov",
            "ownerLn": "Sob"
        }

        request = factory.post('api/create/organization', data=mock_data, format='json')
        request.user = mock_user
        response = createOrganization(request)

        

        obj.save.assert_called_once()
        
        assert response.status_code == status.HTTP_201_CREATED


    @patch('hsabackend.views.organizations.Organization.objects.filter')
    @patch('hsabackend.views.organizations.Organization.objects.get')
    def test_create_org_fail_if_already_has_org(self, org, filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        factory = APIRequestFactory()

        org_object = MagicMock(spec=Organization)
        org.return_value = org_object

        qs = MagicMock(spec=QuerySet)
        qs.count.return_value = 1 # no prev account
        filter.return_value = qs

        request = factory.post('api/create/organization', format='json')
        request.user = mock_user
        response = createOrganization(request)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get('errors', '') == "This user already has an organization"


    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    @patch('hsabackend.views.organizations.Organization')
    def test_create_org_fail_if_missing_data(self, org_construct, auth_org):
        mock_user = MagicMock(spec=User)
        mock_user.is_authenticated = True

        org = Organization()
        org.is_onboarding = False
        auth_org.return_value = org

        factory = APIRequestFactory()

        qs = MagicMock(spec=QuerySet, name="filter qs")
        qs.count.return_value = 0

        manager = MagicMock(name="manager")

        org_construct.objects = manager
        manager.filter.return_value = qs

        # Mock instance
        org_instance = MagicMock()
        org_construct.return_value = org_instance
        org_instance.full_clean.side_effect = ValidationError({'email': ['This field is required.']})

        mock_data = {
            "city": "BobTown",
            "requestor_state": "Iowa",
            "requestor_zip": "52213",
            "requestor_address": "222 Box",
            "ownerLn": "Sob"
        }

        request = factory.post('api/create/organization', data=mock_data, format='json')
        request.user = mock_user
        response = createOrganization(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get('errors', '') == {'email': ['This field is required.']}


    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_edit_org_succeeds(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        factory = APIRequestFactory()

        org_object = MagicMock(spec=Organization)
        org_object.is_onboarding = False
        org.return_value = org_object

        mock_data = {
            "name": "Superman HQ",
            "email": "supermanHQ@supermanHQ.co",
            "city": "BobTown",
            "requestor_address": "222 Box",
            "ownerFn": "Dov",
            "ownerLn": "Sob",
            "is_onboarding": False,
        }

        request = factory.post('api/edit/organization', data=mock_data, format='json')
        request.user = mock_user
        request.org = org_object
        response = editOrganizationDetail(request)
        org_object.save.assert_called_once()
        
        assert response.status_code == status.HTTP_200_OK


    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_edit_org_fail_if_bogus_param(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        factory = APIRequestFactory()

        org_object = MagicMock(spec=Organization, name="Org")
        org_object.is_onboarding = False
        org.return_value = org_object
        org_object.full_clean.side_effect = ValidationError({'email': ['Invalid Email']})

        mock_data = {
            "name": "Superman HQ",
            "email": "oofemail",
            "city": "BobTown",
            "requestor_address": "222 Box",
            "ownerFn": "Dov",
            "ownerLn": "Sob"
        }

        request = factory.post('api/edit/organization', data=mock_data, format='json')
        request.user = mock_user
        response = editOrganizationDetail(request)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("errors", "") == {'email': ['Invalid Email']}


    @patch('hsabackend.views.organizations.Organization.objects.filter')
    @patch('hsabackend.views.organizations.Organization')
    def test_delete_org_fails(self, org, filter):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        factory = APIRequestFactory()

        org_object = MagicMock(spec=Organization)
        org.return_value = org_object

        qs = MagicMock(spec=QuerySet)
        qs.count.return_value = 0 # no prev account
        filter.return_value = qs

        request = factory.post('api/delete/organization', format='json')
        request.user = mock_user
        response = deleteOrganization(request)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get('errors', '') == "All users must have at least 1 org; You only have 1 or less orgs, cannot delete."

    @patch('hsabackend.views.organizations.Organization')
    @patch('hsabackend.views.organizations.Organization.objects.get')
    def test_onboarding_already_done(self, get_org, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True

        mock_org = Mock(spec=Organization)
        mock_org.is_onboarding = False  # Trigger the 400 case
        get_org.return_value = mock_org
        org.objects = Mock(get=get_org)

        factory = APIRequestFactory()
        request = factory.post('api/edit/organization/onboarding', format='json')
        request.user = mock_user

        response = complete_onboarding(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "Already onboarded"

    @patch('hsabackend.views.organizations.Customer')
    @patch('hsabackend.views.organizations.Organization.objects.get')
    def test_onboarding_invalid(self, get_org, customer):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_org = Mock(spec=Organization)
        get_org.return_value = mock_org
    
        mock_customer = MagicMock(spec=Customer)
        customer.return_value = mock_customer

        mock_data = {
            "isOnboarding": False,
        }

        factory = APIRequestFactory()
        request = factory.post('api/edit/organization/onboarding', data=mock_data, format='json')
        request.user = mock_user
        response = complete_onboarding(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @patch('hsabackend.views.organizations.JobContractor')
    @patch('hsabackend.views.organizations.JobMaterial')
    @patch('hsabackend.views.organizations.JobService')
    @patch('hsabackend.views.organizations.Job')
    @patch('hsabackend.views.organizations.Contractor')
    @patch('hsabackend.views.organizations.Material')
    @patch('hsabackend.views.organizations.Service')
    @patch('hsabackend.views.organizations.Customer')
    @patch('hsabackend.views.organizations.Organization.objects.get')
    def test_onboarding_succeeds(self, get_org, customer, service, material, contractor, job, job_service, job_material, job_contractor):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_org = Mock(spec=Organization)
        get_org.return_value = mock_org

        def mock_model(model):
            instance = MagicMock(spec=model)
            instance.full_clean = Mock()
            instance.save = Mock()
            return instance
    
        mock_customer = mock_model(Customer)
        customer.return_value = mock_customer
        mock_service = mock_model(Service)
        service.return_value = mock_service
        mock_material = mock_model(Material)
        material.return_value = mock_material
        mock_contractor = mock_model(Contractor)
        contractor.return_value = mock_contractor
        mock_job = mock_model(Job)
        mock_job.customer = mock_customer
        job.return_value = mock_job
        mock_job_service = mock_model(JobService)
        mock_job_service.job = mock_job
        mock_job_service.service = mock_service
        job_service.return_value = mock_job_service
        mock_job_material = mock_model(JobMaterial)
        mock_job_material.job = mock_job
        mock_job_material.material = mock_material
        job_material.return_value = mock_job_material
        mock_job_contractor = mock_model(JobContractor)
        mock_job_contractor.job = mock_job
        mock_job_contractor.contractor = mock_contractor
        job_contractor.return_value = mock_job_contractor

        mock_data = {
            "isOnboarding": False,
            "customerRequest": {
                'firstn': 'John',
                'lastn': 'Doe',
                'email': 'john.doe@example.com',
                'phoneno': '',
                'notes': 'Sample note for testing purposes.'
            },
            "serviceRequest": {
                'service_name': 'Mow Lawn',
                'service_description': 'Mowing the Lawn'
            },
            "materialRequest": {
                'material_name': 'Test Material',
            },
            "contractorRequest": {
                'firstName': 'FirstCon',
                'lastName': 'LastCon',
                'email': 'firstcon.lastcon@test.com',
                'phone': '',
            },
            "jobRequest": {
                "startDate": "2026-01-02",
                "endDate": "2026-02-02",
                "description": "Test Job",
                "customerID": 1,
                "city": "Test City",
                "state": "Iowa",
                "zip": "99999",
                "address": "Test Address",
                "contractors": [
                    { 
                        "id": 2
                    }
                ],
                "services": [
                    {
                        "id": 2
                    }
                ],
                "materials": [
                    {
                        "id": 2,
                        "unitsUsed": 0,
                        "pricePerUnit": 0.00
                    },
                ]
            }
        }

        factory = APIRequestFactory()
        request = factory.post('api/edit/organization/onboarding', data=mock_data, format='json')
        request.user = mock_user
        response = complete_onboarding(request)

        assert response.status_code == status.HTTP_200_OK
        mock_customer.save.assert_called_once()
        mock_service.save.assert_called_once()
        mock_material.save.assert_called_once()
        mock_contractor.save.assert_called_once()
        mock_job.save.assert_called_once()
        mock_job_service.save.assert_called_once()
        mock_job_material.save.assert_called_once()
        mock_job_contractor.save.assert_called_once()
        mock_org.save.assert_called_once()

class GetPaymentLintTest(APITestCase):
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_none_payment_url(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_org = Mock(spec=Organization)
        mock_org.is_onboarding = False
        org.return_value = mock_org
        org.default_payment_url = None

        factory = APIRequestFactory()
        request = factory.get('api/get/payment-link')
        request.user = mock_user

        res = get_payment_link(request)
        assert res.status_code == 200

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_valid_url(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_org = Mock(spec=Organization)
        mock_org.is_onboarding = False
        org.return_value = mock_org
        org.default_payment_url = "http://google.com"

        factory = APIRequestFactory()
        request = factory.get('api/get/payment-link')
        request.user = mock_user

        res = get_payment_link(request)

        assert res.status_code == 200

class TestSetPayment(APITestCase):
    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_no_url(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_org = Mock(spec=Organization)
        org.return_value = mock_org
        mock_org.is_onboarding = False
        factory = APIRequestFactory()
        request = factory.post('api/set/payment-link')
        request.user = mock_user

        res = set_payment_link(request)
        assert res.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_invalid(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_org = Mock(spec=Organization)
        org.return_value = mock_org
        mock_org.is_onboarding = False
        mock_org.full_clean.side_effect = ValidationError({'email': ['This field is required.']})

        factory = APIRequestFactory()
        request = factory.post('api/set/payment-link', data={"url": "://google.com"}, format='json' )
        request.user = mock_user

        res = set_payment_link(request)
        assert res.status_code == 400

    @patch('hsabackend.utils.auth_wrapper.Organization.objects.get')
    def test_ok(self, org):
        mock_user = Mock(spec=User)
        mock_user.is_authenticated = True
        mock_org = Mock(spec=Organization)
        org.return_value = mock_org
        mock_org.is_onboarding = False

        factory = APIRequestFactory()
        request = factory.post('api/set/payment-link', data={"url": "://google.com"}, format='json' )
        request.user = mock_user

        res = set_payment_link(request)
        assert res.status_code == 200
