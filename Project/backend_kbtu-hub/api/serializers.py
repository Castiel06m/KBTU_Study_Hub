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
        fields = ['id', 'title', 'content', 'order', 'course', 'video_url']

class CommentSerializer(serializers.ModelSerializer):
    # Чтобы видеть имя пользователя, а не просто его ID
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'course', 'user', 'user_name', 'text', 'created_at']
        read_only_fields = ['user', 'created_at'] # Юзера будем брать из request.user во вьюхе

class CourseModelSerializer(serializers.ModelSerializer):
    # Вложенный сериализатор для красоты 
    lessons = LessonSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta: 
        model = Course
        fields = ['id', 'title', 'description', 'category', 'category_name', 'author', 'lessons', 'comments']

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
# Обычные Serializers

class EnrollmentSerializer(serializers.Serializer):
    # Используем для логики записи на курс
    course_id = serializers.IntegerField()
    student_id = serializers.IntegerField(read_only=True)
    enrolled_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Enrollment.objects.create(**validated_data)

class StatSerializer(serializers.Serializer):
    # Чисто для статистики 
    total_courses = serializers.IntegerField()
    total_students = serializers.IntegerField()

class GuildMessageSerializer(serializers.Serializer):
    guild_id = serializers.IntegerField()
    content = serializers.CharField(max_length=1000)
    sender_username = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return GuildMessage.objects.create(**validated_data)