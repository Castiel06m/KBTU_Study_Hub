# KBTU Study Hub — Backend

Django + DRF backend for the KBTU Study Hub project.

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py makemigrations users materials
python manage.py migrate

# 4. Create a superuser (for /admin panel)
python manage.py createsuperuser

# 5. Start the server
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| POST | /api/auth/register/ | ❌ | Register new user |
| POST | /api/auth/login/ | ❌ | Get JWT tokens |
| POST | /api/auth/token/refresh/ | ❌ | Refresh access token |
| POST | /api/auth/logout/ | ✅ | Blacklist refresh token |
| GET/PATCH | /api/auth/profile/ | ✅ | View/edit own profile |
| GET/POST | /api/categories/ | ✅ | List / create categories |
| GET/POST | /api/materials/ | ✅ | List / upload materials |
| GET/PATCH/DELETE | /api/materials/:id/ | ✅ | CRUD for single material |
| POST | /api/materials/:id/like/ | ✅ | Toggle like |
| GET/POST | /api/materials/:id/comments/ | ✅ | List / add comments |
| DELETE | /api/materials/:id/comments/:id/ | ✅ | Delete comment |

## Requirements Coverage

| Requirement | Status |
|-------------|--------|
| ≥ 4 models | ✅ User, Category, Material, Like, Comment |
| 1 custom model manager | ✅ MaterialManager |
| ≥ 2 ForeignKey relationships | ✅ Material→User, Material→Category, Comment→User, Like→User |
| ≥ 2 `serializers.Serializer` | ✅ MaterialCreateSerializer, CommentCreateSerializer |
| ≥ 2 `serializers.ModelSerializer` | ✅ MaterialSerializer, CommentSerializer, CategorySerializer, LikeSerializer |
| ≥ 2 Function-Based Views (FBV) | ✅ material_list_create, material_detail |
| ≥ 2 Class-Based Views (APIView) | ✅ CategoryListView, LikeToggleView |
| JWT login/logout | ✅ |
| Full CRUD for 1 model | ✅ Material (GET list, GET detail, POST, PATCH, DELETE) |
| Link objects to request.user | ✅ author=request.user on create |
| CORS configured | ✅ django-cors-headers, localhost:4200 allowed |
| Postman collection | ✅ postman_collection.json |
