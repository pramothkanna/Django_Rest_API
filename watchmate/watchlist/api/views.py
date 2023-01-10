from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from watchlist.api.permissions import AdminOrReadOnly,ReviewUserOrReadOnly

from watchlist.models import WatchList,StreamPlatform,Review
from watchlist.api.serializers import WatchListSerializer,StreamPlatformSerializer,ReviewSerializer

class ReviewCreate(generics.CreateAPIView):
    serializer_class=ReviewSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.all()
    
    
    def perform_create(self, serializer):
        pk=self.kwargs.get('pk')
        movie=WatchList.objects.get(pk=pk)
        
        review_user=self.request.user
        review_queryset=Review.objects.filter(watchList=movie,review_user=review_user)
        
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this Movie")
        
        if movie.nof_rating==0:
            movie.avg_rating=serializer.validated_data['rating']
        else:
            movie.avg_rating=(watclist.avg_rating+serializer.validated_data['rating']/2)
            
        movie.nof_rating=movie.nof_rating+1
        movie.save()
            
        serializer.save(watchList=movie,review_user=review_user)
        

class ReviewList(generics.ListAPIView):
    serializer_class=ReviewSerializer
    # permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        pk=self.kwargs['pk']
        return Review.objects.filter(watchList=pk)
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[ReviewUserOrReadOnly]

# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset= Review.objects.all()
#     serializer_class=ReviewSerializer
    
#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)
    

# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset= Review.objects.all()
#     serializer_class=ReviewSerializer
    
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
    
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset=StreamPlatform.objects.all()
    serializer_class=StreamPlatformSerializer

class StreamPlatformAV(APIView):
    
    def get(self, request):
        if request.method == 'GET':
            platform=StreamPlatform.objects.all()
            serializer = StreamPlatformSerializer(platform,many=True)
            return Response(serializer.data)
    
    def post(self, request):
        serializer=StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class StreamPlatformDetailAV(APIView):
    def get(self,request,pk):
        platform=StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)
    
    def put(self,request,pk):
        platform=StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
            
    
    def delete(self,request,pk):
        platform=StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchlistAV(APIView):
    
    def get(self, request):
        if request.method == 'GET':
            movies=WatchList.objects.all()
            serializer = WatchListSerializer(movies,many=True)
            return Response(serializer.data)
    
    def post(self, request):
        serializer=WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class WatchDetailAV(APIView):
    def get(self,request,pk):
        movie=WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self,request,pk):
        movie=WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
            
    
    def delete(self,request,pk):
        movie=WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies=Movie.objects.all()
#         serializer = MovieSerializer(movies,many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer=MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# @api_view(['GET', 'PUT','DELETE'])
# def movie_detail(request,pk):
    
#     if request.method == 'GET':
#         movie=Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         movie=Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
            
    
#     if request.method == 'DELETE':
#         movie=Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
