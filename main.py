# This is a sample Python script.
import json

import quart
import quart_cors

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

app = quart_cors.cors(quart.Quart(__name__), allow_origin='https://chat.openai.com')

# 保存待办事项的字典，如果Python会话重新启动，数据将不会持久化。
_TODOS = {}


@app.post('/todos/<string:username>')
async def add_todo(username):
    print('add_todo '+username)
    request_data = await quart.request.get_json(force=True)
    if username not in _TODOS:
        _TODOS[username] = []
    # 存储对应用户的todo数据
    _TODOS[username].append(request_data['todo'])
    return quart.Response(response='OK', status=200)


@app.get('/todos/<string:username>')
async def get_todos(username):
    print('get_todos ' + username)
    return quart.Response(response=json.dumps(_TODOS.get(username, [])), status=200)


@app.delete('/todos/<string:username>')
async def delete_todo(username):
    print('delete_todo ' + username)
    request_data = await quart.request.get_json(force=True)
    todo_idx = request_data['todo_idx']
    # 对于简单的插件，静默处理错误。
    if 0 <= todo_idx < len(_TODOS[username]):
        _TODOS[username].pop(todo_idx)
    return quart.Response(response='OK', status=200)


@app.get('/logo.png')
async def plugin_logo():
    print('plugin_logo ')
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')


@app.get('/.well-known/ai-plugin.json')
async def plugin_manifest():
    host = quart.request.headers['Host']
    print('plugin_manifest '+host)
    with open('./.well-known/ai-plugin.json') as f:
        text = f.read()
        return quart.Response(text, mimetype='text/json')


@app.get('/openapi.yaml')
async def openapi_spec():
    print('openapi_spec ')
    host = quart.request.headers['Host']
    with open('openapi.yaml') as f:
        text = f.read()
        return quart.Response(text, mimetype='text/yaml')


@app.get('/')
async def index():
    print('index ')
    return 'Hello World'


def main():
    print('main ')
    app.run(debug=True,port=5002)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
