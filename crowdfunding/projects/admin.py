from django.contrib import admin
from .models import Project
from .models import Pledge



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'goal', 'is_open', 'date_created', 'owner')
    list_filter = ('is_open', 'date_created')
    search_fields = ('title', 'description', 'owner__username')
# Register your models here.

@admin.register(Pledge)
class PledgeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'comment', 'anonymous', 'project')
    list_filter = ('anonymous', 'project')
    search_fields = ('comment',)

    #put back in suppoert into list_filter and list display

