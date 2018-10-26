#
# Wordless: Semantics
#
# Copyright (C) 2018 Ye Lei (叶磊) <blkserene@gmail.com>
#
# License Information: https://github.com/BLKSerene/Wordless/blob/master/LICENSE.txt
#

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot
import networkx
import nltk

from wordless_widgets import *
from wordless_utils import *

def init(self):
    def search_settings_changed():
        self.settings_custom['semantics']['search_term'] = line_edit_search_term.text()
        self.settings_custom['semantics']['search_mode'] = combo_box_search_mode.currentText()
        self.settings_custom['semantics']['search_for'] = combo_box_search_for.currentText()

        if self.settings_custom['semantics']['search_for'] in ['Synonyms', 'Antonyms']:
            checkbox_recursive.setEnabled(False)
            spin_box_depth_max.setEnabled(False)
            checkbox_depth.setEnabled(False)
            checkbox_show_lemmas.setEnabled(False)
        else:
            checkbox_recursive.setEnabled(True)
            spin_box_depth_max.setEnabled(True)
            checkbox_depth.setEnabled(True)
            checkbox_show_lemmas.setEnabled(True)

        table_semantics.setHorizontalHeaderItem(2, QTableWidgetItem(self.settings_custom['semantics']['search_for']))

        plot_settings_changed()

    def plot_settings_changed():
        self.settings_custom['semantics']['degree_max'] = spin_box_degree_max.value()
        self.settings_custom['semantics']['degree_no_limit'] = checkbox_degree.isChecked()
        self.settings_custom['semantics']['recursive'] = checkbox_recursive.isChecked()
        self.settings_custom['semantics']['depth_max'] = spin_box_depth_max.value()
        self.settings_custom['semantics']['depth_no_limit'] = checkbox_depth.isChecked()
        self.settings_custom['semantics']['show_lemmas'] = checkbox_show_lemmas.isChecked()

        if self.settings_custom['semantics']['degree_no_limit']:
            spin_box_degree_max.setEnabled(False)
        else:
            spin_box_degree_max.setEnabled(True)

        if self.settings_custom['semantics']['search_for'] not in ['Synonyms', 'Antonyms']:
            if self.settings_custom['semantics']['recursive']:
                spin_box_depth_max.setEnabled(True)
                checkbox_depth.setEnabled(True)
                checkbox_show_lemmas.setEnabled(True)

                if self.settings_custom['semantics']['depth_no_limit']:
                    spin_box_depth_max.setEnabled(False)
                else:
                    spin_box_depth_max.setEnabled(True)
            else:
                spin_box_depth_max.setEnabled(False)
                checkbox_depth.setEnabled(False)
                checkbox_show_lemmas.setEnabled(False)

    def restore_defaults():
        line_edit_search_term.setText(self.settings_default['semantics']['search_term'])
        combo_box_search_mode.setCurrentText(self.settings_default['semantics']['search_mode'])
        combo_box_search_for.setCurrentText(self.settings_default['semantics']['search_for'])

        spin_box_degree_max.setValue(self.settings_default['semantics']['degree_max'])
        checkbox_degree.setChecked(self.settings_default['semantics']['degree_no_limit'])
        spin_box_depth_max.setValue(self.settings_default['semantics']['depth_max'])
        checkbox_depth.setChecked(self.settings_default['semantics']['depth_no_limit'])
        checkbox_recursive.setChecked(self.settings_default['semantics']['recursive'])
        checkbox_show_lemmas.setChecked(self.settings_default['semantics']['show_lemmas'])

        search_settings_changed()

    tab_semantics = wordless_layout.Wordless_Tab(self, self.tr('Semantics'))

    table_semantics = wordless_table.Wordless_Table_Data(self,
                                                         headers = [
                                                             self.tr('Synsets'),
                                                             self.tr('Part of Speech'),
                                                             '',
                                                             self.tr('Definition'),
                                                             self.tr('Examples')
                                                         ],
                                                         cols_stretch = ['Examples'])

    table_semantics.button_search = QPushButton('Begin Search', self)
    table_semantics.button_generate_plot = QPushButton('Generate Plot', self)

    table_semantics.button_search.clicked.connect(lambda: search(self, table_semantics))
    table_semantics.button_generate_plot.clicked.connect(lambda: generate_plot(self))

    tab_semantics.layout_table.addWidget(table_semantics, 0, 0, 1, 5)
    tab_semantics.layout_table.addWidget(table_semantics.button_search, 1, 0)
    tab_semantics.layout_table.addWidget(table_semantics.button_generate_plot, 1, 1)
    tab_semantics.layout_table.addWidget(table_semantics.button_export_selected, 1, 2)
    tab_semantics.layout_table.addWidget(table_semantics.button_export_all, 1, 3)
    tab_semantics.layout_table.addWidget(table_semantics.button_clear, 1, 4)

    # Search Settings
    groupbox_search_settings = QGroupBox('Search Settings', self)

    label_search_term = QLabel('Search Term:', self)
    line_edit_search_term = QLineEdit(self)
    label_search_mode = QLabel('Search Mode:', self)
    combo_box_search_mode = QComboBox(self)
    label_search_for = QLabel('Search For:', self)
    combo_box_search_for = QComboBox(self)

    combo_box_search_mode.addItems([
                                      self.tr('Word'),
                                      self.tr('Lemma'),
                                      self.tr('Synset')
                                  ])
    combo_box_search_for.addItems([
                                     self.tr('Synonyms'),
                                     self.tr('Antonyms'),
                                     self.tr('Hypernyms'),
                                     self.tr('Hyponyms'),
                                     self.tr('Member Holonyms'),
                                     self.tr('Member Meronyms'),
                                     self.tr('Part Holonyms'),
                                     self.tr('Part Meronyms'),
                                     self.tr('Substance Holonyms'),
                                     self.tr('Substance Meronyms'),
                                     self.tr('Entailments')
                                  ])

    line_edit_search_term.textChanged.connect(search_settings_changed)
    line_edit_search_term.returnPressed.connect(table_semantics.button_search.click)
    combo_box_search_mode.currentTextChanged.connect(search_settings_changed)
    combo_box_search_for.currentTextChanged.connect(search_settings_changed)

    layout_search_settings = QGridLayout()
    layout_search_settings.addWidget(label_search_term, 0, 0)
    layout_search_settings.addWidget(line_edit_search_term, 1, 0)
    layout_search_settings.addWidget(label_search_mode, 2, 0)
    layout_search_settings.addWidget(combo_box_search_mode, 3, 0)
    layout_search_settings.addWidget(label_search_for, 4, 0)
    layout_search_settings.addWidget(combo_box_search_for, 5, 0)
    
    groupbox_search_settings.setLayout(layout_search_settings)

    # Plot Settings
    groupbox_plot_settings = QGroupBox('Plot Settings', self)

    label_degree_max = QLabel('Maximum Degree:', self)
    spin_box_degree_max = QSpinBox(self)
    checkbox_degree  = QCheckBox('No Limit', self)
    label_depth_max = QLabel('Maximum Depth:', self)
    spin_box_depth_max = QSpinBox(self)
    checkbox_depth = QCheckBox('No Limit', self)
    checkbox_recursive = QCheckBox('Recursive', self)
    checkbox_show_lemmas = QCheckBox('Show All Lemmas', self)

    spin_box_degree_max.valueChanged.connect(plot_settings_changed)
    checkbox_degree.stateChanged.connect(plot_settings_changed)
    spin_box_depth_max.valueChanged.connect(plot_settings_changed)
    checkbox_depth.stateChanged.connect(plot_settings_changed)
    checkbox_recursive.stateChanged.connect(plot_settings_changed)
    checkbox_show_lemmas.stateChanged.connect(plot_settings_changed)

    layout_plot_settings = QGridLayout()
    layout_plot_settings.addWidget(label_degree_max, 0, 0, 1, 2)
    layout_plot_settings.addWidget(spin_box_degree_max, 1, 0)
    layout_plot_settings.addWidget(checkbox_degree, 1, 1)
    layout_plot_settings.addWidget(label_depth_max, 2, 0, 1, 2)
    layout_plot_settings.addWidget(spin_box_depth_max, 3, 0)
    layout_plot_settings.addWidget(checkbox_depth, 3, 1)
    layout_plot_settings.addWidget(checkbox_recursive, 4, 0, 1, 2)
    layout_plot_settings.addWidget(checkbox_show_lemmas, 5, 0, 1, 2)

    groupbox_plot_settings.setLayout(layout_plot_settings)

    tab_semantics.layout_settings.addWidget(groupbox_search_settings, 0, 0, Qt.AlignTop)
    tab_semantics.layout_settings.addWidget(groupbox_plot_settings, 1, 0, Qt.AlignTop)
    
    restore_defaults()

    return tab_semantics

def search(self, table):
    def append_search_result(row, synset):
        examples = synset.examples()

        if len(examples) == 1:
            synset_examples = [examples]
        else:
            synset_examples = []

            for i, example in enumerate(examples):
                synset_examples.append('({}) {}'.format(i + 1, example))

        table.setRowCount(table.rowCount() + 1)

        table.setItem(row, 0, QTableWidgetItem(synset.name()))
        table.setItem(row, 1, QTableWidgetItem(self.settings_custom['semantics']['parts_of_speech'][synset.pos()]))
        table.setItem(row, 2, QTableWidgetItem(', '.join(synset.lemma_names())))
        table.setItem(row, 3, QTableWidgetItem(synset.definition()))
        table.setItem(row, 4, QTableWidgetItem(' '.join(examples)))

    if self.settings_custom['semantics']['search_term']:
        table.clear_table()
        table.setRowCount(0)

        i = 0
        for synset in nltk.corpus.wordnet.synsets(self.settings_custom['semantics']['search_term']):
            if self.settings_custom['semantics']['search_for'] == 'Synonyms':
                append_search_result(i, synset)

                i += 1
            elif self.settings_custom['semantics']['search_for'] == 'Antonyms':
                for lemma in synset.antonyms():
                    for antonym in lemma.antonyms():
                        append_search_result(i, antonym.synset())

                        i += 1
            elif self.settings_custom['semantics']['search_for'] == 'Hypernyms':
                for hypernym in synset.hypernyms():
                    append_search_result(i, hypernym)

                    i += 1
            elif self.settings_custom['semantics']['search_for'] == 'Hyponyms':
                for hyponym in synset.hyponyms():
                    append_search_result(i, hyponym)

                    i += 1
            elif self.settings_custom['semantics']['search_for'] == 'Member Holonyms':
                for member_holonym in synset.member_holonyms():
                    append_search_result(i, member_holonym)

                    i += 1
            elif self.settings_custom['semantics']['search_for'] == 'Member Meronyms':
                for member_meronym in synset.member_holonyms():
                    append_search_result(i, member_meronym)

                    i += 1
            elif self.settings_custom['semantics']['search_for'] == 'Part Holonyms':
                for part_holonym in synset.part_holonyms():
                    append_search_result(i, part_holonym)

                    i += 1
            elif self.settings_custom['semantics']['search_for'] == 'Part Meronyms':
                for part_meronym in synset.part_holonyms():
                    append_search_result(i, part_meronym)

                    i += 1
            elif self.settings_custom['semantics']['search_for'] == 'Substance Holonyms':
                for substance_holonym in synset.substance_holonyms():
                    append_search_result(i, substance_holonym)

                    i += 1
            elif self.settings_custom['semantics']['search_for'] == 'Substance Meronyms':
                for substance_meronym in synset.substance_holonyms():
                    append_search_result(i, substance_meronym)

                    i += 1
            elif self.settings_custom['semantics']['search_for'] == 'Entailments':
                for entailment in synset.entailments():
                    append_search_result(i, entailment)

                    i += 1

        if table.rowCount() == 0:
            table.setRowCount(1)

            QMessageBox.information(self,
                                    self.tr('No Search Results'),
                                    self.tr('There are no results for your search!'),
                                    QMessageBox.Ok)
    else:
        QMessageBox.warning(self,
                            self.tr('Search Failed'),
                            self.tr('Please enter your search item first!'),
                            QMessageBox.Ok)

    self.status_bar.showMessage('Done!')

def generate_plot(self):
    def search(graph, search_item):
        if self.settings_custom['semantics']['search_for'] == 'Antonyms':
            graph_depth = graph.depth[search_item.synset().name()]
        else:
            graph_depth = graph.depth[search_item.name()]

        if self.settings_custom['semantics']['search_for'] == 'Synonyms':
            root = self.settings_custom['semantics']['search_term']

            for synonym in search_item.lemma_names():
                if synonym != root:
                    graph.add_edge(search_item.name(), synonym)
                    graph.depth[synonym] = graph_depth + 1
        elif self.settings_custom['semantics']['search_for'] == 'Antonyms':
            for antonym in search_item.antonyms():
                graph.add_edge(search_item.name(), antonym.name())
                graph.depth[antonym.name()] = graph_depth + 1
        else:
            if self.settings_custom['semantics']['search_for'] == 'Hypernyms':
                synsets = search_item.hypernyms()
            elif self.settings_custom['semantics']['search_for'] == 'Hyponyms':
                synsets = search_item.hyponyms()
            elif self.settings_custom['semantics']['search_for'] == 'Member Holonyms':
                synsets = search_item.member_holonyms()
            elif self.settings_custom['semantics']['search_for'] == 'Member Meronyms':
                synsets = search_item.member_meronyms()
            elif self.settings_custom['semantics']['search_for'] == 'Part Holonyms':
                synsets = search_item.part_holonyms()
            elif self.settings_custom['semantics']['search_for'] == 'Part Meronyms':
                synsets = search_item.part_meronyms()
            elif self.settings_custom['semantics']['search_for'] == 'Substance Holonyms':
                synsets = search_item.substance_holonyms()
            elif self.settings_custom['semantics']['search_for'] == 'Substance Meronyms':
                synsets = search_item.substance_meronyms()
            elif self.settings_custom['semantics']['search_for'] == 'Entailments':
                synsets = search_item.entailments()

            for i, synset in enumerate(synsets):
                if self.settings_custom['semantics']['depth_no_limit'] or i < self.settings_custom['semantics']['depth_max']:
                    graph.add_edge(search_item.name(), synset.name())
                    graph.depth[synset.name()] = graph_depth + 1

                    if self.settings_custom['semantics']['show_lemmas']:
                        for j, lemma in enumerate(synset.lemma_names()):
                            if self.settings_custom['semantics']['depth_no_limit'] or j < self.settings_custom['semantics']['depth_max']:
                                graph.add_edge(synset.name(), lemma)
                                graph.depth[lemma] = graph_depth + 2

                    if (self.settings_custom['semantics']['recursive'] and self.settings_custom['semantics']['depth_no_limit'] or
                        self.settings_custom['semantics']['recursive'] and graph_depth <= self.settings_custom['semantics']['depth_max']):
                        search(graph, synset)

        return graph

    if self.settings_custom['semantics']['search_term']:
        graph = networkx.Graph()
        graph.depth = {'Root: ' + self.settings_custom['semantics']['search_term']: 0}
        
        lemmas = nltk.corpus.wordnet.lemmas(self.settings_custom['semantics']['search_term'])
        for lemma in lemmas:
            graph.add_edge('Root: ' + self.settings_custom['semantics']['search_term'], lemma.synset().name())
            graph.depth[lemma.synset().name()] = 1

            if self.settings_custom['semantics']['search_for'] == 'Antonyms':
                graph = search(graph, lemma)
            else:
                graph = search(graph, lemma.synset())

        if len(graph) > len(lemmas) + 1:
            networkx.draw(graph,
                          node_size = [32 * (max(graph.depth.values()) - graph.depth[node] + 1) for node in graph],
                          node_color = [graph.depth[node] for node in graph],
                          cmap = matplotlib.pyplot.cm.Set3,
                          edge_color = '#B3B3B3',
                          font_size = '11',
                          font_family = 'Arial',
                          with_labels = True)
            matplotlib.pyplot.show()
        else:
            QMessageBox.information(self,
                                    self.tr('No Search Results'),
                                    self.tr('There are no results for your search!'),
                                    QMessageBox.Ok)
    else:
        QMessageBox.warning(self,
                            self.tr('Generation Failed'),
                            self.tr('Please enter your search item first!'),
                            QMessageBox.Ok)

    self.status_bar.showMessage('Done!')
