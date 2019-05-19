import factory as factory_boy

from crossbox import models

factory_boy.Faker._DEFAULT_LOCALE = 'es_ES'


class TypeFactory(factory_boy.django.DjangoModelFactory):
    class Meta:
        model = models.Type
        django_get_or_create = ('name',)

    name = factory_boy.Faker('first_name')
    price_reference = factory_boy.Faker(
        'pydecimal',
        left_digits=8,
        right_digits=2,
        positive=True,
    )
    lifespan_years_reference = factory_boy.Faker('pyint')


class ManufacturerFactory(factory_boy.django.DjangoModelFactory):
    class Meta:
        model = models.Manufacturer
        django_get_or_create = ('name',)

    name = factory_boy.Faker('first_name')
