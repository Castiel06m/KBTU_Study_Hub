from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Модель категорий 
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CourseManager(models.Manager):
    def get_by_category(self, category_name):
        return self.filter(category__name=category_name)

    # фильтрация "активных" или популярных курсов
    def popular_courses(self):
        return self.all()[:5]
# Модель курса 
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    # связь курса с преподом 
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    objects = CourseManager()

    def __str__(self):
        return self.title
    


# Модель урока внутри курса
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField() 
    order = models.IntegerField(default=1) 
    video_url = models.URLField(blank=True, null = True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

# Модель записи на курс 
class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course') # Чтобы нельзя было записаться дважды

# Модель отзывов/комментариев 
class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# Модель Гильдии 
class Guild(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='led_guilds')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='guilds', blank=True)

    def __str__(self):
        return self.name

# Модель сообщения внутри Гильдии 
class GuildMessage(models.Model):
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']