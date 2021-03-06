# -*- coding: utf-8 -*-
import sqlite3


class Storage():

    def __init__(self, db_path):
        self.db_path = db_path
        self.db_conn = sqlite3.connect(db_path)

        # Initialize tables
        self.db_cursor = self.db_conn.cursor()
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS Languages(
        lang TEXT, directory TEXT)""")
        self.db_conn.commit()

        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS Files(
        name TEXT, lang TEXT, project TEXT, size INTEGER, known INTEGER,
        pknown REAL, maybe INTEGER, pmaybe REAL, unknown INTEGER,
        punknown REAL)""")
        self.db_conn.commit()

        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS Words(
        word TEXT, lang TEXT, project TEXT, file TEXT, quantity INTEGER)""")
        self.db_conn.commit()

        self.words = []
        self.new_words = []
        self.to_insert = []
        self.to_update = []

    def add_language(self, lang, folder):
        """
        Adds new language and it's folder to DB.
        :param lang:
        :param folder:
        :return:
        """
        db_cursor = self.db_conn.cursor()
        db_cursor.execute('''INSERT INTO Languages
         VALUES (?, ?)''', (lang, folder))
        self.db_conn.commit()

    def batch_update_stats(self):
        """
        Applies the changes and updates the stats for projects given
        before.
        :return:
        """
        db_cursor = self.db_conn.cursor()
        db_cursor.executemany('''INSERT INTO Files
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                              self.to_insert)
        self.db_conn.commit()
        self.to_insert = []

        db_cursor.executemany('''UPDATE Files
            SET size=?, known=?, pknown=?, maybe=?, pmaybe=?, unknown=?,
            punknown=?
            WHERE rowid =?''', self.to_update)
        self.db_conn.commit()
        self.to_update = []

    def update_stat(self, rowid, language, project, file, text_size,
                    known, maybe):
        """
        Updates the stats for the given project. Delayed insert is used.
        Batch_update_stats must be called afterward to apply changes.
        :param rowid:
        :param language:
        :param project:
        :param file:
        :param text_size:
        :param known:
        :param maybe:
        :return:
        """
        pknown = 0.0
        pmaybe = 0.0
        unknown = text_size - known - maybe
        punknown = 0.0
        if text_size > 0:
            pknown = known / text_size
            pmaybe = maybe / text_size
            punknown = unknown / text_size

        if rowid == 0:  # Create new stats row
            self.to_insert.append((file, language, project, text_size, known,
                                   pknown, maybe, pmaybe, unknown, punknown))
        else:  # We have a valid rowid
            self.to_update.append((text_size, known, pknown, maybe, pmaybe,
                                   unknown, punknown, rowid))

    def batch_update_words(self):
        """
        Applies the changes and updates the word lists for projects given
        before.
        :return:
        """
        # Clear old unknown words data
        db_cursor = self.db_conn.cursor()
        db_cursor.executemany('''DELETE FROM Words
        WHERE lang=? AND project=? AND file=?''', self.words)
        self.db_conn.commit()
        self.words = []

        # Set new data
        db_cursor.executemany('''INSERT INTO Words
        VALUES(?, ?, ?, ?, ?)''', self.new_words)
        self.db_conn.commit()
        self.new_words = []

    def update_words(self, language, project, file, dic_unknown):
        """
        Updates the word list for the given project. Delayed insert is used.
        Batch_update_words must be called afterward to apply changes.
        :param language:
        :param project:
        :param file:
        :param dic_unknown:
        :return:
        """
        # Save data that should be deleted in memory
        self.words.append((language, project, file))

        # Save new data in memory
        records = [(word, language, project, file, quantity)
                   for word, quantity in dic_unknown.items()]
        self.new_words += records

    def language_exists(self, lang):
        """
        Checks if the language is used in Table Languages.
        :param lang:
        :return:
        """
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""SELECT lang FROM Languages
         WHERE lang=?""", (lang, ))
        if len(db_cursor.fetchall()) > 0:
            return True
        else:
            return False

    def folder_exists(self, folder):
        """
        Checks if the folder is used in Table Languages.
        :param folder:
        :return:
        """
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""SELECT lang FROM Languages
         WHERE directory=?""", (folder, ))
        if len(db_cursor.fetchall()) > 0:
            return True
        else:
            return False

    def stat_changed(self, language, project, name, size, known, maybe):
        """
        Checks if the statistics of the given file has changed.
        :param language:
        :param project:
        :param name:
        :param size:
        :param known:
        :param maybe:
        :return: -1 if it's unchanged, 0 if there is no record in DB for given
        file, rowid - if there is the record and stats has changed.
        """
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""SELECT rowid, size, known, maybe FROM Files WHERE
         lang=? AND project=? AND name=?""", (language, project, name))
        result = db_cursor.fetchone()
        if result:
            rowid, *stats = result
            if stats == [size, known, maybe]:
                return -1  # Stats unchanged
            else:
                return rowid  # Stats changed
        else:
            return 0  # No record has been found

    def get_languages(self):
        """
        Provides list of pairs [language, project].
        """
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""SELECT lang, directory FROM Languages""")
        return db_cursor.fetchall()

    def get_projects(self, language):
        """
        Return projects for chosen language.
        """
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""SELECT project FROM Files
        WHERE lang=?
        GROUP BY project""", (language, ))
        return [x[0] for x in db_cursor.fetchall()]

    def get_unknown_words(self, language, project):
        """
        Provides the list of unknown words and theirs quantities for given
        language and project.
        :param language:
        :param project:
        """
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""SELECT word, SUM(quantity) as sum FROM Words
        WHERE lang=? AND project=?
        GROUP BY word
        ORDER BY sum DESC
        LIMIT 100""", (language, project))
        return db_cursor.fetchall()

    def get_unknown_words_for_file(self, language, project, file):
        """
        Provides the list of unknown words and theirs quantities for given
        language, project and file.
        :param language:
        :param project:
        :param file
        """
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""SELECT word, quantity FROM Words
        WHERE lang=? AND project=? AND file=?
        ORDER BY quantity DESC""", (language, project, file))
        return db_cursor.fetchall()

    def get_files_stats(self, language, project, filter_value):
        """
        Provides the list of files and corresponding stats for given
        language and project. The list contains files that contain
        filtered_value.
        :param language:
        :param project:
        :return:
        """
        db_cursor = self.db_conn.cursor()
        if filter_value:
            db_cursor.execute("""SELECT F.name, F.size, F.known, F.pknown,
             F.maybe, F.pmaybe, F.unknown, F.punknown
             FROM (SELECT * from Files WHERE lang=:lang AND project=:prj) F
             INNER JOIN (SELECT * FROM Words WHERE lang=:lang
             AND project=:prj AND word LIKE :like) W
             ON F.name = W.file
             GROUP BY F.name
             ORDER BY F.punknown DESC""", {'lang': language,
                                           'prj': project,
                                           'like': filter_value})
        else:
            db_cursor.execute("""SELECT name, size, known, pknown, maybe, pmaybe,
             unknown, punknown FROM Files WHERE
             lang=? AND project=?
             ORDER BY punknown DESC""", (language, project))
        return db_cursor.fetchall()

    def get_total_stats(self, language, project):
        """
        Provides the total and maybe stat of the project.
        :param language:
        :param project:
        :return:
        """
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""SELECT SUM(known), SUM(maybe) FROM Files
         WHERE lang=? AND project=?""", (language, project))
        return db_cursor.fetchone()

    def remove_file(self, name, language, project):
        """
        Removes the stats of the given file from the DB.
        :param name:
        :param language:
        :param project:
        :return:
        """
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""DELETE FROM Files WHERE
        name=? AND lang=? AND project=?""", (name, language, project))
        self.db_conn.commit()

        db_cursor.execute("""DELETE FROM Words
        WHERE lang=? AND project=? and file=?""", (language, project, name))
        self.db_conn.commit()

    def remove_language(self, language):
        """
        Removes the stats of the given language from DB.
        :param language:
        :return:
        """
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""DELETE FROM Languages
        WHERE lang=?""", (language, ))
        self.db_conn.commit()

        db_cursor.execute("""DELETE FROM Files
        WHERE lang=?""", (language, ))
        self.db_conn.commit()

        db_cursor.execute("""DELETE FROM Words
        WHERE lang=?""", (language, ))
        self.db_conn.commit()

    def remove_project(self, lang, project):
        """
        Removes the stats of the given project from DB.
        :param lang:
        :param project:
        :return:
        """
        db_cursor = self.db_conn.cursor()
        db_cursor.execute("""DELETE FROM Files
        WHERE lang=? AND project=?""", (lang, project))
        self.db_conn.commit()

        db_cursor.execute("""DELETE FROM Words
        WHERE lang=? AND project=?""", (lang, project))
        self.db_conn.commit()
