from django.db import transaction
from celery import shared_task
from core.enums import RequestStatus
from core.models import CSVRequest
from core.services import CSVProcessService

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
                CSVProcessService.process_request(request=request)
