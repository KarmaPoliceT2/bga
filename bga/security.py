from pyramid.security import Allow, Everyone, Authenticated


class ScorecardRecordFactory(object):
    __acl__ = [(Allow, Everyone, "view"), (Allow, Authenticated, "create")]

    def __init__(self, request):
        pass
