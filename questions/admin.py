from django.contrib import admin
from explainthis.questions.models import *

admin.site.register(UserProfile)
admin.site.register(Site)
admin.site.register(Question)
admin.site.register(Answer)

