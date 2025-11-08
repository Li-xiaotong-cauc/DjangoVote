from django.contrib import admin
from .models import poll, choice, vote

admin.site.register(poll)
admin.site.register(choice)
admin.site.register(vote)

