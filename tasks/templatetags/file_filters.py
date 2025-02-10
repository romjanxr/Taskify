from django import template

register = template.Library()


@register.filter
def is_image(url):
    if url:  # check if url is not empty
        path = url.split('?')[0]  # remove query params from url
        return path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
    return False
