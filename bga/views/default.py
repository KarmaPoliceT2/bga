from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from ..services.user import UserService
from ..models.user import User
from ..forms import RegistrationForm


@view_config(route_name='home', renderer='../templates/index.jinja2')
def index_page(request):
    return{}


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


@view_config(route_name='register', renderer='../templates/register.jinja2')
def register(request):
    form = RegistrationForm(request.POST)
    if request.method == "POST" and form.validate():
        new_user = User(name=form.username.data)
        new_user.set_password(form.password.data.encode('utf-8'))
        new_user.setup_keypair()
        request.dbsession.add(new_user)
        return HTTPFound(location=request.route_url('login'))
    return {'form': form}
