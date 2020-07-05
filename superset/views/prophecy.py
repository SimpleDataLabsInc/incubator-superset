from flask_appbuilder.security.views import AuthRemoteUserView
from flask import redirect, g, flash, request, session
from flask_appbuilder._compat import as_unicode
from flask_appbuilder.security.views import AuthDBView, AuthRemoteUserView
from flask_appbuilder.security.views import expose
from flask_appbuilder.security.manager import BaseSecurityManager
from flask_appbuilder import base
from flask_login import login_user, logout_user


class ProphecyRemoteUserView(AuthRemoteUserView):
    # Leave blank
    login_template = ''

    @expose('/login/')
    def login(self):
        # headers
        token = request.headers.get("X-AUTH-TOKEN")
        # username = request.headers.get('HTTP_PROXY_REMOTE_USER')
        if g.user is not None and g.user.is_authenticated():
            return redirect(self.appbuilder.get_url_for_index)

        sm = self.appbuilder.sm
        session = sm.get_session
        user = session.query(sm.user_model).filter_by(username=token).first()
        if user is None and token:
            msg = ("User not allowed, {}".format(token))
            flash(as_unicode(msg), 'error')
            return redirect(self.appbuilder.get_url_for_login)

        if token:
            user = self.appbuilder.sm.auth_user_remote_user(token)
            if user is None:
                flash(as_unicode(self.invalid_login_message), 'warning')
            else:
                login_user(user)
        else:
            flash(as_unicode(self.invalid_login_message), 'warning')

        return redirect(self.appbuilder.get_url_for_index)
