from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from bigchaindb_driver import BigchainDB
from ..services.user import UserService
from ..models.user import User
from ..forms import RegistrationForm, CreateCourseForm, CreateScoreForm
import logging
log = logging.getLogger(__name__)


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
    return HTTPFound(location=request.route_url('login'), headers=headers)


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


@view_config(route_name='createcourse', renderer='../templates/createcourse.jinja2')
def create_course(request):
    form = CreateCourseForm(request.POST)
    if request.method == "POST" and form.validate():
        bdb = BigchainDB(request.registry.settings['bigchaindb.url'])
        course_asset = {
            'data': {
                'course': {
                    'appname': 'BlockchainGolfers',
                    'assetclass': 'BGA_GolfCourse',
                    'coursename': form.coursename.data,
                    'courselocation': form.courselocation.data
                }
            }
        }
        course_metadata = {
            'rating': str(form.rating.data),
            'slope': str(form.slope.data),
            'courseimage': str(form.courseimage.data)
        }
        user = UserService.by_name(
            request.authenticated_userid, request=request)
        prepared_creation_tx = bdb.transactions.prepare(
            operation='CREATE',
            signers=user.pubkey,
            asset=course_asset,
            metadata=course_metadata
        )
        fulfilled_creation_tx = bdb.transactions.fulfill(
            prepared_creation_tx,
            private_keys=user.privkey
        )
        sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)
        return HTTPFound(location=request.route_url('createcourse'))
    return {'form': form}


@view_config(route_name='createscore', renderer='../templates/createscore.jinja2')
def create_score(request):
    form = CreateScoreForm(request.POST)
    username = request.authenticated_userid
    if username and request.method == "GET":
        user_list = UserService.all_users(request=request)
        form.attest.choices = [(user.pubkey, user.name) for user in user_list]
        bdb = BigchainDB(request.registry.settings['bigchaindb.url'])
        courses = bdb.assets.get(search='BGA_GolfCourse')
        form.course.choices = [
            (course['id'], course['data']['course']['coursename']) for course in courses]
        return {'form': form}
    log.debug(form.validate())
    if request.method == "POST":
        user = UserService.by_name(
            request.authenticated_userid, request=request)
        bdb = BigchainDB(request.registry.settings['bigchaindb.url'])
        score_asset = {
            'data': {
                'score': {
                    'appname': 'BlockchainGolfers',
                    'assetclass': 'BGA_ScoreCard',
                    'rounddate': str(form.rounddate.data),
                    'courseid': str(form.course.data),
                    'roundscore': str(form.score.data),
                    'roundplayer': str(user.pubkey),
                    'attestplayername': str(dict(form.attest.choices).get(form.attest.data)),
                    'attestplayerpubkey': str(form.attest.data)
                }
            }
        }
        score_metadata = {
            'scorecardstatus': 'unattested'
        }
        prepared_creation_tx = bdb.transactions.prepare(
            operation='CREATE',
            signers=user.pubkey,
            asset=score_asset,
            metadata=score_metadata
        )
        fulfilled_creation_tx = bdb.transactions.fulfill(
            prepared_creation_tx,
            private_keys=user.privkey
        )
        sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)
        log.debug('BDB Transaction ID is %s', fulfilled_creation_tx['id'])
        return HTTPFound(location=request.route_url('login'))
    else:
        return HTTPFound(location=request.route_url('login'))


@view_config(route_name='courses', renderer='../templates/courses.jinja2')
def courses(request):
    bdb = BigchainDB(request.registry.settings['bigchaindb.url'])
    courses = bdb.assets.get(search='BGA_GolfCourse')
    course_list = []
    for course in courses:
        courses_meta = bdb.metadata.get(search=course['id'])
        log.debug(type(course))
        log.debug(type(courses_meta))
        course.update(courses_meta[0])
        course_list.append(course)
    return {'courses': course_list}
