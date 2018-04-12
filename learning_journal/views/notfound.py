from pyramid.view import (notfound_view_config, forbidden_view_config)


@notfound_view_config(renderer='../templates/404.jinja2')
def notfound_view(request):
    request.response.status = 404
    return {}


@forbidden_view_config(renderer='../templates/404.jinja2')
def forbidden_view(request):
    request.response.status = 404
    return {}
