from .api import Signup_api, Login_api, dashboard_api, profile_api, forgot_password_api
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', Signup_api, name='signup'),
    path('login/', Login_api, name='login'),
    path('dashboard/', dashboard_api, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('profile/', profile_api, name='profile'),
    path('forgot-password/', forgot_password_api, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='accounts/change_password.html', success_url=reverse_lazy('login')), name='password_change'),
]
