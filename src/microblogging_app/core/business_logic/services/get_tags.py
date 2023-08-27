from core.models import Tag


def get_tags_func() -> list[tuple[str, str]]:
    tags = [(tag.name, tag.name) for tag in Tag.objects.all().order_by("-created_at")]
    return tags
