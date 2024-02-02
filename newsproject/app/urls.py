from django.contrib import admin
from django.urls import path
from .views import*
from .import views
app_name ='app'

urlpatterns = [
    path('',IndexListView.as_view() , name='index' ),
    path('news/category',CategoryListView.as_view() , name='news_category' ),
    path('news/category/<str:main_category_slug>/', views.CategoryListView.as_view(), name='news_category'),
    path('news/category/<str:main_category_slug>/<str:sub_category_slug>/', views.CategoryListView.as_view(), name='news_category'),
    path('news-details/<slug:news_slug>', NewsDetailsView.as_view(), name='newsDetails'),
    path('team', OurTeamView.as_view(), name='team'),
    path('contact',views.contact, name='contact'),
    path('marketing', DigitalMListview.as_view(), name='marketing'),
    path('marketing/detail<slug:marketing_slug>', DigitalMDetailsView.as_view(), name='marketing_detail'),
    path('gallery', VideoGalleryListview.as_view(), name='gallery'),
    # path('<path:not_found>', custom_404_view, name='catch_all_404'),
 
]
