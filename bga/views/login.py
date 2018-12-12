from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from ..services.user import UserService
from ..models.user import User


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login(request):
    return {}


@view_config(route_name='auth', match_param='action=out', renderer='string')
@view_config(route_name='auth', match_param='action=in', renderer='string', request_method='POST')
def sign_in_out(request):
    username = request.POST.get("username")
    if username:
        user = UserService.by_name(username, request=request)
        if user and user.verify_password(request.POST.get('password')):
            headers = remember(request, user.name)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)
