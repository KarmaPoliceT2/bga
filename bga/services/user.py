from ..models.user import User
from sqlalchemy import and_


class UserService(object):
    @classmethod
    def by_name(cls, name, request):
        return request.dbsession.query(User).filter(User.name == name).first()

    @classmethod
    def all_users(cls, request):
        return request.dbsession.query(User).filter(User.name != 'admin')

    @classmethod
    def all_users_except_me_and_admin(cls, request):
        return request.dbsession.query(User).filter(and_(User.name != 'admin', User.name != request.authenticated_userid))
