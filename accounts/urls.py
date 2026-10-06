from django.urls import path
from .views import SignUpView, LoginView,ProfilView, PasswordChangeView, ProfileUpdateView, TokenRefresh, LogoutView


urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('me/', ProfilView.as_view()),
    path('passchang/', PasswordChangeView.as_view()),
    path('update/', ProfileUpdateView.as_view()),
    path('login/', LoginView.as_view()),
    path('access/', TokenRefresh.as_view()),
    path('logout/', LogoutView.as_view())
]