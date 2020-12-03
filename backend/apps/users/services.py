from sqlalchemy.sql import expression
from sqlalchemy_utils.types.ltree import LQUERY
from flask import request

from engine.db import db_session
from engine.db import engine as db_engine
from .models import User, Role


class UserNotFound(Exception):
    pass

class RoleNotFound(Exception):
    pass

class InvalidRoutePath(Exception):
    pass


def users_create(username, role_id, number=None, full_name=None):
    """create user function"""
    if not Role.query.filter(Role.id == role_id).first():
        raise RoleNotFound

    u = User(username=username, number=number, full_name=full_name, role_id=role_id)
    db_session.add(u)
    db_session.commit()


def users_update(user_id, username, role_id, number=None, full_name=None):
    """update user function"""
    if not Role.query.filter(Role.id == role_id).first():
        raise RoleNotFound

    u = User.query.filter(User.id == user_id).first()
    if not u:
        raise UserNotFound("User update failed. User with this id does not exist")

    u.username = username
    u.number = number
    u.full_name = full_name
    u.role_id = role_id
    db_session.commit()


def users_delete(user_id):
    """delte user function"""
    u = User.query.filter(User.id == user_id)
    if not u:
        raise UserNotFound("User delete failed. User with this id does not exist")
    u.delete()
    db_session.commit()


def users_list(path=None):
    """get users list function"""
    if not path:
        sql = """
        SELECT users.*, roles.path as role_path, roles.name as role
        FROM users
            LEFT JOIN roles ON users.role_id = roles.id
        ;"""
    else:
        sql = f"""
        SELECT users.*, roles.path as role_path, roles.name as role
        FROM users
            INNER JOIN roles ON users.role_id = roles.id AND roles.path <@ '{path}'
        ;"""
    users_models = db_engine.execute(sql)

    users_dict = []
    for user in users_models:
        users_dict.append({
            "id": user.id,
            "username": user.username,
            "role_id": user.role_id,
            "role": user.role,
            "role_path": user.role_path,
            "number": user.number,
            "full_name": user.full_name
        })
    return users_dict


def users_detail(user_id):
    """get users detail function"""
    u = db_engine.execute(f"""
    SELECT users.*, roles.path as role_path, roles.name as role
    FROM users
        LEFT JOIN roles ON users.role_id = roles.id
    WHERE users.id={user_id}
    """).first()
    if not u:
        raise UserNotFound("Fetching user data failed. User with this id does not exist")
    return {
        "id": u.id,
        "username": u.username,
        "role_id": u.role_id,
        "role": user.role,
        "role_path": u.role_path,
        "number": u.number,
        "full_name": u.full_name
    }


def roles_list():
    """get roles list function"""
    roles_models = Role.query.order_by(Role.path).all()
    roles_in_dict = []
    for role in roles_models:
        roles_in_dict.append({"id": role.id, "name": role.name, "path": role.path.path})
    return roles_in_dict
