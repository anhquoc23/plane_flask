import datetime
from sqlalchemy import func
from app.models import User, SanBay, ChuyenBay, ChiTietSBTG, chi_tiet_san_bay, Ghe, HangVe, Customer, Ve
from app import app, db
import hashlib
from sqlalchemy.sql import extract
from datetime import datetime, timedelta


def load_sanbay(name=None):
    query = SanBay.query
    if name:
        return query.filter(SanBay.ten_san_bay.__eq__(name)).first()
    return query.all()



def load_chuyenbay():
    return ChuyenBay.query.all()


def san_bay(id_chuyenbay):
    cb = ChuyenBay.query.get(id_chuyenbay)


# def load_SBTG(chuyenbay_id):
#     query = ChiTietSBTG.query;
#     query = query.filter(id_chuyenbay=chuyenbay_id)
#     return query.all()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def load_hangve():
    return HangVe.query.all()


def load_chair():
    return Ghe.query.all()


def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).digest())
        return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password)).first()
    return None



def tracuu_cb(sb_di, sb_den, time:datetime):
    name = sb_di + ' - ' + sb_den
    return ChuyenBay.query.filter(ChuyenBay.ten_chuyen_bay.__eq__(name),
                                  ChuyenBay.tg_khoihanh.contains(time.date())).all()

def get_cb_by_id(id_cb):
    return ChuyenBay.query.get(id_cb)


def get_sb_by_name(name):
    return SanBay.query.filter(SanBay.ten_san_bay.contains(name)).first()


def add_cb(name, tg_kh, tg_bay, gv_h1, gv_h2):
    cb = ChuyenBay(ten_chuyen_bay=name, tg_khoihanh=tg_kh, tg_bay=tg_bay, giave_hv1=gv_h1, giave_hv2=gv_h2)
    db.session.add(cb)
    db.session.commit()


# def add_sbtg(id_sb, id_cb, name, tg_dung, ghi_chu):
#     sbtg = ChiTietSBTG(id_sanbay_tg=id_sb, id_chuyenbay=id_cb, ten_sanbay_tg=name, tg_dung=tg_dung, ghi_chu=ghi_chu)
#     db.session.add(sbtg)
#     db.session.commit()
#     id_sanbay_tg = Column(ForeignKey('SanBay.id'), primary_key=True)
#     id_chuyenbay = Column(ForeignKey('ChuyenBay.id'), primary_key=True)
#     ten_sanbay_tg = Column(String(50), nullable=False)
#     tg_dung = Column(Time)
#     ghi_chu = Column(Text)


def get_cb_by_last_id():
    x = db.session.query(func.max(ChuyenBay.id)).first()
    return ChuyenBay.query.get(x)


def get_kh_by_last_id():
    x = db.session.query(func.max(Customer.id)).first()
    return Customer.query.get(x)


def get_ve_by_last_id():
    x = db.session.query(func.max(Ve.id)).first()
    return Ve.query.get(x)


def add_sb(name, diadiem):
    sb = SanBay(ten_San_bay=name, dia_diem=diadiem)
    db.session.add(sb)
    db.session.commit()


def add_chuyen_bay(name, time_start, time_fly, price_1, price_2, id_nv,):
    c = ChuyenBay(ten_chuyen_bay=name, tg_khoihanh=time_start, tg_bay=time_fly,
                  giave_hv1=price_1, giave_hv2=price_2, id_nv=id_nv)
    db.session.add(c)
    db.session.commit()
    # Sân bay đi và đến
    sb_di = SanBay.query.get(get_id_SanBay_From_Name(name=name.split(' - ')[0]))
    sb_den = SanBay.query.get(get_id_SanBay_From_Name(name=name.split(' - ')[1]))
    c.san_bay.append(sb_di)
    c.san_bay.append(sb_den)
    db.session.add(c)
    db.session.commit()




def add_sb_for_CB(id_sanbaydi, id_sanbayden, id_chuyenbay):
    sb1 = SanBay.query.get(id_sanbaydi)
    sb2 = SanBay.query.get(id_sanbayden)
    c = ChuyenBay.query.get(id_chuyenbay)
    c.san_bay.append(sb1)
    c.san_bay.append(sb2)
    db.session.add(c)
    db.session.commit()


def add_sanbaytg(sanbay, time_stop, ghichu=None):
    id_sanbay = get_id_SanBay_From_Name(sanbay)
    id_chuyenbay = get_cb_by_last_id().id
    sbtg = ChiTietSBTG(id_sanbay_tg=id_sanbay, id_chuyenbay=id_chuyenbay,
                       tg_dung=time_stop, ghi_chu=ghichu)
    db.session.add(sbtg)
    db.session.commit()

def get_Ve_By_id(id_chuyenbay):
    return Ve.query.filter(Ve.id_chuyenbay.__eq__(id_chuyenbay)).all()

def ghe_chair_by_id(id_ghe):
    return Ghe.query.get(id_ghe)

def get_chair(id_hangve, id_chuyenbay):
    # Tạo 1 mảng chứa danh sách số ghế có id hạng vé là 1
    chairs = []
    ghes = Ghe.query.filter(Ghe.id_hangve == id_hangve).all()
    for ghe in ghes:
        chairs.append(ghe.so_ghe)

    # Lấy tất cả các ghế đã đặt của một chuyến bay mà ghế đó có id hạng vé là 1
    cb = ChuyenBay.query.get(id_chuyenbay)
    ves = cb.customer
    for ve in ves:
        if ve.id_hangve == id_hangve:
            soghe = ve.ghe.so_ghe
            if chairs.__contains__(soghe):
                chairs.remove(soghe)  # ghe1 là danh sách các ghế chưa đặt có id hạng vé là 1
    return chairs

def load_chairs(id_chuyenbay):
    chairs = []
    ve = get_Ve_By_id(id_chuyenbay=id_chuyenbay)
    for chair in Ghe.query.all():
        chairs.append(chair)
    # for i in ve:
    #    chairs.remove(get_Ve_By_id(i.id_ghe))
    return chairs

def get_hv_by_name(name):
    return HangVe.query.filter(HangVe.ten_hang_ve.contains(name)).first()


def get_hv_by_so_ghe(so_ghe):
    return HangVe.query.filter(HangVe.ghe.so_ghe == so_ghe).first()


def get_ghe_by_so_ghe(so_ghe):
    return Ghe.query.filter(Ghe.so_ghe == so_ghe).first()


def add_ve_Onine(id_cb, id_kh, id_hv, id_ghe, gv, ngay_xuatve):
    ve = Ve(id_chuyenbay=id_cb, id_khach_hang=id_kh, id_hangve=id_hv, id_ghe=id_ghe, GiaVe=gv, ngay_xuat_ve=ngay_xuatve)
    db.session.add(ve)


def add_kh(name, cccd, sdt):
    kh = Customer(ho_ten=name, so_cccd=cccd, sdt=sdt)
    db.session.add(kh)
    db.session.commit()

def get_ChuyenBay_by_id(id):
    return ChuyenBay.query.get(id)

def get_id_SanBay_From_Name(name):
    s = SanBay.query.filter(SanBay.ten_San_bay.__eq__(name)).first()
    return s.id

def get_id_SBTG(id_ChuyenBay):
    return ChiTietSBTG.query.filter(ChiTietSBTG.id_chuyenbay.__eq__(id_ChuyenBay)).all()

def get_name_SB_By_id(id):
    return SanBay.query.filter(SanBay.id.__eq__(id)).first()
def get_customer_lastest():
    customer = db.session.query(func.max(Customer.id)).first()
    return Customer.query.get(customer)

def ChuyenBay_Month_Stat(month, year):
    return db.session.query( ChuyenBay.ten_chuyen_bay,
                            func.sum(Ve.GiaVe)).join(Ve, Ve.id_chuyenbay.__eq__(ChuyenBay.id))\
                            .filter(extract('month', Ve.ngay_xuat_ve) == month,
                                    extract('year', Ve.ngay_xuat_ve) == year) \
                            .group_by(ChuyenBay.ten_chuyen_bay).all()


def cb_stats(kw=None, from_date=None, to_date=None):
     cb = db.session.query(ChuyenBay.id, ChuyenBay.ten_chuyen_bay, func.sum(Ve.GiaVe))\
    .join(Ve, Ve.id_chuyenbay.__eq__(ChuyenBay.id))\
    .group_by(ChuyenBay.id, ChuyenBay.ten_chuyen_bay)
     return cb.all()

def get_ticket_by_datetime(dateS=None):
    datev = datetime.now()
    if dateS is None:
        date = datetime.now().date()
    return Ve.query.filter(func.date(Ve.ngay_xuat_ve).__eq__(dateS)).all()

if __name__ == '__main__':
    with app.app_context():
        print(get_ticket_by_datetime(datetime(year=2020, month=6, day=25)))
        # t = db.session.query(func(Ve.GiaVe)).join(Ve, Ve.id_chuyenbay.__eq__(ChuyenBay.id))\
        #     .filter(extract('month', Ve.ngay_xuat_ve) == 2,
        #                                             extract('year', Ve.ngay_xuat_ve) == 2023).all()
        # print(t)
#         c = load_chuyenbay()
#         print(c[0].san_bay[0])
#         for i in load_sanbay():
#             print(i.ten_San_bay)
        # c = add_chuyen_bay(name='asd', time_start=datetime.now(), time_fly=timedelta(hours=10, minutes=40),
        #                    price_1=10000, price_2=100000, id_nv=1)
        # add_sb_for_CB(id_sanbaydi=10, id_sanbayden=3, id_chuyenbay=c)

