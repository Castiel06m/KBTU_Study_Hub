from django.urls import path
from .views import (
    category_list, 
    top_courses, 
    CourseListAPIView, 
    CourseDetailAPIView,
    leave_comment,
    enroll_in_course,
    GuildListAPIView,
    guild_messages
)

urlpatterns = [
    # Категории и топ
    path('categories/', category_list),
    path('courses/top/', top_courses),
    
    # Основные курсы 
    path('courses/', CourseListAPIView.as_view()),
    path('courses/<int:pk>/', CourseDetailAPIView.as_view()),
    path('courses/<int:course_id>/comment/', leave_comment),
    path('courses/enroll/', enroll_in_course),
    
    
    # Гильдии и хаб 
    path('guilds/', GuildListAPIView.as_view()),
    path('guilds/<int:guild_id>/messages/', guild_messages),
]