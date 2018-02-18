# Copyright (C) 2011 Chris Dekter
# Copyright (C) 2018 Thomas Hess <thomas.hess@udo.edu>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from PyQt4 import uic
from PyQt4 import QtCore, Qt
from PyQt4.QtGui import QListWidgetItem


from .common import get_ui_qfile, EMPTY_FIELD_REGEX

ui_file = get_ui_qfile("abbrsettings")
AbbrSettingsBase = uic.loadUiType(ui_file)
ui_file.close()


WORD_CHAR_OPTIONS_ORDERED = ["All non-word", "Space and Enter", "Tab"]

class AbbrListItem(QListWidgetItem):

    def __init__(self, text):
        QListWidgetItem.__init__(self, text)
        self.setFlags(self.flags() | Qt.ItemFlags(Qt.ItemIsEditable))

    def setData(self, role, value):
        if value == "":
            self.listWidget().itemChanged.emit(self)
        else:
            QListWidgetItem.setData(self, role, value)


class AbbrSettings(*AbbrSettingsBase):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi()
        for item in WORD_CHAR_OPTIONS_ORDERED:
            self.wordCharCombo.addItem(item)

    def setupUi(self):
        self.setObjectName("Form")
        super().setupUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def on_addButton_pressed(self):
        item = AbbrListItem("")
        self.abbrListWidget.addItem(item)
        self.abbrListWidget.editItem(item)
        self.removeButton.setEnabled(True)

    def on_removeButton_pressed(self):
        item = self.abbrListWidget.takeItem(self.abbrListWidget.currentRow())
        if self.abbrListWidget.count() == 0:
            self.removeButton.setEnabled(False)

    def on_abbrListWidget_itemChanged(self, item):
        if EMPTY_FIELD_REGEX.match(item.text()):
            row = self.abbrListWidget.row(item)
            self.abbrListWidget.takeItem(row)
            del item

        if self.abbrListWidget.count() == 0:
            self.removeButton.setEnabled(False)

    def on_abbrListWidget_itemDoubleClicked(self, item):
        self.abbrListWidget.editItem(item)

    def on_ignoreCaseCheckbox_stateChanged(self, state):
        if not self.ignoreCaseCheckbox.isChecked():
            self.matchCaseCheckbox.setChecked(False)

    def on_matchCaseCheckbox_stateChanged(self, state):
        if self.matchCaseCheckbox.isChecked():
            self.ignoreCaseCheckbox.setChecked(True)

    def on_immediateCheckbox_stateChanged(self, state):
        if self.immediateCheckbox.isChecked():
            self.omitTriggerCheckbox.setChecked(False)
            self.omitTriggerCheckbox.setEnabled(False)
            self.wordCharCombo.setEnabled(False)
        else:
            self.omitTriggerCheckbox.setEnabled(True)
            self.wordCharCombo.setEnabled(True)
