
from django.urls import path,include
from rest_framework.routers import DefaultRouter
# from watchlist.api.views import movie_list,movie_detail
from watchlist.api.views import (WatchDetailAV,WatchlistAV,StreamPlatformAV,StreamPlatformVS,
                                 StreamPlatformDetailAV,ReviewDetail,ReviewList,ReviewCreate)

router=DefaultRouter()
router.register('stream',StreamPlatformVS,basename='streamplatform')

urlpatterns = [
    path('list/', WatchlistAV.as_view(),name='movie-list'),
    path('<int:pk>', WatchDetailAV.as_view(),name='movie-detail'),
    
    
    path('', include(router.urls)),
    
    
    
    
    # path('platform', StreamPlatformAV.as_view(),name='platform-list'),
    # path('platform/<int:pk>', StreamPlatformDetailAV.as_view(),name='movie-detail'),
    
    path('<int:pk>/reviewcreate', ReviewCreate.as_view(),name='review-create'),
    path('<int:pk>/review', ReviewList.as_view(),name='review-list'),
    path('review/<int:pk>', ReviewDetail.as_view(),name='review-detail'),
]
