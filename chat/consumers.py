import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Sum

from chat.async_to_sync_queries import async_filter_work_engineer_and_date
from chat.models import Work, Aircraft


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.date = self.scope["url_route"]["kwargs"]["date"]
        self.date_group_name = f"chat_{self.date}"
        await self.channel_layer.group_add(self.date_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.date_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data = text_data_json["data"]

        await self.channel_layer.group_send(
            self.date_group_name, {"type": "data.change", "data": data}
        )

    async def data_change(self, event):
        data = event["data"]
        validation = {}
        for obj in data:
            aircraft = await Aircraft.objects.aget_or_create(aircraft_sn=obj['sn'])
            work = await Work.objects.aget_or_create(
                date=obj["date"],
                aircraft=aircraft[0],
                engineer_id=obj["engineer_id"],
            )
            work = work[0]
            work.mh = obj['mh']
            await work.asave()
            validation['engineer_id'] = obj["engineer_id"]
            validation['date'] = obj["date"]
            validation.setdefault('aircraft', [])
            validation['aircraft'].append(obj["sn"])
        res = await async_filter_work_engineer_and_date(
            validation["date"],
            validation['aircraft'],
            validation["engineer_id"],
        )

        await self.send(text_data=json.dumps({"data": res}))
