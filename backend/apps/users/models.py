from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import LtreeType
from sqlalchemy_utils import Ltree

from engine.db import Base


class Role(Base):
    """Role model"""
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    path = Column(LtreeType, nullable=False)

    def __repr__(self):
        return "<Role {}>".format(self.name)


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    number = Column(String)
    full_name = Column(String)
    role_id = Column(Integer, ForeignKey(Role.id), nullable=False)
    role = relationship("Role", backref="User")

    def __repr__(self):
        return "<User {}>".format(self.username)


def load_db_data(db_session):
    """Load the required data into the database"""
    # 1 lvl roles
    user_role = Role(name="Пользователи", path=Ltree("users"))

    # 2 lvl roles
    # users
    admin_role = Role(name="Администраторы", path=Ltree("users.admins"))
    client_role = Role(name="Клиенты", path=Ltree("users.clients"))
    employee_role = Role(name="Сотрудники", path=Ltree("users.employees"))

    # 3 lvl roles
    # clients
    entity_role = Role(name="Юридические лица", path=Ltree("users.clients.entitities"))
    private_buyer_role = Role(name="Физические лица", path=Ltree("users.clients.private_buyers"))
    # employees
    manager_role = Role(name="Менеджеры", path=Ltree("users.employees.managers"))
    operator_role = Role(name="Операторы", path=Ltree("users.employees.operators"))

    roles = [
        user_role,
        admin_role, client_role, employee_role,
        entity_role, private_buyer_role, manager_role, operator_role
    ]

    db_session.add_all(roles)
    db_session.commit()

    # insert random users
    agree = input("Do you want to populate the database with random users? [Y / N]: ").lower()
    while agree != 'y' and agree != 'n':
        agree = input("Please use only Y or N: ").lower()
    if agree == 'y':
        i = 1
        users = []
        for role in roles:
            users.append(User(username=f"test{i}", role_id=role.id))
            i += 1
            users.append(User(username=f"test{i}", role_id=role.id))
            i += 1
    db_session.add_all(users)
    db_session.commit()
    print('Users inserted')
