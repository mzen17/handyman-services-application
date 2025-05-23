from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
import traceback
from django.contrib.auth.models import User
from hsabackend.models.organization import Organization
from hsabackend.models.customer import Customer
from hsabackend.models.job import Job
from datetime import date
from decimal import Decimal
from hsabackend.models.discount_type import DiscountType
from hsabackend.models.invoice import Invoice

def add_users():
    User.objects.create_user("devuser", "dev@uiowa.edu", "SepTeam003!")
    User.objects.create_user("testuser", "test@uiowa.edu", "SepTeam003!")
    usr  = User.objects.first()
    usr1  = User.objects.last()
    return usr,usr1

def add_orgs(u1,u2):
    org = Organization.objects.create(
        org_name = "devorg",
        org_email = "org@org.dev",
        org_city = "Iowa City",
        org_requestor_state = "Iowa",
        org_requestor_zip = "52240",
        org_requestor_address = "123 main st",
        org_owner_first_name = "Dev",
        org_owner_last_name = "User",
        owning_User = u1,
        org_phone = "1234567890",
        is_onboarding = False
        )
    org1 = Organization.objects.create(
        org_name = "testorg",
        org_email = "org1@org1.dev",
        org_city = "Iowa City",
        org_requestor_state = "Iowa",
        org_requestor_zip = "52240",
        org_requestor_address = "123 main st",
        org_owner_first_name = "Test",
        org_owner_last_name = "User",
        owning_User = u2,
        org_phone = "1234567890"
        )
    return org,org1

def add_customers(org1,org2):
    c1 = Customer.objects.create(
        first_name=f"Firstorg1",
        last_name=f"Lastorg1",
        email=f"custorg1@example.com",
        phone_no=f"1234567890",
        notes=f"Sample notes for user customer org1",
        organization=org1
    )
    c2 = Customer.objects.create(
        first_name=f"Firstorg2",
        last_name=f"Lastorg2",
        email=f"custorg1@example.com",
        phone_no=f"0987654321",
        notes=f"Sample notes for user customer org2",
        organization=org2
    )
    return c1,c2

def add_jobs(c1,o1):
    j1 = Job.objects.create(
        job_status='completed',
        start_date=date(2025, 3, 20),
        end_date=date(2025, 3, 27),
        description="description j1",
        organization=o1,
        customer=c1,
        requestor_city = "Iowa City",
        requestor_state = "Iowa",
        requestor_zip = "52240",
        requestor_address = "2 W Washington St",
        flat_fee = 50.00,
        hourly_rate = 100.00,
        minutes_worked = 30
    )
    j2 = Job.objects.create(
        job_status='completed',
        start_date=date(2025, 3, 20),
        end_date=date(2025, 3, 27),
        description="description j2",
        organization=o1,
        customer=c1,
        requestor_city = "Iowa City",
        requestor_state = "Iowa",
        requestor_zip = "52240",
        requestor_address = "2 W Washington St",
        flat_fee = 0.00,
        hourly_rate = 50.00,
        minutes_worked = 100
    )
    return j1,j2

def add_discount(o1):
    d = DiscountType.objects.create(
        discount_name="Holiday Sale",
        discount_percent=Decimal(20.00),
        organization=o1
    )
    return d
class Command(BaseCommand):
    """Seeds the database with deterministic test data. Used for integration tests"""

    def handle(self, *args, **options):
        try:
            call_command('flush', interactive=False) # truncates all tables
        except CommandError as e:
            self.stdout.write(self.style.ERROR(f'Error flushing the database: {e}'))
        try:
            u1,u2 = add_users()
            o1,o2 = add_orgs(u1,u2)
            c1,c2 = add_customers(o1,o2)
            j1,j2 = add_jobs(c1,o1)
            d = add_discount(o1)

            
        except Exception as e:
            stack_trace = traceback.format_exc()
            self.stdout.write(self.style.ERROR(f'Error seeding the database: {e}\n{stack_trace}'))
        