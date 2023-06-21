from bottle import template, request, redirect
import json, pprint
import persist

def get_import():
    return template("import")


def post_import(db):
    upfile = request.files.get("upfile")
    if not upfile:
        redirect("/import")
    if upfile.content_type != 'application/json':
        return "Only JSON files allowed"

    rawdata = upfile.file.read()  # upfile.file

    data = json.loads(rawdata)
    fmtdata = pprint.pformat(data, indent=2)

    last_id = persist.db_persist_parse(db, data)
    redirect(f"/details/{last_id}")
