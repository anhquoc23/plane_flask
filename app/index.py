from app import app, login, dao, controller
from flask import render_template, url_for, request, redirect
from flask_login import login_user
from app import admin

app.add_url_rule('/', 'home', controller.home)
app.add_url_rule('/tracuu', 'tra_cuu', controller.tra_cuu, methods=['GET'])
app.add_url_rule('/tracuu?check_tracuu', 'check_tracuu', controller.check_tracuu, methods=['GET'])
app.add_url_rule('/tracuu/tracuu_detail', 'tra_cuu_detail', controller.tra_cuu_detail)
app.add_url_rule('/datve/id=<int:chuyenbay_id>', 'dat_ve', controller.dat_ve)
app.add_url_rule('/admin-login', 'admin_login', controller.admin_login, methods=['post'])
app.add_url_rule('/laplich', 'lap_lich_CB', controller.lap_lich_CB, methods=['GET', 'post'])
app.add_url_rule('/luuve', 'luu_ve', controller.luu_ve, methods=['post'])

if __name__ == '__main__':
    from app.admin import *

    app.run(debug=True)
