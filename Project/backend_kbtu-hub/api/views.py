from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Course, Category, Guild 
from .serializers import (
    CourseModelSerializer, CategorySerializer, 
    GuildModelSerializer, CommentSerializer, 
    EnrollmentSerializer, GuildMessageSerializer, LessonSerializer
)

# FBV 

@api_view(['GET'])
def category_list(request):
    """Список всех категорий"""
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def top_courses(request):
    """Возвращает первые 3 курса"""
    # Custom Manager!
    courses = Course.objects.popular_courses()[:3] 
    serializer = CourseModelSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def leave_comment(request, course_id):
    """Оставить отзыв к курсу"""
    course = get_object_or_404(Course, pk=course_id)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, course=course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def enroll_in_course(request):
    """Записаться на курс"""
    serializer = EnrollmentSerializer(data=request.data)
    if serializer.is_valid():
        # Метод .save() в сериализаторе создаст запись в Enrollment
        serializer.save(student=request.user)
        return Response({"message": "Вы успешно записаны!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def guild_messages(request, guild_id):
    guild = get_object_or_404(Guild, pk=guild_id)

    if request.method == 'GET':
        messages = guild.messages.all().order_by('created_at')
        serializer = GuildMessageSerializer(messages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GuildMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user, guild=guild) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print("DEBUG ERRORS:", serializer.errors) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def join_guild(request, guild_id):
    guild = get_object_or_404(Guild, pk=guild_id)
    
    if guild.members.filter(id=request.user.id).exists():
        return Response({'detail': 'Вы уже состоите в этой гильдии'}, status=status.HTTP_400_BAD_REQUEST)
    
    guild.members.add(request.user)
    return Response({'detail': 'Вы успешно вступили в гильдию'}, status=status.HTTP_200_OK)

# CBV 

class CourseListAPIView(APIView):
    """CRUD: Create & Read для курсов"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseModelSerializer(courses, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):

        print("DATA FROM FRONTEND:", request.data)

        if request.user.role != 'teacher':
            return Response(
                {'error': 'Только преподаватели могут создавать курсы'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = CourseModelSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(author=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("SERIALIZER ERRORS:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDetailAPIView(APIView):
    """CRUD: Read, Update, Delete"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Course, pk=pk)

    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseModelSerializer(course, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        course = self.get_object(pk)
        if course.author != request.user:
            return Response({'error': 'No permission'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CourseModelSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = self.get_object(pk)
        if course.author != request.user:
            return Response({'error': 'No permission'}, status=status.HTTP_403_FORBIDDEN)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GuildListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        guilds = Guild.objects.all()
        serializer = GuildModelSerializer(guilds, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuildModelSerializer(data=request.data)
        if serializer.is_valid():
            guild = serializer.save(leader=request.user)
            guild.members.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LessonCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        course_id = request.data.get('course')
        course = get_object_or_404(Course, pk=course_id)
        
        if course.author != request.user:
            return Response({'error': 'Только автор курса может добавлять уроки'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)