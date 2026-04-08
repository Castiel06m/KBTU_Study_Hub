from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


# ── Custom Model Manager (requirement: 1 custom manager) ─────────────────────

class MaterialManager(models.Manager):
    def by_type(self, material_type):
        return self.filter(material_type=material_type)

    def recent(self, count=10):
        return self.order_by('-created_at')[:count]

    def by_author(self, user):
        return self.filter(author=user)


class Material(models.Model):
    TYPE_CHOICES = [
        ('lecture', 'Lecture Notes'),
        ('exam', 'Exam Prep'),
        ('lab', 'Lab Work'),
        ('other', 'Other'),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='materials'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='materials/', blank=True, null=True)
    material_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='other')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='materials'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MaterialManager()  # custom manager

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes'
    )
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'material')

    def __str__(self):
        return f'{self.user.username} likes {self.material.title}'


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments'
    )
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username}: {self.text[:50]}'
