from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from raterapi.views import UserViewSet
from raterapi.views import GameView, ReviewView, RatingView

router = DefaultRouter(trailing_slash=False)
router.register(r'games', GameView, 'game')
router.register(r'reviews', ReviewView, 'review')
router.register(r'ratings', RatingView, 'rating')

urlpatterns = [
    path('', include(router.urls)),
    path('login', UserViewSet.as_view({'post': 'user_login'}), name='login'),
    path('register', UserViewSet.as_view({'post': 'register_account'}), name='register'),
]