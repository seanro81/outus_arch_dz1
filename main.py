import uuid
import secrets

import datetime
import json
from flask import Flask, request, jsonify
from pydantic import ValidationError

from adapters.orm import users_tbl_crete, authinfo_tbl_crete, SimpleORM
from models.user import UserInfo, User, AuthInfo, Login
from utils.settings import logger

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'


@app.route('/login', methods=['POST'])
def login():
    try:
        input_data = request.json
        login = Login(**input_data)

        orm = SimpleORM()
        auth: AuthInfo = orm.get_auth(login.id)
        if auth is None:
            logger.error(f"/login: Пользователь {login.id} не найден")
            return {
                "message": f"Пользователь не найден",
                "request_id": login.id,
                "code": 404
            }, 404
        if auth.password == login.password:
            logger.info(f"/login: Пользователь {login.id} Успешно Аутентифицирован")
            return {"token": auth.token}
        else:
            logger.error(f"/login: Не верный пароль или идентификатор пользователя")
            return {
                "message": f"Не верный пароль или идентификатор пользователя",
                "request_id": login.id,
                "code": 404
            }, 404
    except ValidationError as v_ex:
        logger.error(f"/login: {str(v_ex)} ")
        return {
            "message": str(v_ex),
            "request_id": "",
            "code": 400
        }, 400
    except Exception as e_ex:
        logger.error(f"/login: {str(e_ex)} ")
        return {
            "message": str(e_ex),
            "request_id": "",
            "code": 500
        }, 500


@app.route('/user/get/<string:id>', methods=['GET'])
def get_user(id: str):
    try:
        orm = SimpleORM()
        user: UserInfo = orm.get_user_info_by_id(id)
        if user is not None:
            logger.info(f"/user/get найден Пользователь: {id} с именем: {user.first_name}")
            return user.model_dump_json(), 200
        else:
            logger.error(f"/user/get Пользователь: {id} не найден")
            return {
                "message": "Анкета не найдена",
                "request_id": id,
                "code": 404
            }, 404

    except ValidationError as v_ex:
        logger.error(f"/user/get:  {str(v_ex)} ")
        return {
            "message": str(v_ex),
            "request_id": "",
            "code": 400
        }, 400
    except Exception as e_ex:
        logger.error(f"/user/get: {str(e_ex)} ")
        return {
            "message": str(e_ex),
            "request_id": "",
            "code": 500
        }, 500


@app.route('/user/register', methods=['POST'])
def register():
    try:
        input_data = request.json
        input_data['id'] = str(uuid.uuid4())
        user = User(**input_data)

        token = secrets.token_hex(20)

        t_s = datetime.datetime.now(tz=datetime.timezone.utc)
        event_date = str(t_s.isoformat(sep=' ', timespec='milliseconds'))

        auth = AuthInfo(id=user.id,
                        password=user.password,
                        token=token,
                        token_create_dt=event_date,
                        token_valid_dt=event_date
                        )

        orm = SimpleORM()
        orm.user_register(user, auth)
        logger.info(f"/user/register: успешно зарегистрирован новый Пользователь:{user.id}")
        return {"user_id": user.id}, 200
    except ValidationError as v_ex:
        logger.error(f"/user/register: {str(v_ex)} ")
        return {
            "message": str(v_ex),
            "request_id": "",
            "code": 400
        }, 400
    except Exception as e_ex:
        logger.error(f"/user/register: {str(e_ex)} ")
        return {
            "message": str(e_ex),
            "request_id": "",
            "code": 500
        }, 500


if __name__ == "__main__":

    logger.info("Запуск скрипта миграции: Создание таблиц users и authinfo, если они не созданы и добавление тестового пользователя 6d082945-4db0-41cd-945f-da21e78f7da5 для коллекции запросов, если таблицы пустые ")
    orm = SimpleORM()
    orm.migration()

    """
      Осталось сделать 
      1) миграция - создание таблиц при запуске if not exist  +++
      2) тестовых пользователей добавить для коллекции        +++
      3) логирование добавить к методам                       +++
      4) Описание md файл (взять с Кафки)                     +++
      6) dockerfile
      7) dockercompose
      8) добавить в репозиторий
      9) добавить заполненную коллекцию запросов
      10) подумать на кастомизацией ошибки 503               нет 
    """

    app.run(host="0.0.0.0", port=5000, debug=True)
