from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponseNotFound
import hsabackend.views.index as hview
from hsabackend.views.user_auth import login_view, logout_view, user_create, user_exist
from hsabackend.views.customers import get_customer_excluded_table_data, get_customer_table_data, create_customer, edit_customer, delete_customer
from hsabackend.views.contractors import (
    get_contractor_excluded_table_data,
    get_contractor_table_data,
    create_contractor,
    edit_contractor,
    delete_contractor,
    get_all_contractors_for_org,
)
from hsabackend.views.requests import (
    get_filtered_request_data, 
    get_individual_request_data, 
    delete_request,
    approve_request,
    create_request,
)
from hsabackend.views.services import get_service_table_data, get_service_excluded_table_data, create_service, edit_service, delete_service
from hsabackend.views.materials import get_material_excluded_table_data, get_material_table_data, create_material, edit_material, delete_material
from hsabackend.views.invoices import createInvoice, getInvoices, deleteInvoice, updateInvoice, get_data_for_invoice
from hsabackend.views.jobs import get_job_excluded_table_data, get_job_table_data, get_job_individual_data, create_job, edit_job, delete_job, get_jobs_by_contractor, get_invoicable_jobs, get_invoicable_jobs_per_invoice
from hsabackend.views.jobs_services import get_job_service_table_data, create_job_service, delete_job_service, delete_cached_job_service
from hsabackend.views.jobs_materials import get_job_material_table_data, create_job_material, delete_job_material, delete_cached_job_material
from hsabackend.views.jobs_contractors import get_job_contractor_table_data, create_job_contractor, delete_job_contractor, delete_cached_job_contractor
from hsabackend.views.job_templates import get_job_template_table_data, get_job_template_individual_data, create_job_template, edit_job_template, delete_job_template
from hsabackend.views.job_templates_services import get_job_template_service_table_data, create_job_template_service, delete_job_template_service, delete_cached_job_template_service
from hsabackend.views.job_templates_materials import get_job_template_material_table_data, create_job_template_material, delete_job_template_material, delete_cached_job_template_material
from hsabackend.views.invoices import createInvoice, getInvoices, deleteInvoice, updateInvoice
from hsabackend.views.generate_invoice_pdf_view import generate_pdf
from hsabackend.views.generate_quote_pdf_view import generate_quote_pdf, send_quote_pdf_to_customer_email, generate_quote_pdf_as_base64, sign_the_quote, get_list_of_quotes_by_org, retrieve_quote, accept_reject_quote
from hsabackend.views.organizations import complete_onboarding, createOrganization, getOrganizationDetail, editOrganizationDetail, get_payment_link, set_payment_link
from hsabackend.views.generate_requests_iframe import getHTMLForm
from hsabackend.views.discounts import get_discounts, edit_discount, create_discount, delete_discount
from hsabackend.views.bookings import create_event, delete_event, edit_event, get_booking_data, get_ical_for_bookings
from django.http import HttpResponse

def handle_unmatched_api(request):
    return HttpResponseNotFound("404 Not Found")

def handle_health_check(request):
    return HttpResponse("OK", content_type="text/plain", status=200)

urlpatterns = [
    path('admin/', admin.site.urls),

    # health check (used for int testing)
    path("api/healthcheck", handle_health_check),

    # auth
    path("api/login", login_view),
    path("api/logout", logout_view),
    path("api/create/user", user_create),
    path("api/userexist", user_exist),

    # customer
    path("api/get/customers", get_customer_table_data),
    path("api/get/customers/exclude", get_customer_excluded_table_data),
    path("api/create/customer", create_customer),
    path("api/edit/customer/<int:id>", edit_customer),
    path("api/delete/customer/<int:id>", delete_customer),

    # contractor
    path("api/get/all/contractors", get_all_contractors_for_org),
    path("api/get/contractors", get_contractor_table_data),
    path("api/get/contractors/exclude", get_contractor_excluded_table_data),
    path("api/create/contractor", create_contractor),
    path("api/edit/contractor/<int:id>", edit_contractor),
    path("api/delete/contractor/<int:id>", delete_contractor),

    # request
    path("api/get/requests/filter", get_filtered_request_data),
    path("api/get/request/<int:id>", get_individual_request_data),
    path("api/delete/request/<int:id>", delete_request),
    path("api/create/request/<int:id>", create_request),
    path("api/approve/request/<int:id>", approve_request),
    path("api/request/genhtml/<int:id>", getHTMLForm),

    # service 
    path("api/get/services", get_service_table_data),
    path("api/get/services/exclude", get_service_excluded_table_data),
    path("api/create/service", create_service),
    path("api/edit/service/<int:id>", edit_service),
    path("api/delete/service/<int:id>", delete_service),

    # materials
    path("api/get/materials", get_material_table_data),
    path("api/get/materials/exclude", get_material_excluded_table_data),
    path("api/create/material", create_material),
    path("api/edit/material/<int:id>", edit_material),
    path("api/delete/material/<int:id>", delete_material),

    # jobs
    path("api/get/jobs", get_job_table_data),
    path("api/get/invoicable/jobs", get_invoicable_jobs),
    path("api/get/jobs/exclude", get_job_excluded_table_data),
    path("api/get/job/<int:id>", get_job_individual_data),
    path("api/create/job", create_job),
    path("api/edit/job/<int:id>", edit_job),
    path("api/delete/job/<int:id>", delete_job),
    path("api/get/jobs/by-contractor", get_jobs_by_contractor),
    path("api/get/jobs/for-invoice", get_invoicable_jobs_per_invoice),

    # jobs_services join
    path("api/get/job/<int:id>/services", get_job_service_table_data),
    path("api/create/job/<int:id>/service", create_job_service),
    path("api/delete/job/<int:job_id>/service/<int:job_service_id>", delete_job_service),
    path("api/delete/job/<int:job_id>/services", delete_cached_job_service),

    # jobs_materials join
    path("api/get/job/<int:id>/materials", get_job_material_table_data),
    path("api/create/job/<int:id>/material", create_job_material),
    path("api/delete/job/<int:job_id>/material/<int:job_material_id>", delete_job_material),
    path("api/delete/job/<int:job_id>/materials", delete_cached_job_material),

    # jobs_contractors join
    path("api/get/job/<int:id>/contractors", get_job_contractor_table_data),
    path("api/create/job/<int:id>/contractor", create_job_contractor),
    path("api/delete/job/<int:job_id>/contractor/<int:job_contractor_id>", delete_job_contractor),
    path("api/delete/job/<int:job_id>/contractors", delete_cached_job_contractor),
    
    # quote
    path("api/generate/quote/<int:id>", generate_quote_pdf),
    path('api/ret/quote', generate_quote_pdf_as_base64),
    path('api/quote/sign', sign_the_quote),

    # job_templates
    path("api/get/jobtemplates", get_job_template_table_data),
    path("api/get/jobtemplate/<int:id>", get_job_template_individual_data),
    path("api/create/jobtemplate", create_job_template),
    path("api/edit/jobtemplate/<int:id>", edit_job_template),
    path("api/delete/jobtemplate/<int:id>", delete_job_template),

    # job_templates_services join
    path("api/get/jobtemplate/<int:id>/services", get_job_template_service_table_data),
    path("api/create/jobtemplate/<int:id>/service", create_job_template_service),
    path("api/delete/jobtemplate/<int:job_template_id>/service/<int:job_template_service_id>", delete_job_template_service),
    path("api/delete/jobtemplate/<int:job_template_id>/services", delete_cached_job_template_service),

    # job_templates_materials join
    path("api/get/jobtemplate/<int:id>/materials", get_job_template_material_table_data),
    path("api/create/jobtemplate/<int:id>/material", create_job_template_material),
    path("api/delete/jobtemplate/<int:job_template_id>/material/<int:job_template_material_id>", delete_job_template_material),
    path("api/delete/jobtemplate/<int:job_template_id>/materials", delete_cached_job_template_material),

    # invoices
    path("api/create/invoice", createInvoice),
    path("api/get/invoices", getInvoices),
    path("api/delete/invoice/<int:id>", deleteInvoice),
    path("api/edit/invoice/<int:id>", updateInvoice),
    path("api/generate/invoice/<int:id>", generate_pdf),
    path("api/get/invoice/displaydata/<int:id>", get_data_for_invoice),
    
    
    
    # orgs
    path("api/create/organization", createOrganization),
    path("api/get/organization", getOrganizationDetail),
    path("api/edit/organization", editOrganizationDetail),
    path("api/edit/organization/onboarding", complete_onboarding),
    path("api/get/payment-link", get_payment_link),
    path("api/set/payment-link", set_payment_link),

    # quotes
    path("api/send/quote/<int:id>", send_quote_pdf_to_customer_email),
    path("api/manage/quote/<int:id>", accept_reject_quote),
    path('api/get/quotes', get_list_of_quotes_by_org),
    path("api/render/quote/<int:id>", retrieve_quote),

    # discounts
    path("api/get/discounts", get_discounts),
    path("api/edit/discount/<int:id>", edit_discount),
    path("api/create/discount", create_discount),
    path("api/delete/discount/<int:id>", delete_discount),

    # bookings
    path("api/get/bookings", get_booking_data),
    path("api/create/booking", create_event),
    path("api/edit/booking/<int:id>", edit_event),
    path("api/delete/booking/<int:id>", delete_event),
    path("api/icals/booking", get_ical_for_bookings),

    # password reset
    re_path(r'^api/password_reset/', include('hsabackend.utils.password_reset_route_adder', namespace='password_reset')),

    # Catch-all for unmatched API requests
    re_path(r'^api/.*', handle_unmatched_api), 

    # all non API routes should redirect to angular
    # must be at the bottom!!!
    re_path(r'.*', hview.main_view)   
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
