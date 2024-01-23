from django.contrib import admin

from .models import User, Post, Category, Volunteer, Contact

# Customize the model admins
class UserAdminConfiguraton(admin.ModelAdmin):
    list_display = ('name', 'email')

class PostAdminConfiguraton(admin.ModelAdmin):
    list_display = ('title', 'post_image','uid', 'category', 'created_at')
    search_fields = ('title',)
    
# Register your models here.
admin.site.register(User, UserAdminConfiguraton)
admin.site.register(Post, PostAdminConfiguraton)
admin.site.register(Category)
admin.site.register(Volunteer)
admin.site.register(Contact)