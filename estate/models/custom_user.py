from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import validate_email, RegexValidator


class CustomUser(AbstractUser):
    USER_TYPE = (
        (1, "visitor"),
        (2, "owner"),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.PositiveSmallIntegerField(choices=USER_TYPE, default=2, null=True, blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ContactInfo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    CONTACT_TYPES = (
        ('phone', 'Phone Number'),
        ('email', 'Email Address'),
        ('line', 'Line Id'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
    )
    contact_type = models.CharField(
        choices=CONTACT_TYPES,
        default='phone',
        max_length=10,
    )
    information = models.CharField(max_length=100)

    def clean(self):
        if self.contact_type == 'email':
            validate_email(self.information)
        if self.contact_type == 'phone':
            phone_validator = RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
            phone_validator(self.information)
        return True

    def __str__(self):
        type_display = dict(self.CONTACT_TYPES)[self.contact_type]
        return f"{type_display}: {self.information}"
