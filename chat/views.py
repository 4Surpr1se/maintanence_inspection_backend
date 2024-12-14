from django.db.models import Q, F
from django.http import JsonResponse

from chat.models import Work, Engineer, Aircraft

def index(request, date):
    qs = Work.objects.filter(date=date)
    for eng in Engineer.objects.filter(~Q(id__in=qs.values_list('engineer_id', flat=True))):
        Work(engineer=eng, aircraft=Aircraft.get_spawn(), date=date).save()
    qs = Work.objects.filter(date=date).select_related('engineer').group_by('aircraft__aircraft_sn').values(
        'id',
        'date',
        'mh',
        'status',
        engineer_id=F('engineer_id'),
        name=F('engineer__name'),
        surname=F('engineer__surname'),
        types=F('engineer__aircraft_types'),
        sn=F('aircraft__aircraft_sn'),
    )
    return JsonResponse({
        'available': list(Aircraft.objects.filter(status='AVAILABLE').values(type=F('aircraft_type'),
                                                                             sn=F('aircraft_sn'))),
        'data': list(qs)
    }, safe=False)
