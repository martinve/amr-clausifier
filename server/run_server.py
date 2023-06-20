import bottle
from bottle import run, error, static_file
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine

import persist
import settings as cnf
from models import Base

engine = create_engine(f"sqlite:///{cnf.dbfile}")

app = bottle.Bottle()
plugin = sqlalchemy.Plugin(engine, Base.metadata, keyword="db", create=True, commit=True)
app.install(plugin)

import static_controller
import parse_controller
import import_controller
import sentence_controller
import passage_controller

def is_authenticated_user(db, user, password):
    return True


@error(404)
def error404():
    return static_file("error.html", root='./public')


def serve_static(filename):
    return static_file(filename, root='public/')


def setup_routing(app):
    app.route("/", "GET", passage_controller.index)

    app.route("/import", "GET", import_controller.get_import),
    app.route("/import", "POST", import_controller.post_import),

    app.route("/parse", "GET", parse_controller.index)
    app.route('/parse', "POST", parse_controller.update)

    app.route("/flush", "GET", persist.recreate_data)

    app.route("/passage/:id/add", "GET", passage_controller.add_sent_to_passage)
    app.route("/passage/:id/sentences", "GET", sentence_controller.passage)
    app.route("/passage/:id", "GET", passage_controller.get_passage)
    app.route("/passage/:id/delete", "GET", passage_controller.delete)

    app.route("/test", "GET", passage_controller.test_logic)
    app.route("/resources", "GET", static_controller.resources)

    app.route("/sentences", "GET", sentence_controller.index)
    app.route("/sentences/:id", "GET", sentence_controller.get_sentence)
    app.route("/sentences/:id/logic", "GET", sentence_controller.sentence_update_logic)
    app.route("/sentences/refresh", "GET", sentence_controller.update_all)
    app.route("/sentences/:id/delete", "GET", sentence_controller.delete)

    app.route("/process", "GET", sentence_controller.sentence_process)
    app.route('/<filename:path>', serve_static)



setup_routing(app)

session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': 'secret!',
    'session.httponly': True,
    'session.timeout': 3600 * 24,  # 1 day
    'session.type': 'cookie',
    'session.validate_key': True,
}
# app = SessionMiddleware(app, session_opts)


if __name__ == '__main__':
    run(host=cnf.host, port=cnf.port, app=app, debug=True, reloader=True)
