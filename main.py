# -*- coding: utf-8 -*-

import uuid
import os
import requests
import re

from schema import validator
from db import WebsiteDB
from flask import *

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html', message="Hello")



@app.route("/register", methods=["GET", "POST"])
def register_website():

    # 画像のバリデーション
    img = request.files.get("img")    
    if img is None:
        return abort(400, "invalid image")

    # フォームのバリデーション
    if validator.validate(request.form):
        # データベースに登録
        uid = str(uuid.uuid4())
        db = WebsiteDB()
        db.add_website(id=uid, img=img.read(), **request.form)

        # カードのページへリダイレクト
        return redirect(url_for("get_card", id=uid))
    else:
        print(validator.errors)
        return abort(400, "invalid paramators")



@app.route("/card/<id>")
def get_card(id):
    db = WebsiteDB()
    website = db.get_website(id)

    # IDが登録されていれば
    if website is not None:
        return render_template("card.html", **website)
    else:
        return abort(404, { 'id': id })



@app.route("/thumb/<id>")
def get_image(id):
    db = WebsiteDB()
    content = db.get_image(id)

    #  画像が登録されていれば返す
    if content:
        resp = make_response(content)
        resp.headers["Content-type"] = "Image"
        return resp
    else:
        return abort(404)



@app.route("/meta", methods=["POST"])
def get_meta_info():
    url = request.form.get("url")
    if url is None:
        return abort(400, "invalid url")

    # タイトルとmetaタグの説明を取得
    res = requests.get(url)
    m_title = re.search("<title>(.+?)</title>", res.text, re.S)
    m_desc = re.search("""<meta name=['|"]description['|"] content=['|"](.+?)['|"].+?>""", res.text, re.S)

    # マッチしなければ空文字
    title = m_title.group(1) if m_title else ""
    desc = m_desc.group(1)   if m_desc else ""

    return json.jsonify({"title": title, "description": desc})



if __name__ == "__main__":
    app.run()
    # from os import environ
    # app.run(debug=False, port=environ.get("PORT", 5000))

