from flask import Flask, jsonify, request, json, make_response
from common import MongoOpea, ParseHtml
# import json

app = Flask(__name__)
MONGO = MongoOpea()
PARSE = ParseHtml()


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


def headers(data={}, code=200, message='成功', success=True):
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
    return response


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'NOT FOUND'}), 404


@app.route('/parse/update', methods=['GET', 'POST'])
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
def parse_import():
    data = get_post_data()
    # MONGO.insert(data, 'update')
    PARSE.parse(data.get('text'))

    return headers()


@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    data = get_post_data()
    account = data.get('account')
    password = data.get('password')
    with open('./data.txt','a',encoding='utf-8') as fn:
        fn.write(account)
        fn.write(password)

    result = MONGO.select('user', {'account': account}, _id=False)
    if not result:
        return headers(code=201, message='账号不存在')
    if result.get('password') != password:
        return headers(code=202, message='密码不正确')

    result.pop('_id')
    result.pop('account')
    result.pop('password')
    return headers(result)


@app.route('/parse/html', methods=['GET', 'POST'])
def parse_html():
    data = get_post_data()
    result = PARSE.parse(data.get('text'))

    return headers({
        "html":
        None,
        "name":
        None,
        "basic":
        None,
        "works":
        None,
        "edus":
        None,
        "projects":
        None,
        "relationResume": [{
            "name": "陆少舟",
            "sex": 1,
            "birthday": "2020/12/10",
            "last_edu": 1,
            "update_time": "2020/12/10",
            "id": 1
        },{
            "name": "陆少舟",
            "sex": 1,
            "birthday": "2020/12/10",
            "last_edu": 1,
            "update_time": "2020/12/10",
            "id": 3
        },{
            "name": "陆少舟",
            "sex": 1,
            "birthday": "2003/12/10",
            "last_edu": 1,
            "update_time": "2080/12/10",
            "id": 6
        }],
        "relationOldResume": [{
            "name_chi": "陆少舟",
            "sex": 1,
            "birthday2": "2020/12/10",
            "percent": "11",
            "degree": 5,
            "cv_update_time": "2020/12/10",
            "id": 1
        },{
            "name_chi": "陆少舟",
            "sex": 1,
            "birthday2": "2020/12/10",
            "percent": "23",
            "degree": 5,
            "cv_update_time": "2020/12/10",
            "id": 1
        }],
        "resumeEntity":
        None
    })
    if not result:
        return headers()

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

    return headers(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=32767)
    # uwsgi -s /tmp/uwsgi.sock -w backup:app --chdir /home/xuan/git/Workoo/now/lieme/background/ --chmod-socket=666
