# -*- coding: utf-8 -*-
import os
import logging

from ui.langManager import Ui_languagesDialog
import config
from baseTableModel import BaseTaBleModel

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAbstractItemView, QDialog, QFileDialog,\
    QMessageBox, QHeaderView


class LangManager(Ui_languagesDialog, QDialog):

    langListHasChanged = pyqtSignal()

    def __init__(self, storage):
        super(LangManager, self).__init__()
        self.setupUi(self)

        self.storage = storage

        self.langs_model = BaseTaBleModel(["Language", "Folder"])
        self.languagesTable.setModel(self.langs_model)
        self.languagesTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.languagesTable.horizontalHeader()\
            .setSectionResizeMode(1, QHeaderView.Stretch)

        # Connect signals and slots
        self.removeButton.clicked.connect(self.remove_button_clicked)
        self.addButton.clicked.connect(self.add_button_clicked)
        self.folderButton.clicked.connect(self.folder_button_clicked)

        # Load languages as initial state
        self.initialize()

    def initialize(self):
        """
        Draws the existing languages into table.
        :return:
        """
        languages = self.storage.get_languages()
        for row in languages:
            self.langs_model.add_row(*row)

    def remove_button_clicked(self):
        """
        Removes the language from DB and from lang table.
        :return:
        """
        # Drop the language from DB
        index = self.languagesTable.selectedIndexes()
        if index:
            row = index[0].row()
            current_lang = self.langs_model.index(row, 0).data()
            self.storage.remove_language(current_lang)

            self.langs_model.removeRows(row, 1)

            self.langListHasChanged.emit()

    def add_button_clicked(self):
        """
        After validation adds new language to DB and table. Creates subfolder
        inside new language folder.
        :return:
        """
        lang = self.langEdit.text()
        folder = self.folderEdit.text()
        logging.info("Going to add new lang folder:" + folder)
        if self.validate_fields():
            # Add new lang to DB, and redraw the list of languages.
            self.storage.add_language(lang, folder)

            self.langs_model.add_row(lang, folder)

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
        """
        Runs standard select Folder dialog.
        :return:
        """
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
        """
        Validates fields for ne language.
        :return:
        """
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