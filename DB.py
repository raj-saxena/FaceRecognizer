import sqlite3


class DB:
    connection = sqlite3.connect('FaceRecognizer.db')

    def __init__(self):
        self.dbCursor = self.connection.cursor()
        self.dbCursor.execute("CREATE TABLE IF NOT EXISTS users( mapped_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                              "uuid TEXT NOT NULL UNIQUE );")

    def add(self, uuid):
        self.dbCursor.execute("INSERT INTO users(uuid) values(?)", (uuid,))
        mappedId = self.getId(uuid)
        self.connection.commit()
        return mappedId

    def getId(self, uuid):
        self.dbCursor.execute("SELECT mapped_id FROM users WHERE uuid = ?", (uuid,))
        mappedId = self.dbCursor.fetchone()[0]
        return mappedId

    def getUuid(self, predictedId):
        self.dbCursor.execute("SELECT uuid FROM users WHERE mapped_id = ?", (predictedId,))
        return self.dbCursor.fetchone()

