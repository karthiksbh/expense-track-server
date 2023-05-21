from django.contrib import admin
from .models import Expenses,User

admin.site.register(User)
admin.site.register(Expenses)