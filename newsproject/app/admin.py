from django.contrib import admin
from . models import*





admin.site.register(PopUpAds)

class AboutUSAdmin(admin.ModelAdmin):
    model = AboutUS
    list_display =['title','logo','DepartmentRegistrationNo','contactNo','email']
    
    fieldsets = (
      ('About Us', {
          'fields': ('logo','title','DepartmentRegistrationNo' ,'editor','adEmail' )
      }),
      ('Contact Details', {
          'fields': ('contactNo','email' , 'address'  , 'website',)
      }),
      ('Social Media', {
          'fields': ('facebookUrl','twitterUrl','youtubeUrl','instaUrl','tiktokUrl' )
      })
   )
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)
    
admin.site.register(AboutUS,AboutUSAdmin)





    

class SubcategorieAdmin(admin.TabularInline):
    model =SubCategorie

class MainCategorieAdmin(admin.ModelAdmin):
    inlines =[SubcategorieAdmin]
    list_display = ['categorie_name','ordering']
admin.site.register(MainCategorie, MainCategorieAdmin)




class NewsAdmin(admin.ModelAdmin):
    model = News
    list_display =['title','trending']
    list_filter=['trending']
    list_editable = ['trending']
    list_per_page= 10
    
admin.site.register(News, NewsAdmin)



class ContactUsAdmin(admin.ModelAdmin):
    model = ContactUs
    list_display = ['name','email']
    
admin.site.register(ContactUs, ContactUsAdmin)

class OurTeamAdmin(admin.ModelAdmin):
    model = OurTeam
    list_display = ['name','email']
    
admin.site.register(OurTeam,OurTeamAdmin)


class PrivacyPolicyAdmin(admin.ModelAdmin):
    model = PrivacyPolicy
    list_display =['title','privacy_policy']
    list_editable =['privacy_policy']
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)
    

admin.site.register(PrivacyPolicy,PrivacyPolicyAdmin)

class VideoAdmin(admin.ModelAdmin):
    model = video
    list_display =['title','videoUrl']
    list_per_page= 10
    
admin.site.register(video, VideoAdmin)


class MarketingAdmin(admin.ModelAdmin):
    model = DigitalMarketing
    list_display = ['title','currentPrice']
    
admin.site.register(DigitalMarketing,MarketingAdmin)