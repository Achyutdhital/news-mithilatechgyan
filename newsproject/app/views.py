from django.shortcuts import get_object_or_404, redirect, render ,HttpResponse
from django.views import View, generic
from .models import*
from .forms import*
from django.contrib import messages




# def custom_404_view(request, exception):
#     return render(request, 'app/alt.html')


class IndexListView(generic.ListView):
    model= News
    template_name='app/index.html'


    def get_context_data(self, *args, **kwargs):
        context = super(IndexListView,self).get_context_data(*args, **kwargs)
        newsCategorie = MainCategorie.objects.all().order_by('ordering')
        context['video']= video.objects.all().order_by('-id')
        context['news']= News.objects.all()
        context['firstCategorieNews'] = News.objects.filter(categorie =newsCategorie.first())
        context['firstCategorie'] =newsCategorie[:1]
        context['scondNewsSection'] =News.objects.filter(categorie =newsCategorie[1:2])
        context['secondCategorie'] = newsCategorie[1:2]
        context['thirdSectionNews'] = News.objects.filter(categorie =newsCategorie[2:3])
        context['thirdCategorie'] = newsCategorie[2:3]
        context['fourthSectionNews'] = News.objects.filter(categorie = newsCategorie[3:4])
        context['fourthCategorie'] = newsCategorie[3:4]
        context['fifthSectionNews'] = News.objects.filter(categorie = newsCategorie[4:5])
        context['fifthCategorie'] = newsCategorie[4:5]
        context['sixthSectionNews'] = News.objects.filter(categorie = newsCategorie[5:6])
        context['sixthCategorie'] = newsCategorie[5:6]
        context['seventhSectionNews'] = News.objects.filter(categorie = newsCategorie[6:7])
        context['seventhCategorie'] = newsCategorie[6:7]
        context['eighthSectionNews'] = News.objects.filter(categorie = newsCategorie[7:8])
        context['eighthCategorie'] = newsCategorie[7:8]
        context['ninethSectionNews'] = News.objects.filter(categorie = newsCategorie[8:9])
        context['ninethCategorie'] = newsCategorie[8:9]
        context['tenthSectionNews'] = News.objects.filter(categorie = newsCategorie[9:10])
        context['tenthCategorie'] = newsCategorie[9:10]
        context['eleventhSectionNews'] = News.objects.filter(categorie = newsCategorie[10:11])
        context['eleventhCategorie'] = newsCategorie[10:11]
        context['twelvethSectionNews'] = News.objects.filter(categorie = newsCategorie[11:12])
        context['twelvethCategorie'] = newsCategorie[11:12]
        context['thirteenthSectionNews'] = News.objects.filter(categorie = newsCategorie[12:13])
        context['thirteenthCategorie'] = newsCategorie[12:13]
        context['fourteenthSectionNews'] = News.objects.filter(categorie = newsCategorie[13:14])
        context['fourteenthCategorie'] = newsCategorie[13:14]
        context['extra'] = News.objects.filter(categorie__in=newsCategorie[14:])
        context['extracategory'] = newsCategorie[14: ]
        context['trending'] = News.objects.filter(trending=True).order_by('-id')[:11]
        context['latest'] =News.objects.all().order_by('-id')[:12]
        # context['maincategorie']= MainCategorie.objects.all()
        context['ourteam']= OurTeam.objects.all()

        
        return context
    
    
class CategoryListView(generic.ListView):
    model = News
    template_name = 'app/news_category.html'
    context_object_name = 'news_list'
    paginate_by = 25

    def get_queryset(self):
        main_category_slug = self.kwargs.get('main_category_slug')
        sub_category_slug = self.kwargs.get('sub_category_slug')

        queryset = News.objects.all()

        if sub_category_slug:
            # Filter by subcategory slug using the ForeignKey relationship
            queryset = queryset.filter(subCategorie__subctgslug=sub_category_slug).order_by('-id')
        elif main_category_slug:
            # Filter by main category slug using the ForeignKey relationship
            queryset = queryset.filter(categorie__main_ctg_slug=main_category_slug).order_by('-id')
        else:
            # If only the main category is specified, show the latest news of that category
            queryset = queryset.filter(categorie__main_ctg_slug=main_category_slug).order_by('-id')
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        main_category_slug = self.kwargs.get('main_category_slug')
        sub_category_slug = self.kwargs.get('sub_category_slug')

        if main_category_slug:
            # Retrieve the main category based on the slug
            main_category = MainCategorie.objects.get(main_ctg_slug=main_category_slug)
            context['main_category'] = main_category

        if sub_category_slug:
            # Retrieve the subcategory based on the slug
            sub_category = SubCategorie.objects.get(subctgslug=sub_category_slug)
            context['sub_category'] = sub_category

        # Include other context data as needed
        context['latest'] = News.objects.all().order_by('-id')[:8]
        context['trending'] = News.objects.filter(trending=True).order_by('-id')[:6]

        return context

class NewsDetailsView(generic.DetailView):
    model= News
    template_name= 'app/news_details.html'
    slug_field = 'news_slug'
    slug_url_kwarg = 'news_slug'

    def get_context_data(self, *args, **kwargs):
        context = super(NewsDetailsView,self).get_context_data(*args, **kwargs)
        newsDetails= get_object_or_404(News, news_slug=self.kwargs['news_slug']) 
        categorie = MainCategorie.objects.get(categorie_name = newsDetails.categorie)  
        context['newsDetails']  = newsDetails
        context['relatedNews'] = News.objects.filter(categorie =categorie).exclude(id=newsDetails.id)[:4]
        context['latest'] =News.objects.all().order_by('-id')[:8]
        context['trending'] = News.objects.filter(trending = True).order_by('-id')[:6]

        # context['verticalAds']=print(VerticalAds.objects.filter(page='news_details')[:5])
        return context
    

    
class OurTeamView(generic.ListView):
    model= OurTeam
    template_name= 'app/our_team.html'

    def get_context_data(self, *args, **kwargs):
        context = super(OurTeamView,self).get_context_data(*args, **kwargs)
        teamDetails= OurTeam.objects.all().order_by('ordering')
        
        context['teamDetails']  = teamDetails

        return context
    
    

def contact(request):
    if request.method =="POST":
        form= ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request , "sucess!!")
            return redirect('contact')
        messages.error(request,"error!!")
    return render(request,'app/contact_us.html',{'contact':contact})



class DigitalMListview(generic.ListView):
    model = DigitalMarketing
    template_name= 'app/marketing.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DigitalMListview,self).get_context_data(*args, **kwargs)
        marketing= DigitalMarketing.objects.all().order_by('ordering')
        context['marketing']  = marketing

        return context
    

    
class DigitalMDetailsView(generic.DetailView):
    model= DigitalMarketing
    template_name= 'app/marketing_detail.html'
    slug_field = 'marketing_slug'
    slug_url_kwarg = 'marketing_slug'

    def get_context_data(self, *args, **kwargs):
        context = super(DigitalMDetailsView,self).get_context_data(*args, **kwargs)
        marketing= get_object_or_404(DigitalMarketing, marketing_slug=self.kwargs['marketing_slug']) 
        context['marketingDetails']  = marketing
        context['marketing'] = DigitalMarketing.objects.all().order_by('-id')

        return context
    


    
class VideoGalleryListview(generic.ListView):
    model = video
    template_name= 'app/video_gallery.html'

    def get_context_data(self, *args, **kwargs):
        context = super(VideoGalleryListview,self).get_context_data(*args, **kwargs)
        gallery= video.objects.all().order_by('-id')
        context['gallery']  = gallery

        return context
    
    
    
def custom_404_view(request, not_found):
    return render(request, 'app/alt.html', status=404)