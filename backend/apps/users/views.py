from flask import Blueprint
import json

from engine.response import MakeResponse
from engine.request_validate import validate
from .services import *

router = Blueprint("users", __name__)


class CreateUserForm:
    username: str
    role_id: int
    number: str = None
    full_name: str = None

class UpdateUserForm:
    user_id: int
    username: str
    role_id: int
    number: str = None
    full_name: str = None

@router.route("/list", methods=["GET"])
def users_list_view():
    """Get users list view"""
    path = request.args.get("path")
    users = users_list(path)
    return MakeResponse(data=users)


@router.route("/create", methods=["POST"])
def users_create_view():
    """Create user view"""
    # validate request data by class. Return 400 if request data is not valid
    @validate(CreateUserForm)
    def f(data):
        try:
            users_create(**data)
            return MakeResponse(status_code=204)
        except RoleNotFound:
            return MakeResponse(status_code=400, data={"detail": "Role with this id does not exist"})
    return f()


@router.route("/update", methods=["POST"])
def users_update_view():
    """Update user view"""
    # validate request data by class. Return 400 if request data is not valid
    @validate(UpdateUserForm)
    def f(data):
        try:
            users_update(**data)
            return MakeResponse(status_code=204)
        except UserNotFound:
            return MakeResponse(status_code=400, data={"detail": "User with this id does not exist"})
        except RoleNotFound:
            return MakeResponse(status_code=400, data={"detail": "Role with this id does not exist"})
    return f()


@router.route("/detail/<int:user_id>", methods=["GET"])
def users_detail_view(user_id):
    """get detail user view"""
    try:
        user = users_detail(user_id)
        return MakeResponse(data=user)
    except UserNotFound:
        return MakeResponse(status_code=400, data={"detail": "User with this id does not exist"})


@router.route("/delete/<int:user_id>", methods=["DELETE"])
def users_delete_view(user_id):
    """delete user view"""
    try:
        users_delete(user_id)
        return MakeResponse(status_code=204)
    except UserNotFound:
        return MakeResponse(status_code=400, data={"detail": "User with this id does not exist"})


@router.route("/roles-list")
def roles_list_view():
    """get roles list view"""
    roles = roles_list()
    return MakeResponse(data=roles)
