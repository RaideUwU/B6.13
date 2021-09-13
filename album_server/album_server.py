from bottle import run
from bottle import route
from bottle import HTTPError
from bottle import request

import album

@route("/albums/<artist>")
def artist(artist):
	album_list = album.find(artist)
	if not album_list:
		result = HTTPError(400, "Список альбомов {} не найдено :(".format(artist))
	else:
		result = "Список альбомов {}: ".format(artist)
		for i in album_list:
			result += i.album + ", "
	return result

@route("/albums", method="POST")
def new_album():
	new_album = {
		"year": request.forms.get("year"),
		"artist": request.forms.get("artist"),
		"genre": request.forms.get("genre"),
		"album": request.forms.get("album"),
	}

	try:
		new_album["year"] = int(new_album["year"])
	except TypeError:
		return HTTPError(409, "Неверный год!")

	if album.check_album(new_album["album"]):
		album.add_album(new_album)
	else:
		return HTTPError(409, "Данный альбом уже существует!")

if __name__ == "__main__":
	run(host="localhost", port=8000, debug=True)