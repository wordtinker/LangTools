import sys
import os
import logging
import json

from ui.mainWindow import Ui_MainWindow
import manager
import storage
import config
from lang.lexer import Lexer
import lang.printer as printer

from PyQt5.QtCore import Qt, pyqtSignal, QFileSystemWatcher, QUrl, QFile
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QAbstractItemView,\
    QMainWindow, QTableWidgetItem, QProgressDialog, QMessageBox, QHeaderView


app_data_path = None
if "APPDATA" in os.environ:  # We are on Windows
    app_data_path = os.path.join(os.environ["APPDATA"], config.appname)
elif "HOME" in os.environ:  # We are on Linux
    app_data_path = os.path.join(os.environ["HOME"], "." + config.appname)
else:  # Fallback to our working dir
    app_data_path = os.getcwd()

if not os.path.exists(app_data_path):
    os.makedirs(app_data_path)


def list_dir(dir_name, ext_list):
    dir_list = []
    try:
        dir_list = [file for file in os.listdir(dir_name)
                    if os.path.splitext(file)[1] in ext_list]
    except Exception as e:
        logging.exception(e)
        pass

    return dir_list


class Watcher(QFileSystemWatcher):

    def __init__(self):
        super(Watcher, self).__init__()

    def halt(self):
        old_folders = self.directories()
        # Unset directories
        if old_folders:
            self.removePaths(old_folders)

    def set_dirs(self, dirs):
        self.halt()
        # Set new directories
        for folder in dirs:
            logging.info("FileWatcher dirs:" + folder)
            if os.path.exists(folder):
                self.addPath(folder)


class MainWindow(Ui_MainWindow, QMainWindow):

    projectIsReady = pyqtSignal()  # A signal showing that analyze is finished

    def __init__(self, watcher, storage):
        super(MainWindow, self).__init__()
        # Set up the user interface from Designer.
        self.setupUi(self)

        # Fixing some UI elements
        self.dicsTable.horizontalHeader()\
            .setSectionResizeMode(0, QHeaderView.Stretch)
        self.dicsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.wordsTable.horizontalHeader()\
            .setSectionResizeMode(0, QHeaderView.Stretch)
        self.wordsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.filesTable.horizontalHeader()\
            .setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.filesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        for header in range(1, self.filesTable.horizontalHeader().count()):
            self.filesTable.horizontalHeader()\
                .setSectionResizeMode(header, QHeaderView.Stretch)

        # Create internal variables
        self.watcher = watcher
        self.storage = storage
        self.langs = {}

        # Set signals and slots
        self.languagesBox.currentIndexChanged.connect(self.language_chosen)
        self.languagesBox.activated.connect(self.language_chosen)
        self.projectsBox.currentIndexChanged.connect(self.redraw_files_and_dics)
        self.projectsBox.currentIndexChanged.connect(self.redraw_word_list)
        self.filesTable.currentCellChanged.connect(self.redraw_word_list)
        self.watcher.directoryChanged.connect(self.redraw_files_and_dics)
        self.projectIsReady.connect(self.redraw_files_and_dics)
        self.projectIsReady.connect(self.redraw_word_list)

        self.actionManage.triggered.connect(self.manage_action_triggered)
        self.actionExit.triggered.connect(self.exit_action_triggered)
        self.actionAbout.triggered.connect(self.show_about)

        self.runProject.clicked.connect(self.run_project_clicked)

        self.openFile.clicked.connect(self.open_file)
        self.openUotput.clicked.connect(self.open_output)
        self.openDic.clicked.connect(self.open_dic)

        self.dropFile.clicked.connect(self.delete_file)
        self.dropOutput.clicked.connect(self.delete_output)
        self.dropDic.clicked.connect(self.delete_dic)

        # Load initial values
        self.load_initial_values()

    def load_initial_values(self):
        """
        Loads the list of languages into combobox
        """
        languages = self.storage.get_languages()
        for lang, folder in languages:
            self.langs[lang] = folder
            self.languagesBox.addItem(lang)

    def prepare_files_table(self):
        # Clear the widget
        self.filesTable.clearContents()
        self.filesTable.setRowCount(0)
        # Add Total line to filesTable
        self.insert_row_to_files_table("Total", [])
        fnt = QFont()
        fnt.setBold(True)
        self.filesTable.item(0, 0).setFont(fnt)

    def prepare_dics_table(self):
        # Clear the widget
        self.dicsTable.clearContents()
        self.dicsTable.setRowCount(0)

    def prepare_words_table(self):
        # Clear the widget
        self.wordsTable.clearContents()
        self.wordsTable.setRowCount(0)

    def redraw_word_list(self):
        """
        Redraws list of words for chosen project or chosen file
        :return:
        """
        self.prepare_words_table()
        # Get project and output dirs
        project = self.projectsBox.currentText()
        language = self.languagesBox.currentText()
        # Make sure that we are not trying to draw empty projects and lang
        # when projects and languages are deleted
        if not(project and language):
            return

        row = self.filesTable.currentRow()
        if row == -1 or row == self.filesTable.rowCount() - 1:
            # Get words for whole project
            records = self.storage.get_unknown_words(language, project)
        else:
            # Get words for one file
            file_name = self.filesTable.item(row, 0).text()
            records = self.storage.get_unknown_words_for_file(
                language, project, file_name)
        for record in records:
            self.insert_row_to_words_table(record[0], record[1])

    def redraw_files_and_dics(self):
        """
        Redraws list of files for chosen project
        """
        self.prepare_files_table()
        self.prepare_dics_table()

        # Get project and output dirs
        project = self.projectsBox.currentText()
        language = self.languagesBox.currentText()
        # Make sure that we are not trying to draw empty projects and lang
        # when projects and languages are deleted
        if not(project and language):
            return

        folder = self.langs[language]
        project_dir = os.path.join(
            folder, config.corpus_dir, project)
        logging.info("project_dir:" + project_dir)
        output_dir = os.path.join(
            folder, config.output_dir, project)
        logging.info("output_dir:" + output_dir)
        dic_dir = os.path.join(
            folder, config.dic_dir, project)
        logging.info("dic_dir:" + dic_dir)
        general_dics = os.path.join(folder, config.dic_dir)
        logging.info("general_dics:" + general_dics)

        # Allow watcher to watch new directories
        self.watcher.set_dirs([project_dir, output_dir, dic_dir, general_dics])

        # Add every file from dic and general dic dir

        dictionaries = set(list_dir(dic_dir, config.dic))
        gen_dictionaries = set(list_dir(general_dics, config.dic))

        for file in dictionaries:
            logging.info("Draw dic file:" + file)
            self.insert_row_to_dics_table(file, project)

        for file in gen_dictionaries:
            self.insert_row_to_dics_table(file, "General")
            logging.info("Draw dic file:" + file)

        # Add every file from project dir and output dir to table
        files = set(list_dir(project_dir, config.input))
        outputs = set(list_dir(output_dir, config.output))

        # Determine the input file for output file
        cleared_outputs = set()
        for output in outputs:
            base, extension = os.path.splitext(output)
            file_ext = config.output[extension]
            cleared_outputs.add(base + file_ext)

        records = self.storage.get_files_stats(language, project)
        to_drop = []
        for record in records:
            file, *stats = record
            logging.info("Draw file from DB:" + file)
            in_files = file in files
            in_output = file in cleared_outputs

            if in_files and in_output:
                self.insert_row_to_files_table(file, stats, color=Qt.green)
                files.remove(file)
                cleared_outputs.remove(file)
            elif in_files:
                self.insert_row_to_files_table(file, stats, color=Qt.gray)
                files.remove(file)
            elif in_output:
                self.insert_row_to_files_table(file, stats, color=Qt.red)
                cleared_outputs.remove(file)
            else:
                to_drop.append(file)

        for file in files:
            logging.info("Draw file from dir:" + file)
            in_output = file in cleared_outputs
            if in_output:
                self.insert_row_to_files_table(file, [], color=Qt.green)
                cleared_outputs.remove(file)
            else:
                self.insert_row_to_files_table(file, [], color=Qt.gray)

        for file in cleared_outputs:
            logging.info("Draw file from output:" + file)
            self.insert_row_to_files_table(file, [], color=Qt.red)

        self.recalculate_total()

        # Drop stats from DB if there is no file for it nor output file
        for dropname in to_drop:
            self.storage.remove_file(dropname, language, project)

    def insert_stats(self, stats, row=0, fnt=None):
        self.filesTable.setItem(row, 1, QTableWidgetItem(str(stats[0])))
        self.filesTable.setItem(row, 2, QTableWidgetItem(str(stats[1])))
        self.filesTable.setItem(
            row, 3, QTableWidgetItem("{0:.2f}".format(stats[2])))
        self.filesTable.setItem(row, 4, QTableWidgetItem(str(stats[3])))
        self.filesTable.setItem(
            row, 5, QTableWidgetItem("{0:.2f}".format(stats[4])))
        self.filesTable.setItem(row, 6, QTableWidgetItem(str(stats[5])))
        self.filesTable.setItem(
            row, 7, QTableWidgetItem("{0:.2f}".format(stats[6])))
        if fnt:
            for i in range(1, 8):
                self.filesTable.item(row, i).setFont(fnt)

    def insert_row_to_files_table(self, file, stats, row=0, color=Qt.white):
        self.filesTable.insertRow(row)
        self.filesTable.setItem(row, 0, QTableWidgetItem(file))
        self.filesTable.item(row, 0).setBackground(color)
        if stats:
            self.insert_stats(stats)

    def insert_row_to_dics_table(self, file, typeof, row=0):
        self.dicsTable.insertRow(row)
        self.dicsTable.setItem(row, 0, QTableWidgetItem(file))
        self.dicsTable.setItem(row, 1, QTableWidgetItem(typeof))

    def insert_row_to_words_table(self, word, quantity, row=0):
        self.wordsTable.insertRow(row)
        self.wordsTable.setItem(row, 0, QTableWidgetItem(word))
        self.wordsTable.setItem(row, 1, QTableWidgetItem(str(quantity)))

    def language_chosen(self):
        """
        Redraws the projects combobox for chosen language
        """
        # Clear the widget
        self.projectsBox.clear()

        lang = self.languagesBox.currentText()

        if lang:
            # Get known projects from DB
            in_storage = self.storage.get_projects(lang)

            # Add every project from corpus directory
            folder = self.langs[self.languagesBox.currentText()]
            corpus_dir = os.path.join(folder, config.corpus_dir)
            logging.info("Going to check folder for projects:" + corpus_dir)
            if os.path.exists(corpus_dir):
                for directory in next(os.walk(corpus_dir))[1]:
                    self.projectsBox.addItem(directory)
                    if directory in in_storage:
                        in_storage.remove(directory)

            # Remove unused projects from DB
            for proj in in_storage:
                self.storage.remove_project(lang, proj)

    def run_project_clicked(self):
        """
        Fires up the dialog to manage project analysis
        """

        # Get project and language
        project = self.projectsBox.currentText()
        language = self.languagesBox.currentText()
        # Make sure that we are not trying to analyze empty projects and lang
        # when projects and languages are deleted
        if not(project and language):
            return

        # Define working directories
        folder = self.langs[language]
        project_dir = os.path.join(
            folder, config.corpus_dir, project)
        logging.info("Analyze project_dir:" + project_dir)
        output_dir = os.path.join(
            folder, config.output_dir, project)
        logging.info("Analyze output_dir" + output_dir)
        dic_dir = os.path.join(
            folder, config.dic_dir, project)
        logging.info("Analyze dic_dir:" + dic_dir)
        general_dics = os.path.join(folder, config.dic_dir)
        logging.info("Analyze general_dics:" + general_dics)

        # Create folders if some of them are missing
        # Dic and output might be empty on first run
        if not os.path.exists(general_dics):
            os.makedirs(general_dics)
        if not os.path.exists(dic_dir):
            os.makedirs(dic_dir)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # See if we have dictionaries
        dictionaries = set(list_dir(dic_dir, config.dic))
        gen_dictionaries = set(list_dir(general_dics, config.dic))

        if not (dictionaries or gen_dictionaries):
            QMessageBox.information(self, "Information!",
                                    "There are no dictionaries.")
            return
        # Get the list of input files
        files = set(list_dir(project_dir, config.input))

        if not files:
            QMessageBox.information(self, "Information!",
                                    "There are no files.")
            return

        # Build lexer for current project
        lexer = Lexer()

        # Show progressbar and block whole main window
        progress = QProgressDialog("Processing...", "Cancel", 0, 10000, self)
        progress.setMinimumDuration(0)
        progress.setWindowModality(Qt.WindowModal)
        self.menuBar.setEnabled(False)
        progress.setValue(0)

        # See if we have plugin for language
        plugin_name = os.path.join(
            os.getcwd(), config.plugin["folder"],
            language + config.plugin["ext"])
        logging.info("Analyze with plugin_name:" + plugin_name)

        plugin = {}
        try:
            with open(plugin_name, "r") as file:
                plugin = json.loads(file.read())
        except Exception as e:
            logging.exception(e)
            pass
        lexer.load_plugin(plugin)

        # Update progressbar
        progress.setValue(1000)
        QApplication.processEvents()
        if progress.wasCanceled():
            return

        # Load dictionaries
        for file in dictionaries:
            dic_path = os.path.join(dic_dir, file)
            logging.info("Analyze with dic:" + dic_path)
            try:
                with open(dic_path, 'r', encoding="utf-8") as d_file:
                    lexer.load_dictionary(d_file)
            except Exception as e:
                logging.exception(e)
                pass

        # Load general dictionaries
        for file in gen_dictionaries:
            dic_path = os.path.join(general_dics, file)
            logging.info("Analyze with dic:" + dic_path)
            try:
                with open(dic_path, 'r', encoding="utf-8") as d_file:
                    lexer.load_dictionary(d_file)
            except Exception as e:
                logging.exception(e)
                pass

        # Update progressbar
        progress.setValue(2000)
        QApplication.processEvents()
        if progress.wasCanceled():
            return

        # Expand dictionary
        lexer.expand_dic()

        # Update progressbar
        progress.setValue(3000)
        QApplication.processEvents()
        if progress.wasCanceled():
            return

        # Analyze project files
        step = 7000/len(files)
        self.watcher.halt()  # Stop watching for directories, so the generated
        # outputs wont be redrawn immediately. Emit signal afterward.
        for file in files:
            file_path = os.path.join(project_dir, file)
            logging.info("Analyze the file:" + file_path)
            text_size = None
            try:
                with open(file_path, 'r', encoding="utf-8") as i_file:
                    lexi_text, dic_unknown, text_size, known, maybe =\
                        lexer.analyze(i_file)
            except Exception:
                logging.exception(e)
                pass

            if text_size is not None:  # Analysis was sucessful
                rowid = self.storage.stat_changed(
                        language, project, file, text_size, known, maybe)

                if rowid != -1:
                    self.storage.update_stat(rowid,
                        language, project, file, text_size, known, maybe)
                    self.storage.update_words(
                        language, project, file, dic_unknown)

                    # Save marked text to output dir
                    html_page = printer.print_page(file, lexi_text)
                    base, ext = os.path.splitext(file)
                    out_path =\
                        os.path.join(output_dir, base + config.input[ext])
                    logging.info("Writing output to:" + out_path)
                    try:
                        with open(out_path, 'w', encoding='utf-8') as a_file:
                            a_file.write(html_page)
                    except Exception:
                        logging.exception(e)
                        pass

            # Update progressbar
            new_value = progress.value() + step
            progress.setValue(new_value)
            QApplication.processEvents()
            if progress.wasCanceled():
                break

        # Close progress bar
        old_known, old_maybe = self.storage.get_total_stats(language, project)
        if not old_known:
            old_known = 0
        if not old_maybe:
            old_maybe = 0
        self.storage.batch_update_words()
        self.storage.batch_update_stats()
        progress.setValue(10000)
        progress.close()
        self.menuBar.setEnabled(True)

        self.projectIsReady.emit()

        new_known, new_maybe = self.storage.get_total_stats(language, project)
        if not new_known:
            new_known = 0
        if not new_maybe:
            new_maybe = 0
        QMessageBox.information(
            self, "Project changed.", "Known words:{0} Maybe words:{1}"
            .format(new_known - old_known, new_maybe - old_maybe))

    def manage_action_triggered(self):
        """
        Fires up the widget to manage languages
        """
        lang_manager = manager.LangManager(self.storage)
        lang_manager.langListHasChanged.connect(self.language_changed)

        self.menuBar.setEnabled(False)

        lang_manager.exec_()

        self.menuBar.setEnabled(True)

    def language_changed(self):
        """
        Redraw the list of languages
        """
        self.languagesBox.clear()
        self.langs = {}
        self.load_initial_values()

    def files_table_item_value(self, row, col):
        """
        Little helper function that returns the value of cell or Zero
        """
        item = self.filesTable.item(row, col)
        if item is not None:
            return int(item.text())
        return 0

    def recalculate_total(self):
        last_row = self.filesTable.rowCount() - 1

        size = 0
        known = 0
        pknown = 0
        maybe = 0
        pmaybe = 0
        unknown = 0
        punknown = 0

        fnt = QFont()
        fnt.setBold(True)

        for i in range(last_row):
            size += self.files_table_item_value(i, 1)
            known += self.files_table_item_value(i, 2)
            maybe += self.files_table_item_value(i, 4)
            unknown += self.files_table_item_value(i, 6)

        if size != 0:
            pknown = known/size
            pmaybe = maybe/size
            punknown = unknown/size

        self.insert_stats(
            [size, known, pknown, maybe, pmaybe, unknown, punknown],
            last_row, fnt)

    def deal_file(self, func):
        row = self.filesTable.currentRow()
        if row != -1 and row != self.filesTable.rowCount() - 1:
            background = self.filesTable.item(row, 0).background()
            if background != Qt.red:
                file_name = self.filesTable.item(row, 0).text()
                func(config.corpus_dir, file_name)

    def open_file(self):
        self.deal_file(self.open_resource)

    def delete_file(self):
        self.deal_file(self.delete_resource)

    def deal_output(self, func):
        row = self.filesTable.currentRow()
        if row != -1 and row != self.filesTable.rowCount() - 1:
            background = self.filesTable.item(row, 0).background()
            if background in [Qt.green, Qt.red]:
                file_name = self.filesTable.item(row, 0).text()
                (root, ext) = os.path.splitext(file_name)
                file_name = root + config.input[ext]
                func(config.output_dir, file_name)

    def open_output(self):
        self.deal_output(self.open_resource)

    def delete_output(self):
        self.deal_output(self.delete_resource)

    def deal_dic(self, func):
        row = self.dicsTable.currentRow()
        if row != -1:
            file_name = self.dicsTable.item(row, 0).text()
            dic_type = self.dicsTable.item(row, 1).text()
            if dic_type == "General":
                func(config.dic_dir, file_name, gen=True)
            else:
                func(config.dic_dir, file_name)

    def open_dic(self):
        self.deal_dic(self.open_resource)

    def delete_dic(self):
        self.deal_dic(self.delete_resource)

    def open_resource(self, subfolder, file_name, gen=False):
        project = self.projectsBox.currentText()
        language = self.languagesBox.currentText()
        folder = self.langs[language]
        if not gen:
            url = QUrl.fromLocalFile(
                os.path.join(folder, subfolder, project, file_name))
        else:
            url = QUrl.fromLocalFile(
                os.path.join(folder, subfolder, file_name))
        logging.info("Opening resource:" + url.toString())
        QDesktopServices.openUrl(url)

    def delete_resource(self, subfolder, file_name, gen=False):
        project = self.projectsBox.currentText()
        language = self.languagesBox.currentText()
        folder = self.langs[language]
        if not gen:
            file = QFile(os.path.join(folder, subfolder, project, file_name))
        else:
            file = QFile(os.path.join(folder, subfolder, file_name))
        logging.info("Removing resource:" + file.fileName())
        file.remove()

    def show_about(self):
        QMessageBox.information(
            self, "About",  " ".join([config.appname, config.appversion]))

    def exit_action_triggered(self):
        self.close()


if __name__ == '__main__':
    log_name = os.path.join(app_data_path, config.log)

    logging.basicConfig(
        filename=log_name,
        format='%(asctime)s %(message)s',
        level=logging.ERROR)

    logging.info("app_data_path:" + app_data_path)

    try:
        app = QApplication(sys.argv)

        watcher = Watcher()
        storage = storage.Storage(os.path.join(app_data_path, config.dbname))
        form = MainWindow(watcher, storage)

        form.show()

        sys.exit(app.exec_())

    except Exception as e:
        logging.exception(e)
