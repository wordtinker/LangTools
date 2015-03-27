# -*- coding: utf-8 -*-
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
from baseTableModel import BaseTaBleModel

from PyQt5.QtCore import Qt, pyqtSignal, QFileSystemWatcher, QUrl, QFile,\
    QVariant, QSortFilterProxyModel
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QAbstractItemView,\
    QMainWindow, QProgressDialog, QMessageBox, QHeaderView


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


class FilesModel(BaseTaBleModel):
    headers = ["File", "Size", "Known", "%", "Maybe", "%", "Unknown", "%"]

    def __init__(self):
        super(FilesModel, self).__init__(self.headers)

    def prepare(self):
        super(FilesModel, self).prepare()
        # Add Total line to filesTable
        row = self.add_row("Total", 0, 0, 0.0, 0, 0.0, 0, 0.0)

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        # Make total row bold
        elif role == Qt.FontRole and index.row() == self.rowCount() - 1:
            font = QFont()
            font.setBold(True)
            return QVariant(font)

        elif role != Qt.DisplayRole:
            return QVariant()

        data = self.items[index.row()][index.column()]
        if data and index.column() in [3, 5, 7]:
            data = "{0:.2f}".format(data)
        return QVariant(data)

    def recalculate_total(self):
        """
        Recalculates the total stats for project and puts them into Total line.
        """
        last_row = self.rowCount() - 1

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
            file_size = self.items[i][1]
            if file_size:
                size += file_size
            file_known = self.items[i][2]
            if file_known:
                known += file_known
            file_maybe = self.items[i][4]
            if file_maybe:
                maybe += file_maybe
            file_unknown = self.items[i][6]
            if file_unknown:
                unknown += file_unknown

        if size != 0:
            pknown = known / size
            pmaybe = maybe / size
            punknown = unknown / size

        self.update_row(last_row, self.items[last_row][0], size, known, pknown,
                        maybe, pmaybe, unknown, punknown)


class SortingWithTotal(QSortFilterProxyModel):

    def __init__(self):
        super(SortingWithTotal, self).__init__()

    def lessThan(self, index_1, index_2):
        last_row = self.sourceModel().rowCount() - 1
        if index_1.row() == last_row:
            return False
        elif index_2.row() == last_row:
            return True
        else:
            return super(SortingWithTotal, self).lessThan(index_1, index_2)


class MainWindow(Ui_MainWindow, QMainWindow):

    projectIsReady = pyqtSignal()  # A signal showing that analyze is finished

    def __init__(self, watcher, dic_watcher, storage):
        super(MainWindow, self).__init__()
        # Set up the user interface from Designer.
        self.setupUi(self)

        # Fixing some UI elements
        self.dics_model = BaseTaBleModel(["File", "Type"])
        self.dicsTable.setModel(self.dics_model)
        self.dicsTable.horizontalHeader()\
            .setSectionResizeMode(0, QHeaderView.Stretch)
        self.dicsTable.setSelectionMode(QAbstractItemView.SingleSelection)

        self.words_model = BaseTaBleModel(["Word", "Quantity"])
        self.words_proxy = QSortFilterProxyModel()
        self.words_proxy.setSourceModel(self.words_model)
        self.wordsTable.setModel(self.words_proxy)
        self.wordsTable.setSortingEnabled(True)
        self.wordsTable.horizontalHeader()\
            .setSectionResizeMode(0, QHeaderView.Stretch)

        self.files_model = FilesModel()
        self.files_proxy = SortingWithTotal()
        self.files_proxy.setSourceModel(self.files_model)
        self.filesTable.setModel(self.files_proxy)
        self.filesTable.setSortingEnabled(True)
        self.filesTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.filesTable.horizontalHeader()\
            .setSectionResizeMode(0, QHeaderView.ResizeToContents)
        for header in range(1, self.filesTable.horizontalHeader().count()):
            self.filesTable.horizontalHeader()\
                .setSectionResizeMode(header, QHeaderView.Stretch)

        # Create internal variables
        self.watcher = watcher
        self.dic_watcher = dic_watcher
        self.storage = storage
        self.langs = {}

        # Set signals and slots
        self.languagesBox.currentIndexChanged.connect(self.language_chosen)
        self.languagesBox.activated.connect(self.language_chosen)
        self.projectsBox.currentIndexChanged.connect(self.redraw_files)
        self.projectsBox.currentIndexChanged.connect(self.redraw_dics)
        self.projectsBox.currentIndexChanged.connect(self.redraw_word_list)
        self.filesTable.selectionModel().selectionChanged.connect(self.redraw_word_list)
        self.watcher.directoryChanged.connect(self.redraw_files)
        self.dic_watcher.directoryChanged.connect(self.redraw_dics)
        self.projectIsReady.connect(self.redraw_files)
        self.projectIsReady.connect(self.redraw_word_list)

        self.actionManage.triggered.connect(self.manage_action_triggered)
        self.actionExit.triggered.connect(self.exit_action_triggered)
        self.actionAbout.triggered.connect(self.show_about)

        self.runProject.clicked.connect(self.run_project_clicked)

        self.openFile.clicked.connect(
            self.action_btn_clicked(self.deal_file, self.open_resource)
        )
        self.openUotput.clicked.connect(
            self.action_btn_clicked(self.deal_output, self.open_resource)
        )
        self.openDic.clicked.connect(
            self.action_btn_clicked(self.deal_dic, self.open_resource)
        )

        self.dropFile.clicked.connect(
            self.action_btn_clicked(self.deal_file, self.delete_resource)
        )
        self.dropOutput.clicked.connect(
            self.action_btn_clicked(self.deal_output, self.delete_resource)
        )
        self.dropDic.clicked.connect(
            self.action_btn_clicked(self.deal_dic, self.delete_resource)
        )

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

    def redraw_word_list(self):
        """
        Redraws list of words for chosen project or chosen file
        :return:
        """
        self.words_model.prepare()
        # Get project and output dirs
        project = self.projectsBox.currentText()
        language = self.languagesBox.currentText()
        # Make sure that we are not trying to draw empty projects and lang
        # when projects and languages are deleted
        if not(project and language):
            return

        index = self.filesTable.selectedIndexes()
        if index and index[0].row() != self.files_model.rowCount() - 1:
            # Get words for one file
            file_name = self.files_proxy.index(index[0].row(), 0).data()
            records = self.storage.get_unknown_words_for_file(
                        language, project, file_name)
        else:
            # Get words for whole project
            records = self.storage.get_unknown_words(language, project)

        for record in reversed(records):
            self.words_model.add_row(record[0], record[1])

        self.wordsTable.sortByColumn(1, Qt.DescendingOrder)

    def redraw_dics(self):
        """
        Redraws list of dictionaries used in project.
        :return:
        """
        self.dics_model.prepare()
        # Get project and output dirs
        project = self.projectsBox.currentText()
        language = self.languagesBox.currentText()
        # Make sure that we are not trying to draw empty projects and lang
        # when projects and languages are deleted
        if not(project and language):
            return

        folder = self.langs[language]

        dic_dir = os.path.join(folder, config.dic_dir, project)
        logging.info("dic_dir:" + dic_dir)
        general_dics = os.path.join(folder, config.dic_dir)
        logging.info("general_dics:" + general_dics)

        # Allow watcher to watch for new dictionaries
        self.dic_watcher.set_dirs([dic_dir, general_dics])

        # Add every file from dic and general dic dir
        dictionaries = set(list_dir(dic_dir, config.dic))
        gen_dictionaries = set(list_dir(general_dics, config.dic))

        for file in dictionaries:
            logging.info("Draw dic file:" + file)
            self.dics_model.add_row(file, project)

        for file in gen_dictionaries:
            logging.info("Draw dic file:" + file)
            self.dics_model.add_row(file, "General")

    def redraw_files(self):
        """
        Redraws list of files for chosen project.
        """
        # Clear the widget
        self.files_model.prepare()

        # Get project and output dirs
        project = self.projectsBox.currentText()
        language = self.languagesBox.currentText()
        # Make sure that we are not trying to draw empty projects and lang
        # when projects and languages are deleted
        if not(project and language):
            return

        folder = self.langs[language]
        project_dir = os.path.join(folder, config.corpus_dir, project)
        logging.info("project_dir:" + project_dir)
        output_dir = os.path.join(folder, config.output_dir, project)
        logging.info("output_dir:" + output_dir)

        # Allow watcher to watch new directories
        self.watcher.set_dirs([project_dir, output_dir])

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
                self.files_model.add_row(*record)
                files.remove(file)
                cleared_outputs.remove(file)
            elif in_files:
                self.files_model.add_row(*record)
                files.remove(file)
            elif in_output:
                self.files_model.add_row(*record)
                cleared_outputs.remove(file)
            else:
                to_drop.append(file)

        for file in files:
            logging.info("Draw file from dir:" + file)
            in_output = file in cleared_outputs
            if in_output:
                self.files_model.add_row(file)
                cleared_outputs.remove(file)
            else:
                self.files_model.add_row(file)

        for file in cleared_outputs:
            logging.info("Draw file from output:" + file)
            self.files_model.add_row(file)

        self.files_model.recalculate_total()

        self.filesTable.sortByColumn(7, Qt.AscendingOrder)

        # Drop stats from DB if there is no file for it nor output file
        for dropname in to_drop:
            self.storage.remove_file(dropname, language, project)

    def language_chosen(self):
        """
        Redraws the projects combobox for chosen language.
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
        Manages project analysis and shows progress dialog.
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

        # Test flatten dictionary feature
        # with open('flat_dic.txt', 'w') as flat_dic:
        #     for word in  sorted(lexer.dic.keys()):
        #         flat_dic.write('{}\n'.format(word))

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
                base, ext = os.path.splitext(file)
                out_path =\
                    os.path.join(output_dir, base + config.input[ext])

                if not os.path.exists(out_path) or rowid != -1:
                    html_page = printer.print_page(file, lexi_text)
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

    def action_btn_clicked(self, deal_func, action):

        def func(_self):
            dir_name, project, file_name = deal_func()

            if file_name:
                language = self.languagesBox.currentText()
                folder = self.langs[language]

                path = os.path.join(folder, dir_name, project, file_name)
                action(path)

        return func

    def deal_file(self):
        index = self.filesTable.selectedIndexes()
        if index:
            row = index[0].row()
            if row != self.files_model.rowCount() - 1:
                file_name = self.files_proxy.index(row, 0).data()
                return config.corpus_dir, self.projectsBox.currentText(), file_name
        return None, None, None

    def deal_output(self):
        index = self.filesTable.selectedIndexes()
        if index:
            row = index[0].row()
            if row != self.files_model.rowCount() - 1:
                file_name = self.files_proxy.index(row, 0).data()
                (root, ext) = os.path.splitext(file_name)
                file_name = root + config.input[ext]
                return config.output_dir, self.projectsBox.currentText(), file_name
        return None, None, None

    def deal_dic(self):
        index = self.dicsTable.selectedIndexes()
        if index:
            row = index[0].row()
            file_name = self.dics_model.index(row, 0).data()
            dic_type = self.dics_model.index(row, 1).data()
            if dic_type == "General":
                return config.dic_dir, '', file_name
            else:
                return config.dic_dir, self.projectsBox.currentText(), file_name
        return None, None, None

    def open_resource(self, path):
        logging.info("Opening resource:" + path)
        if os.path.exists(path):
            url = QUrl.fromLocalFile(path)
            QDesktopServices.openUrl(url)
        else:
            msg_box = QMessageBox()
            msg_box.setText("Can't open file.")
            msg_box.exec_()

    def delete_resource(self, path):
        logging.info("Removing resource:" + path)
        if os.path.exists(path):
            file = QFile(path)
            file.remove()
        else:
            msg_box = QMessageBox()
            msg_box.setText("Can't delete file.")
            msg_box.exec_()

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
        # level=logging.INFO)

    logging.info("app_data_path:" + app_data_path)

    try:
        app = QApplication(sys.argv)

        watcher = Watcher()
        dic_watcher = Watcher()
        storage = storage.Storage(os.path.join(app_data_path, config.dbname))
        form = MainWindow(watcher, dic_watcher, storage)

        form.show()

        sys.exit(app.exec_())

    except Exception as e:
        logging.exception(e)