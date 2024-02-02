from . models import*


def mainCategories(request):
    allCategories = MainCategorie.objects.all().order_by('ordering')
    subcategories = SubCategorie.objects.all().order_by('ordering')
    return({
        'allCategories':allCategories,
        'subcategories':subcategories,
        'sidemenu': allCategories,
    })


def aboutUs(request):
    about = AboutUS.objects.all()
    return({
        'about':about,
    })