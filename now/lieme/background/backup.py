import functools
from flask import Flask, jsonify, request, json, make_response
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from common import ParseHtml, MONGO, reader_html
# import json

app = Flask(__name__)

PARSE = ParseHtml()


def create_token(api_user):
    '''
    生成token
    :param api_user:用户id
    :return: token
    '''

    s = Serializer('lierui#000Y')
    token = s.dumps({"id": api_user}).decode("ascii")
    return token


def verify_token(token):
    '''
    校验token
    :param token: 
    :return: 用户信息 or None
    '''

    s = Serializer('lierui#000Y')
    try:
        data = s.loads(token)
    except Exception:
        return None

    user = User.query.get(data["id"])
    return user


def login_required(view_func):
    @functools.wraps(view_func)
    def verify_token(*args, **kwargs):

        return view_func(*args, **kwargs)

        try:
            token = request.cookies.get("token")
            # token = request.headers["z-token"]
        except Exception:
            return jsonify(code=4103, msg='缺少参数token')

        s = Serializer('lierui#000Y')
        try:
            s.loads(token)
        except Exception:
            return jsonify(code=4101, msg="登录已过期")

        return view_func(*args, **kwargs)

    return verify_token


def get_post_data():
    """
    从请求中获取参数
    :return:
    """
    data = {}
    if request.content_type.startswith('application/json'):
        data = request.get_data()
        data = json.loads(data)
    else:
        for key, value in request.form.items():
            if key.endswith('[]'):
                data[key[:-2]] = request.form.getlist(key)
            else:
                data[key] = value
    return data


def headers(data={}, code=200, message='成功', success=True, cookie=None):
    result = {}
    result['code'] = code
    result['data'] = data
    result['message'] = message
    result['message'] = message

    response = make_response(jsonify(result))
    response.headers['Vary'] = 'Origin'
    response.headers['Vary'] = 'Access-Control-Request-Method'
    response.headers['Vary'] = 'Access-Control-Request-Headers'
    response.headers['Access-Control-Allow-Origin'] = '*'
    if cookie:
        response.set_cookie('token', cookie)
    return response


@app.errorhandler(404)
@login_required
def not_found(error):
    return jsonify({'error': 'NOT FOUND'}), 404


@app.route('/parse/update', methods=['GET', 'POST'])
@login_required
def parse_update():
    data = get_post_data()
    # MONGO.insert(data, 'update')
    # {
    #     'email': '',
    #     'mobile': '',
    #     'resumeId': '1',
    #     'text': '\n\n\n\n<div id="h-...</script>',
    #     'updateType': 'new',
    #     'userId': '11'
    # }
    return headers()


@app.route('/parse/import', methods=['GET', 'POST'])
@login_required
def parse_import():
    data = get_post_data()
    account = data.get('account')
    text = data.get('text')

    PARSE._import(text)

    return headers()


@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    data = get_post_data()
    account = data.get('account')
    password = data.get('password')

    result = MONGO.select('user', {'account': account}, _id=False)

    if not result:
        return headers(code=201, message='账号不存在')
    if result.get('password') != password:
        return headers(code=202, message='密码不正确')

    result.pop('_id')
    # result.pop('account')
    result.pop('password')

    create_token(str(result.get('_id')))

    return headers(result)


@app.route('/user/unlogin', methods=['GET', 'POST'])
def user_unlogin():
    data = get_post_data()
    account = data.get('account')

    # result = MONGO.select('user', {'account': account}, _id=False)

    return headers()


@app.route('/candidate/', methods=['GET'])
@login_required
def candidate():
    _id = request.args.get('id')
    return reader_html(_id)


@app.route('/parse/html', methods=['GET', 'POST'])
@login_required
def parse_html():
    data = get_post_data()
    account = data.get('account')
    text = data.get('text')

    return headers({
        "relationResume": None,
        "relationCompanyResume": PARSE.parse(text),
        "resumeEntity": None
    })

    # data = {}
    # data['relationResume'] = result.get('relationResume')
    # data['relationOldResume'] = result.get('relationOldResume')
    # data['html'] = result.get('html')
    # data['name'] = result.get('name')
    # data['basic'] = result.get('basic')
    # data['works'] = result.get('works')
    # data['edus'] = result.get('edus')
    # data['projects'] = result.get('projects')
    # data['resumeEntity'] = result.get('resumeEntity')


@app.route('/set_cookie', methods=['GET', 'POST'])
def set_cookie():
    resp = make_response("success")
    resp.set_cookie("Itcast_1", "python_1")
    return resp


@app.route("/get_cookie")
def get_cookie():
    cookie_1 = request.cookies.get("Itcast_1")
    return cookie_1


@app.route("/del_cookie")
def del_cookie():
    resp = make_response("del success")
    resp.delete_cookie("Itcast1")
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=32767)
    # uwsgi -s /tmp/uwsgi.sock -w backup:app --chdir /home/xuan/git/Workoo/now/lieme/background/ --chmod-socket=666
