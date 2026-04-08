from rest_framework import serializers
from .models import Material, Category, Comment, Like
from users.serializers import UserSerializer


# ── serializers.ModelSerializer (requirement: at least 2) ────────────────────

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created_at')
        read_only_fields = ('id', 'author', 'created_at')


class MaterialSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False
    )
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Material
        fields = (
            'id', 'author', 'title', 'description', 'file',
            'material_type', 'category', 'category_id',
            'likes_count', 'comments_count', 'is_liked',
            'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, material=obj).exists()
        return False


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'material', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')


# ── serializers.Serializer (requirement: at least 2) ─────────────────────────

class MaterialCreateSerializer(serializers.Serializer):
    """Plain Serializer for creating a material — covers requirement 4a."""
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    file = serializers.FileField(required=False)
    material_type = serializers.ChoiceField(
        choices=['lecture', 'exam', 'lab', 'other'], default='other'
    )
    category_id = serializers.IntegerField(required=False, allow_null=True)

    def validate_category_id(self, value):
        if value is not None:
            if not Category.objects.filter(pk=value).exists():
                raise serializers.ValidationError('Category not found.')
        return value

    def create(self, validated_data):
        category_id = validated_data.pop('category_id', None)
        category = Category.objects.filter(pk=category_id).first() if category_id else None
        return Material.objects.create(category=category, **validated_data)


class CommentCreateSerializer(serializers.Serializer):
    """Plain Serializer for creating a comment — covers requirement 4a."""
    text = serializers.CharField()

    def validate_text(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError('Comment is too short.')
        return value.strip()

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
