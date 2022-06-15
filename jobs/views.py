import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import (
    Count,
    Q
)

from jobs.models import *
from users.models import *
from core.utils import signin_decorator

class JobListPrivateView(View):
    @signin_decorator
    def get(self, request):
        offset        = int(request.GET.get('offset', 0))
        limit         = int(request.GET.get('limit', 8))
        sort          = request.GET.get('sort', 'most_recent')
        main_category = request.GET.get('category')
        sub_category  = request.GET.get('sub_category')
        location      = request.GET.get('location')
        career        = request.GET.get('career')
        skill         = request.GET.get('skill')
        search        = request.GET.get('search')

        sort_dict = {
            'most_recent' : '-due_date',
            'popularity' : '-like_num'
        }

        q = Q()

        if main_category:
            q.add(Q(sub_category__main_category_id = main_category), q.AND)

        if sub_category:
            q.add(Q(sub_category_id = sub_category), q.AND)

        if location:
            q.add(Q(company__location_id = location), q.AND)
        
        if career and career:
            q.add(Q(career_id= career), q.AND)

        if skill:
            q.add(Q(requiredskill__skill__id= skill), q.AND)
        
        if search:
            q &= Q(name__icontains = search)
        
        job_list = Job.objects.select_related('company', 'company__location', 'career').filter(q).annotate(like_num = Count('follow'))\
            .order_by(sort_dict[sort])[offset:offset+limit]

        results = [{
            'id'      : job.id,
            'name'    : job.name,
            'company' : job.company.name,
            'location': job.company.location.name,
            'years'   : job.career.name,
            'follow'  : Follow.objects.filter(user_id=request.user.id, job_id=job.id).exists(),
            'url'     : job.company.companyimage_set.first().image_url
        } for job in job_list]
        
        return JsonResponse({'result' : results}, status=200)

class RandomJobListView(View):
    def get(self, request):
        jobs    = Job.objects.all().order_by("?")
        results = [{
            'id'      : job.id,
            'name'    : job.name,
            'company' : job.company.name,
            'location': job.company.location.name,
            'image'   : job.company.companyimage_set.first().image_url
        } for job in jobs]
        
        return JsonResponse({'results' : results}, status=200)

class FollowView(View):
    @signin_decorator
    def post(self, request, job_id):
        user   = request.user

        if Follow.objects.filter(user_id = user.id, job_id = job_id).exists(): 
            Follow.objects.get(user_id = user.id, job_id=job_id).delete()
            results = False
            message = "FOLLOW_DELETE"

        else:
            Follow.objects.create(
                user_id = user.id,
                job_id  = job_id,
            )
            results = True
            message = "FOLLOW_SUCCESS"
        
        follow_count = Follow.objects.filter(job_id=job_id).count()
        return JsonResponse({"message" : message, "results" : results, "follow_count" : follow_count}, status =200)

class FollowedJobView(View):
    @signin_decorator
    def get(self, request):
        user = request.user
        follows = Follow.objects.select_related('job', 'job__company', 'job__company__location').filter(user_id = user.id)
        followed_jobs = [{
            'position'    : follow.job.name,
            'company_name': follow.job.company.name,
            'location'    : follow.job.company.location.name,
            'image'       : follow.job.company.companyimage_set.first().image_url
        } for follow in follows]

        return JsonResponse({"results" : followed_jobs}, status=200)