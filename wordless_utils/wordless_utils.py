def fetch_files(self):
    files = [file for file in self.files if file.selected]

    if files == []:
        QMessageBox.warning(self,
                            self.tr('Generation Failed'),
                            self.tr('There are no files being currently selected!'),
                            QMessageBox.Ok)

    return files

def multiple_sorting(item):
    keys = []

    for freq in item[1]:
        keys.append(-freq)
    keys.append(item[0])

    return keys
