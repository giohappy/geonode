#########################################################################
#
# Copyright (C) 2016 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from django.conf import settings
from django.urls import re_path
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.admin.options import IS_POPUP_VAR
from django.shortcuts import get_object_or_404
from django.utils.html import escape
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import PermissionDenied
from django.forms import modelform_factory
from geonode.base.admin import set_user_and_group_dataset_permission

from .models import Profile


csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())


class ProfileAdmin(ModelAdmin):
    modelform_factory(get_user_model(), fields="__all__")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (
            _("Extended profile"),
            {
                "fields": (
                    "organization",
                    "profile",
                    "position",
                    "voice",
                    "fax",
                    "delivery",
                    "city",
                    "area",
                    "zipcode",
                    "country",
                    "keywords",
                )
            },
        ),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("username", "password1", "password2")}),)
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("id", "username", "organization", "email", "first_name", "last_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "organization", "profile", "first_name", "last_name", "email")
    # readonly_fields = ("groups", )
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    actions = [set_user_and_group_dataset_permission]

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)
    
    '''
    def get_urls(self):
        return [  # '',
            re_path(r"^(\d+)/password/$", self.admin_site.admin_view(self.user_change_password))
        ] + super().get_urls()
    '''

admin.site.register(Profile, ProfileAdmin)
