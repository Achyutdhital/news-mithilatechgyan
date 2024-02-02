from django.shortcuts import render,HttpResponse, HttpResponseRedirect,redirect,get_object_or_404
from account.models import User
from django.contrib.auth import authenticate, login, logout
from . decorators import login_required
from django.contrib import messages
from django.contrib import auth
from . forms import *
from app.models import *
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from . new_file_handler import validate_file


def login(request):
    try:
        if request.user.is_authenticated:
            return render(request,'app2/index.html')

        if request.method =="POST":
            email = request.POST['useremail']
            print(email)
            password = request.POST['password']
            print(password)
            user_obj = User.objects.filter(email= email)
            print(user_obj)
            if not user_obj.exists():
                messages.warning(request,"Invalid username...")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                
            
            user_obj = authenticate(email=email, password=password)
            if user_obj and user_obj.is_superuser or user_obj.is_editor:
                auth.login(request, user_obj)
                return redirect('dashboard:index')
            
            messages.warning(request,'Inavlid Password')
            return redirect('dashboard:login')
            
        return render(request,'app2/login.html')
            

    except Exception as e:
        print(e)
        messages.warning(request,'something wrong...')
        return redirect('dashboard:login')


@login_required
def userlogout(request):
    auth.logout(request)
    messages.info(request,"logout successfully..")
    return redirect('dashboard:login')


@login_required
def index(request):
    return render(request,'app2/index.html')


@login_required
def aboutUs(request):
    instance = None
    try:
        if id:
            instance = AboutUS.objects.first()
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the AboutUS.')
        return redirect('dashboard:aboutUs')

    if request.method == 'POST':
        form = AboutUSForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'AboutUS edited successfully.')
                return redirect('dashboard:aboutUs')  # Redirect to the edited AboutUS's details page
            else:  # Add operation
                messages.success(request, 'AboutUS added successfully.')
                return redirect('dashboard:aboutUs')  # Redirect to the page for adding new AboutUSs
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = AboutUSForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_about_us.html', context)


#news categorei
@login_required
def add_edit_MainCategorie(request, id=None):
    instance = None
    try:
        if id:
            instance = MainCategorie.objects.get(pk=id)
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the MainCategorie.')
        return redirect('dashboard:add_MainCategorie')

    if request.method == 'POST':
        form = MainCategorieForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'MainCategorie edited successfully.')
                return redirect('dashboard:edit_MainCategorie', id=instance.id)  # Redirect to the edited MainCategorie's details page
            else:  # Add operation
                messages.success(request, 'MainCategorie added successfully.')
                return redirect('dashboard:add_MainCategorie')  # Redirect to the page for adding new MainCategories
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = MainCategorieForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_MainCategorie.html', context)

@login_required
def mainCategories(request):
    MainCategories=MainCategorie.objects.all()
    p=Paginator(MainCategories,10)
    page_number= request.GET.get('page')
    MainCategories=p.get_page(page_number)
    return render(request, 'app2/MainCategorie.html',{'details':MainCategories})

@login_required
def deleteMainCategorie(request, id):
    record = get_object_or_404(MainCategorie, id=id)

    if request.method == 'POST':
        record.delete()
        return redirect('dashboard:mainCategorie')  # Redirect to a list view after deletion
    else:
        return render(request, 'app2/MainCategorie.html', {'details': record})



#news subcategorie
@login_required
def add_edit_SubCategories(request, id=None):
    instance = None
    try:
        if id:
            instance = SubCategorie.objects.get(pk=id)
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the SubCategories.')
        return redirect('dashboard:add_SubCategories')

    if request.method == 'POST':
        form = SubCategorieForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'SubCategories edited successfully.')
                return redirect('dashboard:edit_SubCategories', id=instance.id)  # Redirect to the edited SubCategories's details page
            else:  # Add operation
                messages.success(request, 'SubCategories added successfully.')
                return redirect('dashboard:add_SubCategories')  # Redirect to the page for adding new SubCategoriess
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = SubCategorieForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_SubCategories.html', context)

@login_required
def subCategories(request):
    SubCategories=MainCategorie.objects.all()
    p=Paginator(SubCategories,4)
    page_number= request.GET.get('page')
    SubCategories=p.get_page(page_number)
    return render(request, 'app2/SubCategories.html',{'details':SubCategories})

@login_required
def deleteSubCategories(request, id):
    record = SubCategorie.objects.get(pk=id)
    if request.method == 'POST':
        record.delete()
        messages.success(request,'Sub Categorie Deleted Successfully !')
        return redirect('dashboard:subCategorie')  # Redirect to a list view after deletion
    else:
        return render(request, 'app2/SubCategories.html', {'details': record})



@login_required 
def newsList(request):
    allnews = News.objects.all()
    return render(request,'app2/news_table.html',{'allNews':allnews})


@login_required
def createNews(request):
    allcategorie= MainCategorie.objects.all()
    user= request.user
    if request.method=="POST":
        newstitle = request.POST['title']
        maincategorie= request.POST['categoryselect']
        mainctg = MainCategorie.objects.get(id=maincategorie)
        subcategorie = request.POST['subcategory']
        if subcategorie:
            subctg = SubCategorie.objects.get(id =subcategorie)
        else:
            subctg =None
        # reporter = request.POST['reporter']
        # news_reporter =User.objects.get(id=reporter)
        trending_status=request.POST['trending']
        # short_description = request.POST['shortdiscription']
        news_description = request.POST['description']
        news_image = request.FILES['newsimage']
        new_news= News.objects.create( 
                                      categorie=mainctg,
                                      subCategorie=subctg,
                                      title=newstitle,
                                      discriptions=news_description,
                                      image =news_image,
                                    #   repoter =news_reporter,
                                      trending= trending_status,
                                      
                                      )
        new_news.save()
        messages.success(request,'News added successfully !')
        return redirect('dashboard:createnews')

    else:
        return render(request,'app2/create_news.html',{'allcategorie':allcategorie,
                                                       'user':user
                                                       })
@login_required
def editeNews(request, slug=None):
    news = News.objects.get(news_slug =slug)
    allcategorie= MainCategorie.objects.all()
    user= request.user
    if request.method=="POST":
        news.title = request.POST['title']
        maincategorie= request.POST['categoryselect']
        news.categorie = MainCategorie.objects.get(id=maincategorie)
        subcategorie = request.POST['subcategory']
        if subcategorie:
            news.subCategorie = SubCategorie.objects.get(id =subcategorie)
        else:
            news.subCategorie =None

        news.trending=request.POST['trending']
        news.discriptions = request.POST['description']
        if 'newsimage' in request.FILES:
            news.image = request.FILES['newsimage']
    
        
        news.save()
        messages.success(request,'News updated successfully !')
        return redirect('dashboard:edite_news', slug=news.news_slug)

    
    return render(request,'app2/edite_news.html',{'news':news,
                                                  'allcategorie':allcategorie,
                                                    'user':user
                                                  })

@login_required
def deletenews(request, slug):
    relatedNews= News.objects.get(news_slug=slug)
    relatedNews.delete()
    messages.success(request,"News deleted successfullY !")
    return redirect('dashboard:allnews')

@login_required
def load_sub_category(request):
    main_ctg_id = request.GET.get('programming')
    print(main_ctg_id)
    sub_category = SubCategorie.objects.filter(maincategorie=main_ctg_id)
    return render(request,'app2/listdropdow.html',{'sub_category':sub_category})




# ads sections
@login_required
def add_edit_HorizontalAds(request, id=None):
    instance = None
    try:
        if id:
            instance = HorizontalAds.objects.get(pk=id)
    except Exception as e:
        print(e)
        messages.warning(request, 'An error occurred while retrieving the HorizontalAds.')
        return redirect('dashboard:add_HorizontalAds')

    if request.method == 'POST':
        form = HorizontalAdsForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'HorizontalAds edited successfully.')
                return redirect('dashboard:edit_HorizontalAds', id=instance.id)  # Redirect to the edited HorizontalAds's details page
            else:  # Add operation
                messages.success(request, 'HorizontalAds added successfully.')
                return redirect('dashboard:add_HorizontalAds')  # Redirect to the page for adding new HorizontalAdss
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = HorizontalAdsForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_horizontal_ads.html', context)

@login_required
def horizontalAds(request):
    horizontalAds=HorizontalAds.objects.all()
    p=Paginator(horizontalAds,10)
    page_number= request.GET.get('page')
    horizontalAds=p.get_page(page_number)
    return render(request, 'app2/horizontalAds.html',{'details':horizontalAds})

@login_required
def deletehorizontalAds(request, id):
    record = get_object_or_404(HorizontalAds, id=id)

    if request.method == 'POST':
        record.delete()
        return redirect('dashboard:horizontalAds')  # Redirect to a list view after deletion

    return render(request, 'app2/horizontalAds.html', {'details': record})

@login_required
def popUpAds(request):
    instance = None
    try:
        if id:
            instance = PopUpAds.objects.first()
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the AboutUS.')
        return redirect('dashboard:popUpAds')

    if request.method == 'POST':
        form = PopUpAdsForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'Pop-Up Ads updated successfully.')
                return redirect('dashboard:popUpAds')  # Redirect to the edited popUpAds's details page
            else:  # Add operation
                messages.success(request, 'Pop-Up Ads updated successfully.')
                return redirect('dashboard:popUpAds')  # Redirect to the page for adding new popUpAdss
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = PopUpAdsForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/popupads.html', context)


@login_required
def ourTeam(request):
    ourTeam_details=OurTeam.objects.all()
    p=Paginator(ourTeam_details,4)
    page_number= request.GET.get('page')
    ourTeam_details=p.get_page(page_number)
    return render(request,'app2/ourTeam.html',{'details':ourTeam_details})

@login_required
def add_edit_OurTeam(request, id=None):
    instance = None
    try:
        if id:
            instance = OurTeam.objects.get(pk=id)
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the ourTeam.')
        return redirect('dashboard:add_OurTeam')

    if request.method == 'POST':
        form = OurTeamForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'OurTeam edited successfully.')
                return redirect('dashboard:edit_OurTeam', id=instance.id)  # Redirect to the edited OurTeam's details page
            else:  # Add operation
                messages.success(request, 'OurTeam added successfully.')
                return redirect('dashboard:add_OurTeam')  # Redirect to the page for adding new OurTeams
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = OurTeamForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_OurTeam.html', context)

@login_required
def deleteOurTeam(request, id):
    record = get_object_or_404(OurTeam, id=id)

    if request.method == 'POST':
        record.delete()
        return redirect('dashboard:ourTeam')  # Redirect to a list view after deletion

    return render(request, 'app2/OurTeam.html', {'details': record})



@login_required
def newsVideo(request):
    newsVideo_details=video.objects.all()
    p=Paginator(newsVideo_details,4)
    page_number= request.GET.get('page')
    newsVideo_details=p.get_page(page_number)
    return render(request,'app2/newsVideo.html',{'details':newsVideo_details})

@login_required
def add_edit_newsVideo(request, id=None):
    instance = None
    try:
        if id:
            instance = video.objects.get(pk=id)
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the training category.')
        return redirect('dashboard:add_newsVideo')

    if request.method == 'POST':
        form = videoForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'newsVideo edited successfully.')
                return redirect('dashboard:edit_newsVideo', id=instance.id)  # Redirect to the edited newsVideo's details page
            else:  # Add operation
                messages.success(request, 'newsVideo added successfully.')
                return redirect('dashboard:add_newsVideo')  # Redirect to the page for adding new newsVideos
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = videoForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_newsVideo.html', context)

@login_required
def deletenewsVideo(request, id):
    record = get_object_or_404(video, id=id)

    if request.method == 'POST':
        record.delete()
        return redirect('dashboard:newsVideo')  # Redirect to a list view after deletion

    return render(request, 'app2/newsVideo.html', {'details': record})


@login_required
def Contact_Us(request):
    ContactUs_details=ContactUs.objects.all()
    p=Paginator(ContactUs_details,4)
    page_number= request.GET.get('page')
    ContactUs_details=p.get_page(page_number)
    return render(request,'app2/Contact_Us.html',{'details':ContactUs_details})

@login_required
def deleteContactUs(request, id):
    record = get_object_or_404(ContactUs, id=id)

    if request.method == 'POST':
        record.delete()
        return redirect('dashboard:Contact_Us')  # Redirect to a list view after deletion

    return render(request, 'app2/Contact_Us.html', {'details': record})



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # update_session_auth_hash(request, user)  # Important to update the session after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard:change_password')  # Redirect to the same view after successful password change
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'app2/change_password.html', {'form': form})




@login_required
def digitalMarketing(request):
    digitalMarketing_details=DigitalMarketing.objects.all()
    p=Paginator(digitalMarketing_details,4)
    page_number= request.GET.get('page')
    digitalMarketing_details=p.get_page(page_number)
    return render(request,'app2/digitalMarketing.html',{'details':digitalMarketing_details})

@login_required
def add_edit_digitalMarketing(request, id=None):
    instance = None
    try:
        if id:
            instance = DigitalMarketing.objects.get(pk=id)
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the training category.')
        return redirect('dashboard:add_digitalMarketing')

    if request.method == 'POST':
        
        form = DigitalMarketingForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'digitalMarketing edited successfully.')
                return redirect('dashboard:edit_digitalMarketing', id=instance.id)  # Redirect to the edited digitalMarketing's details page
            else:  # Add operation
                messages.success(request, 'digitalMarketing added successfully.')
                return redirect('dashboard:add_digitalMarketing')  # Redirect to the page for adding new digitalMarketings

        else:
            print(form.errors)
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = DigitalMarketingForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_digitalMarketing.html', context)

@login_required
def deletedigitalMarketing(request, id):
    record = get_object_or_404(DigitalMarketing, id=id)

    if request.method == 'POST':
        record.delete()
        return redirect('dashboard:digitalMarketing')  # Redirect to a list view after deletion

    return render(request, 'app2/digitalMarketing.html', {'details': record})





