#
# Created on Sun Oct 09 2022
#
# The MIT License (MIT)
# Copyright (c) 2022 Rohit Geddam, Arun Kumar, Teja Varma, Kiron Jayesh, Shandler Mason
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from email.policy import default
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from django_countries.fields import CountryField


from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager
from .utils import check_ncsu_email


class CustomUser(AbstractUser):
    """Custom User Model"""

    username = None
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        email = self.email

        if not check_ncsu_email(email):
            raise ValueError("Please use NCSU Email Id!")
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.email


class Profile(models.Model):
    """Model for User Profile"""

    GENDER_MALE = "Male"
    GENDER_FEMALE = "Female"
    GENDER_OTHER = "Other"

    DEGREE_BS = "Bachelors"
    DEGREE_MS = "Masters"
    DEGREE_PHD = "Phd"

    DIET_VEG = "Vegetarian"
    DIET_NON_VEG = "Non Vegetarian"

    COURSE_CS = "Computer Science"
    COURSE_CE = "Computer Engineering"
    COURSE_EE = "Electrical Engineering"
    COURSE_MEC = "Mechanical Engineering"

    CITY_RALEIGH = "Raleigh"
    CITY_DURHAM = "Durham"
    CITY_CARY = "Cary"
    CITY_OTHER = "Other"

    ROOMS_2 = "2"
    ROOMS_3 = "3"
    ROOMS_4 = "4"
    ROOMS_5 = "5"
    ROOMS_6 = "6"
    ROOMS_OTHER = "Other"

    BLANK = "--"
    NO_PREF = "No Preference"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    DEGREE_CHOICES = (
        (DEGREE_BS, "Bachelors Program (BS)"),
        (DEGREE_MS, "Masters Program (MS)"),
        (DEGREE_PHD, "Doctoral Program (PhD)"),
    )

    COURSE_CHOICES = (
        (COURSE_CS, "Computer Science"),
        (COURSE_CE, "Computer Eng."),
        (COURSE_EE, "Electrical Eng."),
        (COURSE_MEC, "Mechanical Eng."),
    )

    CITY_CHOICES = (
        (CITY_RALEIGH, "Raleigh"),
        (CITY_DURHAM, "Durham"),
        (CITY_CARY, "Cary"),
        (CITY_OTHER, "Other"),
    )

    NUM_ROOMS_CHOICES = (
        (ROOMS_2, "2"),
        (ROOMS_3, "3"),
        (ROOMS_4, "4"),
        (ROOMS_5, "5"),
        (ROOMS_6, "6"),
        (ROOMS_OTHER, "Other"),
    )

    DIET_CHOICES = ((DIET_VEG, "Veg"), (DIET_NON_VEG, "Non Veg"))

    PREF_GENDER_CHOICES = (
        (NO_PREF, "No Preference"),
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    PREF_DEGREE_CHOICES = (
        (NO_PREF, "No Preference"),
        (DEGREE_BS, "Bachelors Program (BS)"),
        (DEGREE_MS, "Masters Program (MS)"),
        (DEGREE_PHD, "Doctoral Program (PhD)"),
    )

    PREF_DIET_CHOICES = (
        (NO_PREF, "No Preference"),
        (DIET_VEG, "Veg"),
        (DIET_NON_VEG, "Non Veg"),
    )

    PREF_COURSE_CHOICES = (
        (NO_PREF, "No Preference"),
        (COURSE_CS, "Computer Science"),
        (COURSE_CE, "Computer Eng."),
        (COURSE_EE, "Electrical Eng."),
        (COURSE_MEC, "Mechanical Eng."),
    )

    # PREF_CITY_CHOICES = (
    #     (NO_PREF, "No Preference"),
    #     (CITY_RALEIGH, "Raleigh"),
    #     (CITY_DURHAM, "Durham"),
    #     (CITY_CARY, "Cary"),
    #     (CITY_OTHER, "Other")
    # )
    #
    # PREF_NUM_ROOMATES_CHOICES = (
    #     (NO_PREF, "No Preference"),
    #     (ROOMATES_1, "1"),
    #     (ROOMATES_2, "2"),
    #     (ROOMATES_3, "3"),
    #     (ROOMATES_4, "4"),
    #     (ROOMATES_5, "5"),
    #     (ROOMATES_6, "6"),
    # )
    #
    # PREF_RENT_CHOICES = (
    #     (NO_PREF, "No Preference"),
    #     (RENT_1, "$0"),
    #     (RENT_2, "$200"),
    #     (RENT_3, "$300"),
    #     (RENT_3, "$400"),
    #     (RENT_3, "$500"),
    #     (RENT_3, "$600"),
    #     (RENT_3, "$700"),
    #     (RENT_3, "$800"),
    #     (RENT_3, "$900"),
    #     (RENT_3, "$300"),
    #
    # )

    """User Profile Model"""
    name = models.CharField(max_length=100, default="")
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    hometown = models.CharField(max_length=100, default="", blank=True)

    gender = models.CharField(
        max_length=128, choices=GENDER_CHOICES, blank=True
    )
    degree = models.CharField(
        max_length=128, choices=DEGREE_CHOICES, blank=True
    )
    diet = models.CharField(max_length=128, choices=DIET_CHOICES, blank=True)
    country = CountryField(blank_label="Select Country", blank=True)
    course = models.CharField(
        max_length=128, choices=COURSE_CHOICES, blank=True
    )

    visibility = models.BooleanField(default=True)
    is_profile_complete = models.BooleanField(default=False)
    profile_photo = models.ImageField(
        default="default.png", upload_to="profile_pics"
    )

    # property details

    have_property = models.BooleanField(default=False) # todo create issue so that if this is selected the other fields drop down
    city = models.CharField(
        max_length=128, choices=CITY_CHOICES, blank=True
    )
    general_location_details = models.TextField(max_length=500, blank=True)
    number_of_rooms = models.CharField(
        max_length=128, choices=NUM_ROOMS_CHOICES, blank=True
    )
    rent_per_person = models.PositiveIntegerField(default=0, blank=True)

    # preferences

    preference_gender = models.CharField(
        max_length=128, choices=PREF_GENDER_CHOICES, default=NO_PREF
    )
    preference_degree = models.CharField(
        max_length=128, choices=PREF_DEGREE_CHOICES, default=NO_PREF
    )
    preference_diet = models.CharField(
        max_length=128, choices=PREF_DIET_CHOICES, default=NO_PREF
    )
    preference_country = CountryField(
        blank_label="No Preference", blank=True, default="No Preference"
    )
    preference_course = models.CharField(
        max_length=128, choices=PREF_COURSE_CHOICES, default=NO_PREF
    )
    # preference_city = models.CharField(
    #     max_length=128, choices=PREF_CITY_CHOICES, default=NO_PREF
    # )
    # preference_number_of_roomates = models.CharField(
    #     max_length=128, choices=PREF_NUM_ROOMATES_CHOICES, default=NO_PREF
    # )
    #
    # preference_rent_min = models.PositiveIntegerField(default=0)
    # preference_rent_max = models.PositiveIntegerField(default=None)

    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email}-profile"


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    """Create User Profile"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    """Save User Profile"""
    instance.profile.save()
