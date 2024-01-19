from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from app import app, db, dao, utils
from utils import datetime_f
from flask_admin import Admin, expose
from app.models import UserRole, User, Ve, HangVe, Ghe, Customer, ChuyenBay, ChiTietSBTG, SanBay
from flask_admin.contrib.sqla import ModelView
from flask import redirect, request, url_for
from flask_admin import BaseView
from flask_login import logout_user, current_user
from datetime import datetime, timedelta

admin = Admin(app=app, name='Quản lý chuyến bay', template_mode='bootstrap4')


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class AuthenticatedBaseView_Admin(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')


class StatsView(AuthenticatedBaseView_Admin):

    @expose('/')
    def index(self):
        year = datetime.now().year
        month = datetime.now().month
        if request.method.__eq__('GET'):
            date = request.args.get('__stat__')
            if date:
                date_stats = datetime.strptime(date, '%Y-%m')
                year = date_stats.year
                month = date_stats.month
            else:
                year = datetime.now().year
                month = datetime.now().month
        stats = dao.ChuyenBay_Month_Stat(month=month, year=year)
        return self.render('admin/stats.html', stats=stats)


class ChuyenBayView(ModelView, AuthenticatedBaseView):
    can_create = False
    can_view_details = True
    form_excluded_columns = ['sanbay_tg', 'customer']

class UserView(ModelView, AuthenticatedBaseView_Admin):
    can_view_details = True
    form_excluded_columns = ['sanbay_tg', 'customer']
    form_excluded_columns = ['chuyen_bay', 've']

class LapLichView(AuthenticatedBaseView):

    @expose('/', methods=["GET", "POST"])
    def index(self):
        list_sanbay = dao.load_sanbay()
        return self.render('employee/laplich.html', sanbays=list_sanbay)

class SanBayView(ModelView, AuthenticatedBaseView_Admin):
    can_create = True
    can_edit = True
    can_view_details = True
    form_excluded_columns = ['chuyen_bay', 'chi_tiet_cb']

class TicketView(AuthenticatedBaseView):
    can_create = False
    can_edit = False

    @expose('/', methods=["GET", "POST"])
    def index(self):
        tickets = dao.get_ticket_by_datetime()
        if request.method.__eq__('GET'):
            date = request.args.get('date')
            tickets = dao.get_ticket_by_datetime(date)
        return self.render('employee/ticket.html', tickets=tickets)


admin.add_view(UserView(User, db.session, name='User'))
admin.add_view(ChuyenBayView(ChuyenBay, db.session, name='Chuyến Bay'))
admin.add_view(LogoutView(name='Log out'))
admin.add_view(StatsView(name='Thống kê báo cáo'))
admin.add_view(LapLichView(name='Lâp lịch Chuyến Bay'))
admin.add_view(SanBayView(session=db.session, name='Sân Bay', model=SanBay))
admin.add_view(TicketView(name='Danh sách vé'))
