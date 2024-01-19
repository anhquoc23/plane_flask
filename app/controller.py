import random

from app import app, login, dao, utils, models, db
from utils import datetime_f
from flask import render_template, url_for, request, redirect
from flask_login import login_user, logout_user
from datetime import datetime, timedelta
from flask_login import logout_user, current_user


def home():
    chuyenbays = dao.load_chuyenbay()
    tg_dens = []
    count = chuyenbays.__len__()
    for c in chuyenbays:
        tm = timedelta(hours=c.tg_bay.hour, minutes=c.tg_bay.minute)
        tg_dens.append(c.tg_khoihanh + tm)
    return render_template('index.html', chuyenbays=chuyenbays, tg_dens=tg_dens, count=count)


def tra_cuu():
    sanbays = dao.load_sanbay()
    return render_template('tracuu.html', sanbays=sanbays)

def tra_cuu_detail():
    return render_template('tracuu_detail.html')

def check_tracuu():
    err = []
    if request.method.__eq__('GET'):
        sb1 = request.args['sanbay1']
        sb2 = request.args['sanbay2']
        date = request.args['date']
        dtime = datetime.strptime(date, '%Y-%m-%d')
        # return sb1 + ', ' + sb2 + ', ' + date
        if sb1.__eq__(sb2):
            err.append('Lỗi trùng sân bay')
        a = datetime.now() - dtime
        if a.days > 0:
            err.append('Chọn thời gian hợp lý')
        cb = dao.tracuu_cb(sb_di=sb1, sb_den=sb2, time=dtime)
        tg_dens = []
        count = cb.__len__()
        for c in cb:
            tm = timedelta(hours=c.tg_bay.hour, minutes=c.tg_bay.minute)
            tg_dens.append(c.tg_khoihanh + tm)
        if err:
            return render_template('tracuu.html', err=err, sanbays=dao.load_sanbay())
    return render_template('tracuu_detail.html', sb1=sb1, sb2=sb2, chuyenbays=cb, tg_dens=tg_dens, count=count)


def dat_ve(chuyenbay_id):
    c = dao.get_ChuyenBay_by_id(id=chuyenbay_id)
    chairs_1 = dao.get_chair(id_chuyenbay=chuyenbay_id, id_hangve=1)
    chairs_2 = dao.get_chair(id_chuyenbay=chuyenbay_id, id_hangve=2)
    #SBTG
    sbtgs = []
    id_sbtgs = dao.get_id_SBTG(chuyenbay_id)
    for id in id_sbtgs:
        name = dao.get_name_SB_By_id(id=id.id_sanbay_tg)
        time_stop = id.tg_dung
        d = dict([('name', name), ('time_stop', time_stop)])
        sbtgs.append(d)
    return render_template('datve.html', chuyenbay=c , sbtgs=sbtgs, chairs_1=chairs_1,
                           chairs_2=chairs_2)

def luu_ve():
    if request.method.__eq__('POST'):
        #Lưu thông tin khách hàng
        hoten = request.form['hoten']
        phone = request.form['phone']
        cccd = request.form['cccd']
        customer = models.Customer(ho_ten=hoten, so_cccd=cccd, sdt=phone)
        db.session.add(customer)
        db.session.commit()
        # Lưu Vé
        # + Lấy thông tin chuyến bay
        id_cb = int(request.form['id_chuyenbay'])
        chuyenbay = dao.get_ChuyenBay_by_id(id_cb)
        id_customer = dao.get_customer_lastest().id
        id_hv = int(request.form['hangve'])
        chair = ''
        price = 0
        if id_hv == 1:
            price = chuyenbay.giave_hv1
            chair = int(request.form['chair_1'])
        else:
            price = chuyenbay.giave_hv2
            chair = int(request.form['chair_2'])
        ve = dao.add_ve_Onine(id_cb=chuyenbay.id, id_kh=id_customer, id_hv=id_hv,
                              id_ghe=chair, gv=price, ngay_xuatve=chuyenbay.tg_khoihanh)
        db.session.commit()
        return home()


def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.check_login(username=username, password=password)
    if user:
        login_user(user=user)
    return redirect('/admin')

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id=user_id)

def lap_lich_CB():
    count_SB = 2
    msg = ''
    err = ''
    if request.method.__eq__('POST'):
        # Sân bay đi và đến
        sanbaydi = request.form['sanbaydi']
        sanbayden = request.form['sanbayden']
        a = {sanbaydi, sanbayden}
        # thời gian khởi han và thời gian bay
        tg_khoihanh = datetime.strptime(request.form['datetime'], '%Y-%m-%dT%H:%M')
        tg_bay = timedelta(hours=int(request.form['hours']), minutes=int(request.form['minutes']))
        # lưu giá vé
        giave_1 = float(request.form['price_1'])
        giave_2 = float(request.form['price_2'])
        # Sân bay trung gian
        # + Sân bay 1
        sbtg1 = request.form['sanbaytg1']
        tg_dung__sbtg1 = timedelta(minutes=int(request.form['time_stop_1']))
        ghichu__sbtg1 = request.form['ghichu1']
        # + Sân bay 2
        sbtg2 = request.form['sanbaytg2']
        tg_dung__sbtg2 = timedelta(minutes=int(request.form['time_stop_2']))
        ghichu__sbtg2 = request.form['ghichu2']
        # check sân bay trùng
        if sbtg1.__eq__('None') == False:
            count_SB = count_SB + 1
            a.add(sbtg1)
        if sbtg2.__eq__('None') == False:
            count_SB = count_SB + 1
            a.add(sbtg2)
        if (a.__len__() < count_SB):
            err =  'Lỗi trùng sân bay!!! Vui lòng quay trở lại để tạo lịch lại'
            return err
        # Xử lý lập lịch
        dao.add_chuyen_bay(name=sanbaydi + ' - ' + sanbayden, time_start=tg_khoihanh,
                           time_fly=tg_bay, price_1=giave_1, price_2=giave_2,
                           id_nv=current_user.id)
        if sbtg1.__eq__('None') == False:
            dao.add_sanbaytg(sanbay=sbtg1, time_stop=tg_dung__sbtg1,
                         ghichu=ghichu__sbtg1)
        if sbtg2.__eq__('None') == False:
            dao.add_sanbaytg(sanbay=sbtg2, time_stop=tg_dung__sbtg2,
                         ghichu=ghichu__sbtg2)
        return render_template('employee/success.html')

def load_ticket():
    if request.method.__eq__('GET'):
        date = request.args['date']
        date_ticket = datetime.strptime(date, '%Y-%m-%d')
        return render_template('employee/ticket.html', tickets=dao.get_ticket_by_datetime(date_ticket))







