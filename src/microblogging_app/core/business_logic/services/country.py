from core.models import Country


def get_countries() -> list[tuple[str, str]]:
    """Gets countries info from DB to EditProfileForm."""

    countries = [(value.name, value.name) for value in Country.objects.all()]
    return countries
