from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,\
    BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.core import validators
import re
from django.utils import timezone
from django.contrib.auth import get_user_model
import uuid

# Create your models here.

class ShadowingProgramUserManager(BaseUserManager):
    def _create_user(self, email, password,
                     is_staff, is_superuser, role, **extra_fields):
        """
        Creates and saves a User with the given email, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        if password == None and not is_superuser:
            password = unicode(uuid.uuid4())
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, role=role, last_login=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, is_staff=False, is_superuser=False, role=ShadowingProgramUser.APPLICANT,
                                 **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self._create_user(email, password, is_staff=True, is_superuser=True, role=ShadowingProgramUser.ADMIN,
                                 **extra_fields)
    
    def create_agencyuser(self, email, password=None, **extra_fields):
        return self._create_user(email, password, is_staff=False, is_superuser=False, role=ShadowingProgramUser.AGENCY,
                                 **extra_fields)
        

class ShadowingProgramUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email'), max_length=255, unique=True, null=False, blank=False)
    USERNAME_FIELD = 'email'
    APPLICANT = 0
    AGENCY = 1
    ADMIN = 2
    ROLES = ((APPLICANT, _('Applicant')),
                (AGENCY, _('Agency')),
                (ADMIN, _('Admin')),
                )
    role = models.IntegerField(verbose_name=_("Role"), choices=ROLES, default=AGENCY, null=False, blank=False)
    
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = _('Shadowing Program User')
        verbose_name_plural = _('Shadowing Program User')
    
    def __unicode__(self):
        return self.email
    
    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
    
    objects = ShadowingProgramUserManager()
    

# from oauth2client.django_orm import FlowField
# from oauth2client.django_orm import CredentialsField

# 
# class CredentialsModel(models.Model):
#     User = get_user_model()
#     id = models.ForeignKey(User, primary_key=True)
#     credential = CredentialsField()

    
    