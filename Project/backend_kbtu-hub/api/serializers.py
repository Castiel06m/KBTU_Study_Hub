from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Course, Lesson, Enrollment, Comment, Guild, GuildMessage

User = get_user_model()

# ModelSerializers 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'order', 'course', 'video_url', 'file']

class CommentSerializer(serializers.ModelSerializer):
    #  имя пользователя, а не просто его ID
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'course', 'user', 'user_name', 'text', 'created_at']
        read_only_fields = ['user', 'course', 'created_at'] # Юзера будем брать из request.user во вьюхе

class CourseModelSerializer(serializers.ModelSerializer):
    # Вложенный сериализатор для красоты 
    lessons = LessonSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    is_enrolled = serializers.SerializerMethodField()

    class Meta: 
        model = Course
        fields = ['id', 'title', 'description', 'category', 'category_name', 'author', 'author_name', 'lessons', 'comments', 'is_enrolled']
        read_only_fields = ['author']

    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            from .models import Enrollment
            return Enrollment.objects.filter(student=request.user, course=obj).exists()
        return False


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class GuildModelSerializer(serializers.ModelSerializer):
    leader_name = serializers.CharField(source='leader.username', read_only=True)
    members_count = serializers.IntegerField(source='members.count', read_only=True)

    class Meta:
        model = Guild
        fields = ['id', 'name', 'description', 'leader', 'leader_name', 'members_count', 'created_at']
        read_only_fields = ['leader', 'created_at']
# Обычные Serializers

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['course'] 

class StatSerializer(serializers.Serializer):
    # Чисто для статистики 
    total_courses = serializers.IntegerField()
    total_students = serializers.IntegerField()

class GuildMessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = GuildMessage    
        fields = ['id', 'content', 'sender_username', 'created_at', 'is_urgent', 'file']
        read_only_fields = ['id', 'sender_username', 'created_at']