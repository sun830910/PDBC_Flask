# You should not import any additional modules
# You can, however, import additional functionalities 
# from the flask and sqlite3 modules


from flask import Flask, render_template, request
import sqlite3
import logging
import regex

app = Flask(__name__)


def get_data_from_db(database, table, attribute):
    result = set()
    try:
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT {table}.{attribute} FROM {table}".format(table=table, attribute=attribute))
        sql_result = cur.fetchall()
        for idx in sql_result:
            result.add(idx[attribute])
    except Exception as e:
        logging.warning("Can't get {attribute} from {table}: {error}".format(attribute=attribute, table=table, error=e))
    return result


def is_float(sentence):
    pattern = "^\d.*\.\d.*$"
    if regex.search(pattern, sentence) != None:
        return True
    return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add/')
def add():
    return render_template('add.html')


@app.route('/collection/')
def collection():
    conn = sqlite3.connect("iMusic.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        "SELECT Album.Title AS Title, Artist.Name AS Name, Track.UnitPrice AS Value, (Track.Milliseconds/1000) AS Duration From Album, Artist, Track where Album.AlbumId=Artist.ArtistId AND Track.TrackId=Album.AlbumId")
    rows = cur.fetchall()
    return render_template('collection.html', rows=rows)


@app.route('/add/track', methods=['POST'])
def addtrack():
    Name = request.form['Name']
    AlbumId = request.form['AlbumId']
    GenreId = request.form['GenreId']
    Composer = request.form['Composer']
    Seconds = request.form['Seconds']
    UnitPrice = request.form['UnitPrice']

    reason = set()
    database = "iMusic.db"
    table = "Track"
    with sqlite3.connect(database) as conn:
        AlbumId_set = get_data_from_db(database, table, "AlbumId")
        GenreId_set = get_data_from_db(database, table, "GenreId")

        # Name
        if len(Name) == 0:
            reason.add("A track name must be provided")
        if len(Name) > 200:
            reason.add("A track's name cannot exceed 200 characters")

        # AlbumId
        try:
            AlbumId = int(AlbumId)
            if AlbumId not in AlbumId_set:
                reason.add("The specified AlbumId does not exist in the DB.")
        except ValueError:  # 若AlbumId转换失败，即字符串中含有其他不能转换成数字的因素存在如"100a"
            reason.add("The specified AlbumId does not exist in the DB.")

        # GenreId
        try:
            GenreId = int(GenreId)
            if GenreId not in GenreId_set:
                reason.add("The specified GenreId does not exist in the DB.")
        except ValueError:
            reason.add("The specified GenreId does not exist in the DB.")

        # Seconds
        try:
            Seconds = int(Seconds)
            if Seconds == 0:
                reason.add("The specified duration is too short. Must be greater than zero.")
        except ValueError:
            reason.add("The specified Milliseconds is too short. Must be greater than zero.")

        # UnitPrice
        try:
            UnitPrice_float = float(UnitPrice)
            if not is_float(UnitPrice) or UnitPrice_float == 0:
                reason.add("The specified price is invalid.")
        except ValueError:
            reason.add("The specified price is invalid.")

        if len(reason) != 0:
            return render_template('add.html', error=1, msg=reason)

        try:
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO Track (Name, AlbumId, GenreId, Composer, Milliseconds, UnitPrice) VALUES (?,?,?,?,?,?)',
                (Name, AlbumId, GenreId, Composer, Seconds * 10000, UnitPrice))
            conn.commit()
            return collection()

        except Exception as e:
            logging.warning("Insert to Track API Error: {}".format(e))


@app.route('/tracks/<string:albumID>')
def tracks(albumID):
    """
    Note!
    1) There is no need to modify this code, there is no task/marks associated with this.
    2) The code in this function does not neccessarily follow best practices.
    Your solutions to Tasks 2& 3 need to consider more things than are performed here.
    For example, this solution does not handle errors at all. Your solutions should!
    There are many other incomplete functionalities missing from this code, so be careful
    if this is the only code you are reviewing ...
    """

    # Connect to our database
    con = sqlite3.connect("iMusic.db")
    # Specify how we want to receive results
    con.row_factory = sqlite3.Row
    # Obtain a cursor for executing queries
    cur = con.cursor()
    # Query our DB for all tracks
    cur.execute("""SELECT Name, Composer, ((Milliseconds/1000)) AS Seconds, UnitPrice as Price 
                   FROM Track 
                   WHERE AlbumId = ?;""", (albumID,))
    # Obtain all tracks
    tracks = cur.fetchall()

    # Get the Album Title and Artist Name
    cur.execute('SELECT Title, Name FROM Album NATURAL JOIN Artist WHERE AlbumId = ?;', (albumID,))
    # There should only be one album in the result
    album = cur.fetchone()

    # Return the track information to the 
    return render_template('tracks.html', tracks=tracks, album=album)


if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
