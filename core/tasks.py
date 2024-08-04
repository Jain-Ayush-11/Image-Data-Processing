from django.db import transaction
from celery import shared_task
from core.enums import RequestStatus
from core.models import CSVRequest
from core.services import CSVProcessService, WebhookService

@shared_task
def process_pending_requests():
    """
    Periodic task to process pending CSV requests.
    """
    pending_requests = CSVRequest.objects.filter(status=RequestStatus.PENDING)
    
    for request in pending_requests:
        # Lock the individual request to prevent revert of all success cases as well in case of a single Failure
        with transaction.atomic():
            request = CSVRequest.objects.select_for_update().get(id=request.id)
            
            if request.status == RequestStatus.PENDING:
                # Update the request status to PROCESSING
                request.status = RequestStatus.PROCESSING
                request.save()
                
                # process the request for ouput csv generation
                process_status = CSVProcessService.process_request(request=request)
                if not process_status:
                    # TODO: Replace print with error log statement
                    print(f"Failed in processing of request with id {request.id}")

                try:
                    WebhookService.send_payload_to_webhook(request_obj=request)
                except Exception as e:
                    # TODO: Replace with log
                    print(e)


@shared_task
def reconcile_failed_requests():
    """
    Reconciliation task to process failed CSV requests.
    """
    pending_requests = CSVRequest.objects.filter(status=RequestStatus.FAILED)
    
    for request in pending_requests:
        # Lock the individual request to prevent revert of all success cases as well in case of a single Failure
        with transaction.atomic():
            request = CSVRequest.objects.select_for_update().get(id=request.id)
            
            if request.status == RequestStatus.FAILED:
                # Update the request status to PROCESSING
                request.status = RequestStatus.PROCESSING
                request.save()
                
                # process the request for ouput csv generation
                CSVProcessService.process_request(request=request)

