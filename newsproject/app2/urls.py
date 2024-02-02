from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import *


app_name ='dashboard'
urlpatterns = [
        path('',views.index,name='index'),
        path('login', views.login, name='login'),
        path('logout', views.userlogout, name='logout'),
        path('about-us', views.aboutUs, name='aboutUs'),
        # path('contact-us', views.contactUs, name='contactUs'),
        # path('our-team',views.ourteam, name="ourteam"),



        path('news', views.newsList, name='allnews'),
        path('news/delete/<slug:slug>', views.deletenews, name='deletenews'),
        path('news/categorie', views.mainCategories, name='mainCategorie'),
        path('news/add', views.createNews, name='createnews'),
        path('news/edite/<slug:slug>',views.editeNews, name="edite_news"),
        path('news/categorie/main-categorie',views.add_edit_MainCategorie,name='add_MainCategorie'),
        path('news/categorie/edit_main-categorie/<int:id>/',views.add_edit_MainCategorie,name='edit_MainCategorie'),
        path('news/categorie/delete/main-ategorie/<int:id>/',views.deleteMainCategorie,name='deleteMainCategorie'),
    
        path('news/categorie/sub-categorie',views.subCategories,name='subCategorie'),
        path('news/categorie/add/sub-categories',views.add_edit_SubCategories,name='add_SubCategories'),
        path('news/categorie/edit/sub-categories/<int:id>/',views.add_edit_SubCategories,name='edit_SubCategories'),
        path('news/categorie/delete/sub-categories/<int:id>/',views.deleteSubCategories,name='deleteSubCategories'),


        path('advertisement/horizontal-ads',views.horizontalAds,name='horizontalAds'),
        path('advertisement/add/horizontal-ads',views.add_edit_HorizontalAds,name='add_HorizontalAds'),
        path('advertisement/edit/horizontal-ads/<int:id>/',views.add_edit_HorizontalAds,name='edit_HorizontalAds'),
        path('advertisement/delete/horizontal-ads/<int:id>/',views.deletehorizontalAds,name='deletehorizontalAds'),

        
        path('ourTeam',views.ourTeam,name='ourTeam'),
        path('add_OurTeam',views.add_edit_OurTeam,name='add_OurTeam'),
        path('edit_OurTeam/<int:id>/',views.add_edit_OurTeam,name='edit_OurTeam'),
        path('deleteOurTeam/<int:id>/',views.deleteOurTeam,name='deleteOurTeam'),
    
        path('newsVideo',views.newsVideo,name='newsVideo'),
        path('add_newsVideo',views.add_edit_newsVideo,name='add_newsVideo'),
        path('edit_newsVideo/<int:id>/',views.add_edit_newsVideo,name='edit_newsVideo'),
        path('deletenewsVideo/<int:id>/',views.deletenewsVideo,name='deletenewsVideo'),
        
        path('digitalMarketing',views.digitalMarketing,name='digitalMarketing'),
        path('add_digitalMarketing/',views.add_edit_digitalMarketing,name='add_digitalMarketing'),
        path('edit_digitalMarketing/<int:id>/',views.add_edit_digitalMarketing,name='edit_digitalMarketing'),
        path('deletedigitalMarketing/<int:id>/',views.deletedigitalMarketing,name='deletedigitalMarketing'),
    
        path('ContactUs',views.Contact_Us,name='contactUs'),
        path('deleteContactUs/<int:id>/',views.deleteContactUs,name='deleteContactUs'),
    
        path('pop-up-ads', views.popUpAds,name='popUpAds'),
        path('subcategories', views.load_sub_category, name="ajax_load_courses"),
        
        path('change_password/', views.change_password, name='change_password'),
        


]+ static (settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)