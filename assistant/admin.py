from django.contrib import admin

from .models import Register
from .models import ReviewRecord

admin.site.register(Register)
admin.site.register(ReviewRecord)
