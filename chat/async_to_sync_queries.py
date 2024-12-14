from channels.db import database_sync_to_async
from django.db.models import F

from chat.models import Work


@database_sync_to_async
def async_filter_work_engineer_and_date(date, aircrafts_sn, engineer_id):
    works = list(Work.objects.filter(
        date=date,
        aircraft__aircraft_sn__in=aircrafts_sn,
        engineer_id=engineer_id,
    ).values('date',
             'engineer_id',
             'mh',
             name=F('engineer__name'),
             surname=F('engineer__surname'),
             sn=F('aircraft__aircraft_sn')
             ))
    return [
        {
            'date': work['date'].strftime('%Y-%m-%d'),
            'sn': work['sn'],
            'engineer_id': work['engineer_id'],
            'name': work['name'],
            'surname': work['surname'],
            'mh': work['mh'],
        }
        for work in works
    ]
