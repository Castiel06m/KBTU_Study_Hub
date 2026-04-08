from django.urls import path
from .views import (
    CategoryListView,
    material_list_create,
    material_detail,
    LikeToggleView,
    CommentListCreateView,
    CommentDetailView,
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('materials/', material_list_create, name='material-list'),
    path('materials/<int:pk>/', material_detail, name='material-detail'),
    path('materials/<int:pk>/like/', LikeToggleView.as_view(), name='material-like'),
    path('materials/<int:pk>/comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('materials/<int:pk>/comments/<int:comment_pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
