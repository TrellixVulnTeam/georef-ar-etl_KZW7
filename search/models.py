from django.db import models


SOURCES = (
    ('here', 'HERE'),
    ('osm', 'OpenStreetMap')
)


class AddressType(models.Model):
    name = models.CharField(max_length=50)  # 'house_number', 'street', etc.

    def __str__(self):
        return "{}".format(self.name)


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.name)


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.name)


class Address(models.Model):
    name = models.CharField(max_length=250)
    house_number = models.IntegerField(blank=True, null=True)
    lat = models.DecimalField(max_digits=65535, decimal_places=65535)
    lon = models.DecimalField(max_digits=65535, decimal_places=65535)
    type = models.ForeignKey(AddressType)
    district = models.CharField(max_length=100, blank=True, null=True)
    suburb = models.CharField(max_length=100, blank=True, null=True)
    city = models.ForeignKey(City, blank=True, null=True)
    state = models.ForeignKey(State, blank=True, null=True)
    postal_code = models.CharField(max_length=8, blank=True, null=True)
    source = models.CharField(max_length=4, choices=SOURCES)

    def __str__(self):
        return '{} {}'.format(self.name, self.house_number)
