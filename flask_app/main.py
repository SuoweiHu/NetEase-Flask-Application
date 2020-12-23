from flask import Flask, request, render_template

app = Flask(__name__) # Flask web应用实例

# 主页面 index.html
@app.route('/') 
def index():
    return render_template("index.html")

# 登录页面 login.html
@app.route('/login', methods=['GET', "POST"])
def login():
    # 如果HTTP方法为GET,那么就是用args方法获得请求参数
    if(request.method == "GET"):
        query_dict = dict(request.args)
        return str(query_dict)
    # 如果HTTP方法为GET,那么就是用form方法获得请求参数
    elif(request.method == "POST"):
        query_dict = dict(request.form)
        return str(query_dict)
    else:
        return "<h1> Unknown HTTP request method. </h1>"
 
# 等待页面 wait.html
@app.route('/wait')
def wait():
    return "<h1> Waiting for crawler to finish... </h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9512, debug=True)
    