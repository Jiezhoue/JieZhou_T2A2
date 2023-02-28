from main import db
from flask import Blueprint
from models.users import User
from models.dentists import Dentist
from main import bcrypt


db_command = Blueprint('db', __name__)

# CLI COMMANDS AREA
@db_command.cli.command('create')
def create():
    db.create_all()
    print("Table created!")

@db_command.cli.command('drop')
def delete():
    db.drop_all()
    print("Table deleted!")

@db_command.cli.command('seed')
def seed():
    user1 = User()
    user1.f_name = 'Eddy'
    user1.l_name = 'Zhou'
    user1.mobile = '0433576893'
    user1.username = 'eddyzhou'
    user1.password = bcrypt.generate_password_hash('12345678').decode('utf-8')
    user1.admin = True

    db.session.add(user1)
    db.session.commit()

    user2 = User()
    user2.f_name = 'Teresa'
    user2.l_name = 'Kerr'
    user2.mobile = '0434562378'
    user2.username = 'teresakerr'
    user2.password = bcrypt.generate_password_hash('12345678').decode('utf-8')

    db.session.add(user2)
    db.session.commit()

    dentist1 = Dentist()
    dentist1.f_name = 'Jamie'
    dentist1.l_name = 'Lam'
    dentist1.username = 'jamielam'
    dentist1.password = bcrypt.generate_password_hash('12345678').decode('utf-8')
    dentist1.speciality = 'Implantology'

    db.session.add(dentist1)
    db.session.commit()


    dentist2 = Dentist()
    dentist2.f_name = 'David'
    dentist2.l_name = 'Keir'
    dentist2.username = 'davidkeir'
    dentist2.password = bcrypt.generate_password_hash('12345678').decode('utf-8')
    dentist2.speciality = 'Orthodontics'

    db.session.add(dentist2)
    db.session.commit()

    dentist3 = Dentist()
    dentist3.f_name = 'James'
    dentist3.l_name = 'Zvirblis'
    dentist3.username = 'jameszvirblis'
    dentist3.password = bcrypt.generate_password_hash('12345678').decode('utf-8')
    dentist3.speciality = 'General'

    db.session.add(dentist3)
    db.session.commit()

    print("Table Seeded!")
