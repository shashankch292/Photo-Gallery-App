from flask import Flask, request, render_template, jsonify
import os, MySQLdb

app = Flask(__name__)


# Index page
@app.route("/")
def index():
	return render_template("index.html")

# Method to get the details of the image
@app.route("/show", methods=['GET'])
def show():
	album_name = request.form['album_name']
	f_id = request.form['id']
	db = MySQLdb.connect('localhost', 'root','1234','Gallery')
	cur = db.cursor()
	cur.execute('SELECT FROM ' + album_name + 'WHERE ID=' + f_id)
	l = cur.fetchall()
	db.close()
	return jsonify({'id' = l[0][0], 'path' = l[0][1]})

# Method to upload the images
@app.route("/upload", methods=['POST'])
def upload():
	album_name = request.form['album_name']
	file = request.files["file_photo"]
	filename = os.path.join("Photos",file.filename)
	filename = os.path.join(os.getcwd(),filename)
	file.save(filename)

	db = MySQLdb.connect('localhost', 'root','1234','Gallery')
	cur = db.cursor()
	cur.execute("INSERT INTO " + album_name + "(ID, PATH) VALUES ('" + file_id + "', '" + filename + "')")
	db.commit()
	db.close()

	return render_template("index.html"), 201

# Method to remove the image
@app.route("/delete", methods=['DELETE'])
def delete():
	album_name = request.form['album_name']
	f_id = request.form['id']
	db = MySQLdb.connect('localhost', 'root','1234','Gallery')
	cur = db.cursor()
	cur.execute('SELECT FROM ' + album_name + 'WHERE ID=' + f_id)
	l = cur.fetchall()
	path = l[0][1]
	os.remove(path)
	cur = db.cursor()
	cur.execute('DELETE FROM ' + album_name + 'WHERE ID=' + f_id)
	db.commit()
	db.close()

	return render_template("index.html")

if __name__=='__main__':
	app.run(debug=True)
