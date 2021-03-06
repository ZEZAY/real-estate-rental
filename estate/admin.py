from django.contrib import admin
from estate.forms.custom_form import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin
from .models import Condo, Unit, CustomUser, ContactInfo
from .models.condo import CondoImages
from .models.unit import UnitImages
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
import json


class ContactInfoInline(admin.TabularInline):
    model = ContactInfo
    extra = 1


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = [
        (None, {
            'fields': [
                'username',
                'first_name',
                'last_name',
                'email',
                'role',
            ]
        }),
    ]
    add_fieldsets = [
        (None, {
            'fields': [
                'username',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'email',
                'role',
            ]
        }),
    ]
    # add_fieldsets = fieldsets


    search_fields = ['username']
    inlines = [ContactInfoInline]
    list_display = ['username', 'email', 'role']


class CondoImagesInline(admin.TabularInline):
    model = CondoImages
    extra = 1


class CondoAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {
            'widget': map_widgets.GoogleMapsAddressWidget(attrs={
                'data-autocomplete-options': json.dumps({'types': [
                    'geocode',
                    'establishment'
                ],
                    'componentRestrictions': {}
                })
            })
        },
    }
    fieldsets = [
        (None, {
            'fields': [
                'name',
                'description',
                'number_of_floors',
                'address',
                'geolocation'
            ]
        }),
        ('Admin only', {
            'fields': [
                'juristic_persons_number',
                'common_fee_account',
            ],
        }),
        ('Amenity Information', {
            'fields': [
                'amenities',
            ],
        }),
    ]
    inlines = [CondoImagesInline]
    list_display = (
        'name',
        'juristic_persons_number',
        'common_fee_account',
    )
    search_fields = ['name']


class UnitImagesInline(admin.TabularInline):
    model = UnitImages
    extra = 1


class UnitAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'condo',
                'owner',
                'title',
                'description',
                'still_on_contract',
                'price_for_rent',
                'price_for_sell',

            ]
        }),
        ('Unit information', {
            'fields': [
                'number',
                'floor_number',
                'number_of_bedroom',
                'number_of_bathroom',
                'area',
            ],
        }),
    ]
    inlines = [UnitImagesInline]
    list_display = (
        'condo',
        'number',
        'still_on_contract',
    )
    list_filter = ['still_on_contract']
    search_fields = [
        'condo',
        'title',
        'number',
        'area',
    ]


admin.site.register(Condo, CondoAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
