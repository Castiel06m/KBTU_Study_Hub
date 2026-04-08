from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Material, Category, Comment, Like
from .serializers import (
    MaterialSerializer, MaterialCreateSerializer,
    CategorySerializer, CommentSerializer, CommentCreateSerializer,
    LikeSerializer,
)


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        author = getattr(obj, 'author', None)
        return author == request.user


# ── CBV: APIView (requirement: at least 2 CBV using APIView) ─────────────────

class CategoryListView(APIView):
    """List all categories or create a new one."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LikeToggleView(APIView):
    """Toggle like on a material."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            material = Material.objects.get(pk=pk)
        except Material.DoesNotExist:
            return Response({'error': 'Material not found.'}, status=404)

        like, created = Like.objects.get_or_create(user=request.user, material=material)
        if not created:
            like.delete()
            return Response({'liked': False, 'likes_count': material.likes.count()})
        return Response({'liked': True, 'likes_count': material.likes.count()}, status=201)


# ── FBV with DRF decorators (requirement: at least 2 FBV) ────────────────────

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def material_list_create(request):
    """List materials (GET) or create a new one (POST)."""
    if request.method == 'GET':
        qs = Material.objects.select_related('author', 'category').order_by('-created_at')
        material_type = request.query_params.get('type')
        category = request.query_params.get('category')
        search = request.query_params.get('search')
        if material_type:
            qs = qs.filter(material_type=material_type)
        if category:
            qs = qs.filter(category__slug=category)
        if search:
            qs = qs.filter(title__icontains=search)
        serializer = MaterialSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    # POST — use plain Serializer for creation
    serializer = MaterialCreateSerializer(data=request.data)
    if serializer.is_valid():
        material = serializer.save(author=request.user)
        return Response(MaterialSerializer(material, context={'request': request}).data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def material_detail(request, pk):
    """Retrieve, update or delete a single material."""
    try:
        material = Material.objects.select_related('author', 'category').get(pk=pk)
    except Material.DoesNotExist:
        return Response({'error': 'Not found.'}, status=404)

    if request.method == 'GET':
        serializer = MaterialSerializer(material, context={'request': request})
        return Response(serializer.data)

    # Write operations — only the author
    if material.author != request.user:
        return Response({'error': 'Permission denied.'}, status=403)

    if request.method in ('PUT', 'PATCH'):
        partial = request.method == 'PATCH'
        serializer = MaterialSerializer(material, data=request.data, partial=partial, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        material.delete()
        return Response(status=204)


# ── Comments: CBV generics ────────────────────────────────────────────────────

class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(material_id=self.kwargs['pk']).select_related('author').order_by('created_at')

    def perform_create(self, serializer):
        material = Material.objects.get(pk=self.kwargs['pk'])
        serializer.save(author=self.request.user, material=material)

    def create(self, request, *args, **kwargs):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            material = Material.objects.get(pk=kwargs['pk'])
            comment = serializer.save(author=request.user, material=material)
            return Response(CommentSerializer(comment).data, status=201)
        return Response(serializer.errors, status=400)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(material_id=self.kwargs['pk'])
