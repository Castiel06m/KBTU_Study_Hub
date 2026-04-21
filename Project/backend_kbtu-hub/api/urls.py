from django.urls import path
from .views import (
    LessonCreateAPIView,
    category_list,
    join_guild, 
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
    path('lessons/', LessonCreateAPIView.as_view()),
    
    
    # Гильдии и хаб 
    path('guilds/', GuildListAPIView.as_view()),
    path('guilds/<int:guild_id>/messages/', guild_messages),
    path('guilds/<int:guild_id>/join/', join_guild),
]