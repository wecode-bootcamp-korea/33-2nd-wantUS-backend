from django.http  import JsonResponse
from django.views import View

from applications.models import Application
from core.utils          import signin_decorator

class ApplicationResultView(View):
    @signin_decorator
    def get(self, request):
        user         = request.user
        applications = Application.objects.select_related('status', 'job', 'job__company').filter(user_id = user.id)

        application_results = [{
            'id'          : application.id,
            'company_name': application.job.company.name,
            'company_logo': application.job.company.logo,
            'position'    : application.job.name,
            'time'        : application.updated_at.strftime('%Y.%m.%d'),
            'result'      : application.status.status
        } for application in applications]

        user_info = {
            "id"   : user.id,
            "name" : user.name,
            "email": user.email
        }

        return JsonResponse({"application_results" : application_results, "user_info" : user_info}, status=200)