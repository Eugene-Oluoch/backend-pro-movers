from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from . import views

# for the swaggerUI
# schema_view = get_swagger_view(title="ProMovers")
schema_view = get_schema_view(
   openapi.Info(
      title="ProMovers",
      default_version='v1',
      description="Documentation for the promovers API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="kennjunnior@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path('', schema_view),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('users/', views.api_get_all_users, name="all_users"),
    path('movers/', views.api_get_all_movers, name="all_movers"),
    path('register/', views.register_user, name="register_user"),
    # path('login/', obtain_auth_token, name="login_user"),
    path('users/<str:username>/', views.api_get_specific_user, name="one_user"),
    path('users/update/<str:username>/', views.api_update_user_profile, name="update_user"),
    path('movers/<str:username>/', views.api_get_specific_mover, name="one_mover"),
    path('movers/update/<str:username>/', views.api_update_mover_profile, name="update_mover"),
    path('requests/new-request/', views.new_move_request.as_view(), name="new_move_request"),
    path('requests/user/<str:username>/', views.api_get_all_users_requests.as_view(), name="users_requests"),
    path('requests/mover/<str:username>/', views.api_get_all_movers_requests.as_view(), name="movers_requests"),
    path('requests/', views.api_get_all_requests.as_view(), name="all_requests"),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('accounts/login/', views.MyTokenObtainPairView.as_view(), name="swagger_login"),
    path('login/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
]
