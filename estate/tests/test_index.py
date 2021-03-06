from django.test import TestCase
from django.urls import reverse
from estate.models import Condo, Unit, CondoImages, CustomUser


class TestIndexView(TestCase):

    def test_no_condo(self):
        response = self.client.get(reverse('estate:index'))
        self.assertContains(response, "No condo available.")

    def test_have_condo(self):
        condo = Condo.objects.create(name="Condo", description="This is not a real condo.", number_of_floors=17,
                                     juristic_persons_number='21754-5432', common_fee_account='12345')
        condoimage = CondoImages.objects.create(condo=condo, image='condo.png')
        condoimage.save()
        condo.save()
        response = self.client.get(reverse('estate:index'))
        self.assertContains(response, condo.name)
        self.assertContains(response, condo.number_of_floors)
