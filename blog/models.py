from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.html import format_html 

from ckeditor.fields import RichTextField
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, confirm_password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email address",max_length=255,unique=True)
    name = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='images', null=True, blank = True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # answer: All admins are staff
        return self.is_admin



class BaseModelWithUid(models.Model):
    uid = models.UUIDField(
        db_index=True, unique=True, default=uuid.uuid4, editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
    


class Category(BaseModelWithUid):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check if the category with the given name already exists
        existing_category = Category.objects.filter(name=self.name).first()

        if not existing_category:
            super().save(*args, **kwargs)
        else:
            # If the category already exists, you can choose to do nothing or raise an exception
            # For example, you can raise a ValidationError
            from django.core.exceptions import ValidationError
            raise ValidationError("Category with this name already exists.")




class Post(BaseModelWithUid):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    feature_image = models.ImageField(upload_to='posts/')
    title = models.CharField(max_length=200)
    teaser = models.TextField(max_length=None, blank=False, default="")
    description = RichTextField(max_length=None, blank=False)

    STATUS_CHOICES = [
        ('publish', 'Publish'),
        ('unpublish', 'Unpublish'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='publish')
    
    
    def __str__(self):
        return self.title
    
    def post_image(self):
        return format_html('<img src="/media/{}" style="width:40px;height:40px;border-radius:50%" />'.format(self.feature_image))
    


class Volunteer(BaseModelWithUid):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    interest_area = models.CharField(max_length=70, null=True, blank=True)
    photo = models.ImageField(upload_to='posts/')
    comment = models.TextField(max_length=200, null=True, blank=True)
    
    
    
class Contact(BaseModelWithUid):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.CharField(max_length=30)
    subject = models.TextField(max_length=200)