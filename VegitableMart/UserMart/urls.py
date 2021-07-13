from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from . import views

urlpatterns=[
    path('signup/', views.signup, name="signup"),
    path('login/', views.MartLogin, name="login"),
    path('logout/', views.MartLogout, name="logout"),
	path('resendOTP/', views.resend_otp),

	path("password-reset/",PasswordResetView.as_view(template_name='UserMart/password_reset.html'),name="password_reset"),
	path("password-reset/done/",PasswordResetDoneView.as_view(template_name='UserMart/password_reset_done.html'),name="password_reset_done"),
	path("password-reset-confirm/<uidb64>/<token>/",PasswordResetConfirmView.as_view(template_name='UserMart/password_reset_confirm.html'),name="password_reset_confirm"),
	path("password-reset-complete/",PasswordResetCompleteView.as_view(template_name='UserMart/password_reset_complete.html'),name="password_reset_complete"),
]

