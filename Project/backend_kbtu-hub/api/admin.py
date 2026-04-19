from django.contrib import admin
from .models import Category, Course, Lesson, Enrollment, Comment

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(Comment)