import responder
import uuid
from tutil import get_last_modified
from schema import validator
from db import WebsiteDB

api = responder.API()



@api.route("/")
async def index(req, resp):
    # resp.text = "index: {}".format(str(dir(req)))
    resp.text = "index: {}".format(get_last_modified(__file__))



@api.route("/register")
async def register_website(req, resp):

    # POST以外ならreturn
    if req.method.lower() != "post":
        resp.status_code = api.status_codes.HTTP_404
        return


    @api.background.task
    def process_db(id, media):
        # mediaを辞書型に変換する
        media = dict(media.items())
        media["img"] = media["img"]["content"]

        # バリデーション
        if validator.validate(media):
            # データベースに登録
            db = WebsiteDB()
            db.add_website(id=id, **media)
        else:
            print(validator.errors)


    uid = str(uuid.uuid4())
    media = await req.media(format="files")
    process_db(uid, media)

    resp.text = uid
    print(uid)




@api.route("/img/{id}")
def get_image(req, resp, *, id):
    db = WebsiteDB()
    content = db.get_image(id)
    resp.content = content


@api.route("/{id}")
def get_website(req, resp, *, id):
    db = WebsiteDB()
    website = db.get_website(id)

    # IDが登録されていれば
    if website is not None:
        resp.html = api.template("template.html", **website)
    else:
        resp.status_code = api.status_codes.HTTP_404
        resp.html = "<h1>404 Not Found</h1>"





api.run()