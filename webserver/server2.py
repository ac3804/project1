#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following uses the postgresql test.db -- you can use this for debugging purposes
# However for the project you will need to connect to your Part 2 database in order to use the
# data
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@<IP_OF_POSTGRE_SQL_SERVER>/postgres
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@<IP_OF_POSTGRE_SQL_SERVER>/postgres"
#
# Swap out the URI below with the URI for the database created in part 2
DATABASEURI = "postgresql://ac3804:ca52b@104.196.175.120/postgres"
'''#DATABASEURI = "sqlite:///test.db"
'''
#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)


#
# START SQLITE SETUP CODE
#
# after these statements run, you should see a file test.db in your webserver/ directory
# this is a sqlite database that you can query like psql typing in the shell command line:
# 
#     sqlite3 test.db
#
# The following sqlite3 commands may be useful:
# 
#     .tables               -- will list the tables in the database
#     .schema <tablename>   -- print CREATE TABLE statement for table
# 
# The setup code should be deleted once you switch to using the Part 2 postgresql database
#
'''
engine.execute("""DROP TABLE IF EXISTS test;""")
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")

'''
#
# END SQLITE SETUP CODE
#



@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print request.args
  return render_template("index.html")

  #
  # example of a database query
  #
'''  cursor = g.conn.execute("SELECT name FROM test")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()
'''
  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
#  context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
#  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at
# 
#     localhost:8111/another
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#


# Example of adding new data to the database
'''@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  print name
  cmd = 'INSERT INTO test(name) VALUES (:name1), (:name2)';
  g.conn.execute(text(cmd), name1 = name, name2 = name);
  return redirect('/')
'''

@app.route('/my_library', methods=['POST'])
def add():
  songid_form = request.form['sid']
  songid_stringarray = []
  songid_array = []
  if songid_form != '':
    songid_stringarray = songid_form.split(',')
    # songid_array = [int(i) for i in songid_stringarray]
    for i in songid_stringarray:
      if i.isdigit()==False:
        return render_template("bad_input.html")
  songid_array = [int(i) for i in songid_stringarray]
  username = request.form['uid']
  password = request.form['pw']
  cursor1 = g.conn.execute("select u.password from users as u where u.uid = %s", username)
  pwds = []
  for result in cursor1:
    pwds.append(result['password'])
  cursor1.close()
  dpassword2 = []
  dpassword2 = pwds
  if pwds == []:
    return render_template("pw_error.html")  
  cmd1 = 'SELECT L.lib_id FROM user_library as L, users as U WHERE U.uid = L.lib_user AND U.uid LIKE :username1'
  cursor2 = g.conn.execute(text(cmd1), username1=username)
  libraries = []
  for result in cursor2:
    libraries.append(result['lib_id'])
  lib = libraries[0]
  cursor2.close()
  cmd = 'SELECT L.lib_id as Library, S.song_id, S.name as Song, R.name as Artist, A.name as Album, S.length, S.genre, S.release_date, L.date_added FROM song as S, album as A, artist as R, song_in_lib as L WHERE S.song_album = A.album_id AND A.artist_id = R.artist_id AND L.song_id = S.song_id AND L.lib_id LIKE :lib1'
  cursor = g.conn.execute(text(cmd), lib1=lib)
  songsgeneral = []
  for result in cursor:
    songrow = []
    songrow.append(result['library'])
    songrow.append(result['song_id'])
    songrow.append(result['song'])
    songrow.append(result['artist'])
    songrow.append(result['album'])
    songrow.append(result['length'])    
    songrow.append(result['genre'])
    songrow.append(result['release_date'])
    songrow.append(result['date_added'])
    songsgeneral.append(songrow)
  context = dict(data=songsgeneral)
  cursor.close()
  if password != dpassword2[0]:
    return render_template("pw_error.html")
  elif songid_form == '':
    return render_template("my_library.html", **context)
  else:
    cmd1 = "select L.lib_id from user_library as L, users as U where U.uid = L.lib_user AND U.uid = %s"
    cursor4 = g.conn.execute(cmd1, username)
    libs = []
    for result in cursor4:
      libs.append(result['lib_id'])
    lib_id = libs[0]
    cursor4.close()
    cmd = "select L.song_id from song_in_lib as L where L.lib_id = %s AND L.song_id = %s"
    songcheck = 'FALSE'
    for song in songid_array:
      cursor5 = g.conn.execute(cmd, (lib_id, song))
      if cursor5.fetchone() != None:
        songcheck = 'TRUE'
      cursor5.close()
    if songcheck == 'TRUE':
      return render_template("my_library.html", ** context)
    else: 
      q ="INSERT into song_in_lib(lib_id, song_id, date_added) VALUES (%s, %s, CURRENT_DATE)"
      for song in songid_array:
        cursor3 = g.conn.execute(q, (lib_id, song))
        cursor3.close()
      cmd = 'SELECT L.lib_id as Library, S.song_id, S.name as Song, R.name as Artist, A.name as Album, S.length, S.genre, S.release_date, L.date_added FROM song as S, album as A, artist as R, song_in_lib as L WHERE S.song_album = A.album_id AND A.artist_id = R.artist_id AND L.song_id = S.song_id AND L.lib_id LIKE :lib1'
      cursor = g.conn.execute(text(cmd), lib1=lib_id)
      songsgeneral = []
      for result in cursor:
        songrow = []
        songrow.append(result['library'])
        songrow.append(result['song_id'])
        songrow.append(result['song'])
        songrow.append(result['artist'])
        songrow.append(result['album'])
        songrow.append(result['length'])
        songrow.append(result['genre'])
        songrow.append(result['release_date'])
        songrow.append(result['date_added'])
        songsgeneral.append(songrow)
      cursor.close()
      context = dict(data=songsgeneral)
      return render_template("my_library.html", **context)

@app.route('/search_by_song',methods=['POST'])
def search_by_song():
  song = request.form['song']
  name = '%' + song + '%'

  cmd = 'SELECT S.song_id, S.name as Song, R.name as Artist, A.name as Album, S.length, S.genre, S.release_date FROM song as S, album as A, artist as R WHERE S.song_album = A.album_id AND A.artist_id = R.artist_id AND S.name ILIKE :name1'
  cursor = g.conn.execute(text(cmd),name1 = name)
  songsgeneral = []
  for result in cursor:
    songrow = []
    songrow.append(result['song_id'])
    songrow.append(result['song'])
    songrow.append(result['artist'])
    songrow.append(result['album'])
    songrow.append(result['length'])    
    songrow.append(result['genre'])
    songrow.append(result['release_date'])
    songsgeneral.append(songrow)

  cursor.close()
  print songsgeneral
  context = dict(data=songsgeneral)
  return render_template("search.html", **context)


@app.route('/search_by_artist',methods=['POST'])
def search_by_artist():
  artist = request.form['artist']
  name = '%' + artist + '%'
  cmd = 'SELECT S.song_id, S.name as Song, R.name as Artist, A.name as Album, S.length, S.genre, S.release_date FROM song as S, album as A, artist as R WHERE S.song_album = A.album_id AND A.artist_id = R.artist_id AND R.name ILIKE :name1'
  cursor = g.conn.execute(text(cmd),name1 = name)
  songsgeneral = []
  for result in cursor:
    songrow = []
    songrow.append(result['song_id'])
    songrow.append(result['song'])
    songrow.append(result['artist'])
    songrow.append(result['album'])
    songrow.append(result['length'])
    songrow.append(result['genre'])
    songrow.append(result['release_date'])
    songsgeneral.append(songrow)
  cursor.close()
  print songsgeneral
  context = dict(data=songsgeneral)
  return render_template("search.html", **context)



@app.route('/search_by_album',methods=['POST'])
def search_by_album():
  album = request.form['album']
  name = '%' + album + '%'
  cmd = 'SELECT S.song_id, S.name as Song, R.name as Artist, A.name as Album, S.length, S.genre, S.release_date FROM song as S, album as A, artist as R WHERE S.song_album = A.album_id AND A.artist_id = R.artist_id AND A.name ILIKE :name1'
  cursor = g.conn.execute(text(cmd),name1 = name)
  songsgeneral = []
  for result in cursor:
    songrow = []
    songrow.append(result['song_id'])
    songrow.append(result['song'])
    songrow.append(result['artist'])
    songrow.append(result['album'])
    songrow.append(result['length'])
    songrow.append(result['genre'])
    songrow.append(result['release_date'])
    songsgeneral.append(songrow)
  cursor.close()
  print songsgeneral
  context = dict(data=songsgeneral)
  return render_template("search.html", **context)


@app.route('/search',methods=['POST'])
def search():
  return render_template("search.html")



@app.route('/song_recommender', methods=['POST'])
def song_recommender():
  username = request.form['uid']
  password = request.form['pw']
  cursor1 = g.conn.execute("select u.password from users as u where u.uid = %s", username)
  pwds = []
  for result in cursor1:
    pwds.append(result['password'])
  cursor1.close()
  dpassword2 = []
  dpassword2 = pwds
  if pwds == []:
    return render_template("pw_error.html")
  if password != dpassword2[0]:
    return render_template("pw_error.html")  
  cmd1 = 'SELECT L.lib_id FROM user_library as L, users as U WHERE U.uid = L.lib_user AND U.uid LIKE :username1'
  cursor2 = g.conn.execute(text(cmd1), username1=username)
  libraries = []
  for result in cursor2:
    libraries.append(result['lib_id'])
  cursor2.close()
  lib = libraries[0]
  cmd2 = 'select A.artist_id from song as S, album as A, song_in_lib as L where S.song_album = A.album_id AND S.song_id = L.song_id AND L.lib_id LIKE :lib1'
  cursor3 = g.conn.execute(text(cmd2), lib1=lib)
  artist_array = []
  for result in cursor3:
    artist_array.append(result['artist_id'])
  cursor3.close()
  song_array = []
  for artist in artist_array:
    cursor4 = g.conn.execute("select S.song_id from song as S, album as A where S.song_album = A.album_id AND A.artist_id = %s",artist)
    for result in cursor4:
      song_array.append(result[0])
    cursor4.close()
  playlist_songs = []
  cmd4 = "select L.song_id from song_in_lib as L where L.lib_id = %s AND L.song_id = %s"
  for song in song_array:
    cursor5 = g.conn.execute(cmd4, (lib, song))
    if cursor5.fetchone()== None:
      playlist_songs.append(song)
    cursor5.close()
  cmd5 = 'select MAX(CAST(p_id as int)) from comp_playlist'
  cursor6 = g.conn.execute(text(cmd5))
  pids = []
  for result in cursor6:
    pids.append(result[0])
  pid = int(pids[0])
  pid = pid + 1
  cursor6.close()
  cmd6 = "INSERT into comp_playlist(p_user, p_id, date_created) VALUES (%s, %s, CURRENT_DATE)"
  cursor7 = g.conn.execute(cmd6, (username, pid))
  cursor7.close()
  cmd7 = "INSERT into song_in_play(play_id, song_id, date_added) VALUES (%s, %s, CURRENT_DATE)"
  for song in playlist_songs:
    cursor8 = g.conn.execute(cmd7, (pid, song))
    cursor8.close()
  pid1 = str(pid)
  cmd8 = "Select S.song_id, S.name as Song, R.name as Artist, A.name as Album, S.length, S.genre, S.release_date From song as S, artist as R, album as A, song_in_play as P where S.song_id = P.song_id AND P.play_id = %s AND S.song_album = A.album_id AND A.artist_id = R.artist_id"
  cursor9 = g.conn.execute(cmd8, pid1)
  songsgeneral = []
  for result in cursor9:
    songrow = []
    songrow.append(result['song_id'])
    songrow.append(result['song'])
    songrow.append(result['artist'])
    songrow.append(result['album'])
    songrow.append(result['length'])    
    songrow.append(result['genre'])
    songrow.append(result['release_date'])
    songsgeneral.append(songrow)
  cursor9.close()
  context = dict(data=songsgeneral)
 
  return render_template("song_recommender.html", **context)

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
