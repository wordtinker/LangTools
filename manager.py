import os
import logging

from ui.langManager import Ui_languagesDialog
import config

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItem, QDialog, QFileDialog, QMessageBox


class LangManager(Ui_languagesDialog, QDialog):

    langListHasChanged = pyqtSignal()

    def __init__(self, storage):
        super(LangManager, self).__init__()
        self.setupUi(self)

        self.storage = storage

        # Load languages as initial state
        self.initialize()

        # Connect signals and slots
        self.removeButton.clicked.connect(self.remove_button_clicked)
        self.addButton.clicked.connect(self.add_button_clicked)
        self.folderButton.clicked.connect(self.folder_button_clicked)

    def initialize(self):
        languages = self.storage.get_languages()
        for inx, row in enumerate(languages):
            self.add_lang_row(inx, row)

    def add_lang_row(self, inx, row):
        self.languagesTable.insertRow(inx)
        self.languagesTable.setItem(inx, 0, QTableWidgetItem(row[0]))
        self.languagesTable.setItem(inx, 1, QTableWidgetItem(row[1]))

    def remove_button_clicked(self):
        # Drop the language from DB
        current_row = self.languagesTable.currentRow()

        if current_row > -1:
            current_lang = self.languagesTable.item(current_row, 0).text()
            self.storage.remove_language(current_lang)

            self.languagesTable.removeRow(current_row)

            self.langListHasChanged.emit()

    def add_button_clicked(self):
        lang = self.langEdit.text()
        folder = self.folderEdit.text()
        logging.info("Going to add new lang folder:" + folder)
        if self.validate_fields():
            # Add new lang to DB, and redraw the list of languages.
            self.storage.add_language(lang, folder)

            self.add_lang_row(0, (lang, folder))
            self.langEdit.clear()
            self.folderEdit.clear()

            # Create subfolders in that folder.
            dic_dir = os.path.join(folder, config.dic_dir)
            logging.info("Create:" + dic_dir)
            corpus_dir = os.path.join(folder, config.corpus_dir)
            logging.info("Create:" + corpus_dir)
            output_dir = os.path.join(folder, config.output_dir)
            logging.info("Create:" + output_dir)
            try:
                if not os.path.exists(corpus_dir):
                    os.makedirs(corpus_dir)
                if not os.path.exists(dic_dir):
                    os.makedirs(dic_dir)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
            except OSError as e:
                msg_box = QMessageBox()
                msg_box.setText(str(e))
                msg_box.exec_()
            self.langListHasChanged.emit()

    def folder_button_clicked(self):
        # Let the user choose folder
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly)

        if dialog.exec_():
            dir_name = dialog.selectedFiles()[0]
            dir_name = os.path.normpath(dir_name)  # UNIX \ even on Win
            logging.info("Chosen dir:" + dir_name)
            # Show selected folder on screen
            self.folderEdit.setText(dir_name)

    def validate_fields(self):
        if not self.folderEdit.text():
            msg_box = QMessageBox()
            msg_box.setText("Name the folder.")
            msg_box.exec_()
            return False

        if not self.langEdit.text():
            msg_box = QMessageBox()
            msg_box.setText("Name the language.")
            msg_box.exec_()
            return False

        if self.storage.language_exists(self.langEdit.text()):
            msg_box = QMessageBox()
            msg_box.setText("Language name already exists.")
            msg_box.exec_()
            return False

        if self.storage.folder_exists(self.folderEdit.text()):
            msg_box = QMessageBox()
            msg_box.setText("Folder name already taken.")
            msg_box.exec_()
            return False

        return True