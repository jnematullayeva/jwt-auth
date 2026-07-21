from django.urls import path
from .views import SignUpView, LoginView,ProfilView, PaswordChangView, ProfileUpdateView, TokenRefresh, LogoutView


urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('me/', ProfilView.as_view()),
    path('passchang/', PaswordChangView.as_view()),
    path('update/', ProfileUpdateView.as_view() ),
    path('acsess/', TokenRefresh.as_view()),
    path('logout/', LogoutView.as_view())
]