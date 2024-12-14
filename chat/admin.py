from django.contrib import admin

from chat.models import *

admin.site.register(AircraftType)
admin.site.register(Aircraft)
admin.site.register(Engineer)
admin.site.register(Work)

# Register your models here.
