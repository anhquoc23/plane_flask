from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Text, Enum, DateTime, Time
from sqlalchemy.orm import relationship, backref
from datetime import datetime, timedelta
from flask_login import UserMixin
from app import db, app
from enum import Enum as UserEnum
import random

class UserRole(UserEnum):
    ADMIN = 1
    EMPLOYEE = 2


class BaseMoDel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class ChiTietSBTG(BaseMoDel):
    __tablename__ = 'ChiTietSBTG'

    id_sanbay_tg = Column(ForeignKey('SanBay.id'), primary_key=True)
    id_chuyenbay = Column(ForeignKey('ChuyenBay.id'), primary_key=True)
    tg_dung = Column(Time, nullable=False)
    ghi_chu = Column(Text)

    def __str__(self):
        return str(self.id_chuyenbay)


chi_tiet_san_bay = db.Table('chi_tiet_san_bay',
                            Column('id_sanbay', Integer, ForeignKey('SanBay.id'), primary_key=True),
                            Column('id_chuyenbay', Integer, ForeignKey('ChuyenBay.id'), primary_key=True))


class SanBay(BaseMoDel):
    __tablename__ = 'SanBay'

    ten_San_bay = Column(String(50), nullable=False)
    dia_diem = Column(String(100), nullable=False)
    chuyen_bay = relationship('ChiTietSBTG', backref='san_bay_tg', lazy=True)

    def __str__(self):
        return self.ten_San_bay


class ChuyenBay(BaseMoDel):
    __tablename__ = 'ChuyenBay'

    ten_chuyen_bay = Column(String(100), nullable=False)
    tg_khoihanh = Column(DateTime, nullable=False)
    tg_bay = Column(Time, nullable=False)
    giave_hv1 = Column(Float, nullable=False)
    giave_hv2 = Column(Float, nullable=False)
    sanbay_tg = relationship("ChiTietSBTG", backref='chuyen_bay_tg', lazy=True)
    san_bay = relationship('SanBay', secondary='chi_tiet_san_bay', lazy='subquery', backref=backref('chi_tiet_cb', lazy=True))
    customer = relationship("Ve", backref='chuyen_bay')
    id_nv = Column(Integer, ForeignKey('User.id'), nullable=False)

    def __str__(self):
        return self.ten_chuyen_bay


class Ve(BaseMoDel):
    __tablename__ = 'Ve'

    id_chuyenbay = Column(ForeignKey('ChuyenBay.id'), primary_key=True)
    id_khach_hang = Column(ForeignKey('Customer.id'), primary_key=True)
    id_hangve = Column(Integer, ForeignKey('HangVe.id'), nullable=False)
    id_ghe = Column(Integer, ForeignKey('Ghe.id'), nullable=False)
    id_nv = Column(Integer, ForeignKey('User.id'))
    GiaVe = Column(Float, nullable=False)
    ngay_xuat_ve = Column(DateTime, default=datetime.now())

    khach_hang = relationship("Customer", backref="ve")
    ten_chuyen_bay = relationship("ChuyenBay", backref="chuyenbay")
    hang = relationship("HangVe", backref="hangve")
    chair = relationship("Ghe", backref="ghe")

    def __str__(self):
        return str(self.id)


class Customer(BaseMoDel):
    __tablename__ = 'Customer'

    ho_ten = Column(String(50), nullable=False)
    so_cccd = Column(String(15), nullable=False)
    sdt = Column(String(12), nullable=False)
    chuyenbay = relationship("Ve", backref='customer')

    def __str__(self):
        return self.ho_ten


class HangVe(BaseMoDel):
    __tablename__ = 'HangVe'

    ten_hang_ve = Column(String(10), nullable=False)
    ve = relationship('Ve', backref='hang_ve', lazy=True)
    ghe = relationship('Ghe', backref='hang_ve', lazy=True)

    def __str__(self):
        return self.ten_hang_ve


# Ghe(ID-Ghe, SoGhe, ID-HangVe)
class Ghe(BaseMoDel):
    __tablename__ = 'Ghe'

    id_hangve = Column(Integer, ForeignKey('HangVe.id'), nullable=False)
    so_ghe = Column(Integer, nullable=False)
    ve = relationship('Ve', backref='ghe', lazy=True)

    def __str__(self):
        return str(self.id)


# User(User-ID, UserName, Password)
class User(BaseMoDel, UserMixin):
    __tablename__ = 'User'

    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.EMPLOYEE)
    ho_ten = Column(String(50), nullable=False)
    so_cccd = Column(String(15), nullable=False)
    sdt = Column(String(12), nullable=False)
    chuyen_bay = relationship('ChuyenBay', backref='nhan_vien', lazy=True)
    ve = relationship('Ve', backref='nhan_vien', lazy=True)

    def __str__(self):
        return str(self.id)


if __name__ == '__main__':
    with app.app_context():
        print('Test')
        # db.create_all()
        # user admin
        # import hashlib
        # pw = str(hashlib.md5('123456'.encode('utf-8')).digest())
        # u = User(username='admin', password=pw, user_role=UserRole.ADMIN,
        #          ho_ten='Nguyễn Anh Quốc', so_cccd='261644679', sdt='0974283040')
        # db.session.add(u)
        # db.session.commit()

        # user employee
        # import hashlib
        #
        # pw = str(hashlib.md5('123123'.encode('utf-8')).digest())
        # u = User(username='anhquoc0304', password=pw, user_role=UserRole.EMPLOYEE,
        #          ho_ten='Nguyễn Anh Quốc', so_cccd='261657679', sdt='0978283040')
        # db.session.add(u)
        # db.session.commit()

        # hạng vé
        # for i in range(1, 3):
        #     ve = HangVe(ten_hang_ve='hang_' + str(i))
        #     db.session.add(ve)
        #
        # db.session.commit()

        #Ghe
        # for i in range(1, 21):
        #     ghe = Ghe(id_hangve=1, so_ghe=i)
        #     db.session.add(ghe)
        #
        # for i in range(1, 21):
        #     ghe = Ghe(id_hangve=2, so_ghe=i)
        #     db.session.add(ghe)
        #
        # db.session.commit()

        #Lập lịch chuyê bay
        # while True:
        #     print('Nhap ngay khoi hanh:')
        #     day = int(random.randint(1, 28))
        #     month = int(random.randint(1, 12))
        #     year = 2020
        #     hour = int(random.randint(0, 23))
        #     minute = 0
        #     thoi_gian_khoi_hanh = datetime(year=year, month=month, day=day, hour=hour, minute=minute)
        #     print('Nhap thoi gian bay')
        #     hour = int(random.randint(1, 24))
        #     minute = 30 if int(random.randint(1, 100)) % 2 is not 0 else 0
        #     thoigianbay = timedelta(hours=hour, minutes=minute)
        #     giave1 = float(int(random.randint(100, 500)) * 10**4)
        #     giave2 = giave1 * 1.5
        #     print('Chi tiet san bay')
        #     sb1 = SanBay.query.get(int(random.randint(1, 7)))
        #     sb2 = SanBay.query.get(1 if int(random.randint(1, 7)) + 1 > 7 else int(random.randint(1, 7)) + 1)
        #     name = sb1.ten_San_bay + ' - ' + sb2.ten_San_bay
        #     c = ChuyenBay(ten_chuyen_bay=name, tg_khoihanh=thoi_gian_khoi_hanh,
        #                   tg_bay=thoigianbay, giave_hv1=giave1, giave_hv2=giave2, id_nv=2)
        #     db.session.add(c)
        #     db.session.commit()
        #     c.san_bay.append(sb1)
        #     c.san_bay.append(sb2)
        #     db.session.add(c)
        #     print('Chi tiet san bay trung gian')
        #     count = random.randint(0, 2)
        #     while count > 0:
        #         id_sanbay = int(input('Nhap ma san bay trung gian: '))
        #         thoigiandung = 30
        #         sbtg = ChiTietSBTG(id_sanbay_tg=id_sanbay, id_chuyenbay=c.id,
        #                            tg_dung=timedelta(minutes=thoigiandung))
        #         db.session.add(sbtg)
        #         count = count - 1
        #     db.session.commit()
        #     print('Luu thanh cong')
        #     if input('Tiep tuc? (Y/N): ') == 'N':
        #         break