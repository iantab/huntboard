import factory
from apps.accounts.models import User
from apps.applications.models import Application, Contact, Interview
from django.utils import timezone
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    full_name = factory.Faker("name")
    preferred_language = "en"

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        obj.set_password(extracted or "testpass123")
        if create:
            obj.save()


class ApplicationFactory(DjangoModelFactory):
    class Meta:
        model = Application

    owner = factory.SubFactory(UserFactory)
    company_name = factory.Faker("company")
    role_title = factory.Faker("job")
    status = "applied"
    priority = "medium"
    applied_date = factory.Faker("date_object")


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = Contact

    application = factory.SubFactory(ApplicationFactory)
    name = factory.Faker("name")
    role = factory.Faker("job")
    email = factory.Faker("email")


class InterviewFactory(DjangoModelFactory):
    class Meta:
        model = Interview

    application = factory.SubFactory(ApplicationFactory)
    round_number = 1
    interview_date = factory.LazyFunction(
        lambda: timezone.now() + timezone.timedelta(days=7)
    )
    format = "video"
    notes = factory.Faker("text")
