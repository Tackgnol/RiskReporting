import pandas as pd


class GetData():
    excelFormats = ('.xlsx', '.xls', '.xlsm') # type: tuple
    csvFormats = ('.csv', '.txt') # type: tuple
    def __init__(self, directory, separator=None):
        # type: (str, str) -> None
        self._directory = directory

        if self._directory.lower().endswith(self.excelFormats):
            self._dataFame = pd.read_excel(self._directory)
        elif self._directory.lower().endswith(self.csvFormats):
            if separator is None:
                raise ValueError('CSV/Text file provided but no separator given')
            self._dataFame = pd.read_csv(self._directory, delimiter=separator)
        else:
            raise TypeError('Unrecognized file type, please use ' + self._acceptableFormats() + ' files')

    def _acceptableFormats(self):
        # type: () -> str
        extensionList = list(self.excelFormats)
        extensionList.extend(list(self.csvFormats))
        return  str(extensionList).strip('[').strip(']')


    @property
    def Data(self):
        # type: () -> DataFrame
        return self._dataFame
    @property
    def SetData(self,dataFrame):
        # type: (DataFrame) -> None
        self._dataFame = dataFrame



