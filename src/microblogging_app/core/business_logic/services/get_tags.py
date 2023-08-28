from core.models import Tag


def get_tags_func() -> list[tuple[str, str]]:
    """Gets tags info from DB to SearchTagForm."""

    tags = [
        ("", ""),
    ] + [(tag.name, tag.name) for tag in Tag.objects.all().order_by("-created_at")]
    return tags
