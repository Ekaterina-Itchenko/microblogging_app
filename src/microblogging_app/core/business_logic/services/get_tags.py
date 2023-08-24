from core.models import Tag


def get_tags() -> list[tuple[str, str]]:
    tags = [(tag.name, tag.name) for tag in Tag.objects.all()]
    return tags
