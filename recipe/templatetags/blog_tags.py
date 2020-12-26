from django import template

register = template.Library()

@register.simple_tag
def tag_get_param(request, tag):
    tags = request.GET.getlist('tag')
    if tag in tags:
        tags.remove(tag)
    else:
        tags.append(tag)
    param = ''
    for i in tags:
        param = param+'tag='+i+'&'
    return param