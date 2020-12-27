from django import template

register = template.Library()

@register.simple_tag
def tag_get_param(request, tag):
    tags = request.GET.getlist('tag')
    param_get = request.GET.urlencode()
    param_get = param_get.split('&')
    page = ''
    for i in param_get:
        if 'page' in i:
            page = i
    if tag in tags:
        tags.remove(tag)
    else:
        tags.append(tag)
    param = ''
    for i in tags:
        param = param+'tag='+i+'&'
    if page != '':
        param = param+page
    return param


@register.simple_tag
def get_param(request):
    param = request.GET.urlencode()
    param = param.split('&')
    tag_list = []
    param_final = ''
    for i in param:
        if 'tag' in i:
            tag_list.append(i)
    for i in tag_list:
        param_final = param_final+'&'+i
    return param_final
