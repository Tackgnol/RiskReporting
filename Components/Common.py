# coding: utf-8
from collections import OrderedDict
from os.path import isfile, dirname, join
import json
import xlrd
import numpy as np
class AZColors():
    @staticmethod
    def AZColorScheme():
        # type:() -> list[str]
        listColors = [
            '#830051',
            '#c4d600',
            '#003865',
            '#3f4444',
            '#68d2df',
            '#d0006f',
            '#3c1053',
            '#f0ab00',
            '#9db0ac'
        ]
        return listColors # type: list[str]
    @staticmethod
    def MonochromaticViolet():
        # type : () -> list[str]
        listColors = [
            '#5f0039',
            '#6f0044',
            '#7d004d',
            '#965974',
            '#b495a1',
            '#cdbcc2',
            '#bcbfc6'
        ]
        return  listColors


class FileSystem():
    @staticmethod
    def OpenOrCreateFile(directory):
        # type: (str) -> File
        if isfile(directory):
            return open(directory, 'r')
        else:
            return open(directory, 'w')
    @staticmethod
    def GetDictFromExcel(directory, name):
        # type: (str, str) -> Dictionary
        try:
            sh = _openAndReturnFirstSheet(directory)
        except:
            return {}

        items = {sh.row_values(rownum)[0] : sh.row_values(rownum)[1] for rownum in range(1, sh.nrows)}

        jsonResult = json.dumps(items, encoding='utf-8')
        savePath = join(dirname(__file__), '../Resources/Dictionaries/JSON/' + name + '.json')
        _writeJSON(savePath, jsonResult)

        return savePath
    @staticmethod
    def GetDictionary(lookingFor):
        # type: (str) -> dict
        filePath = join(dirname(__file__), '../Resources/Dictionaries/')
        source = FileSystem.OpenOrCreateFile(filePath + 'JSON/'+ lookingFor +'.json')  # type: File
        try:
            regionDictionary = json.load(source)  # type : {}
        except:
            regionDictionary = FileSystem.GetDictFromExcel(filePath + 'Excel/' + lookingFor + '.xlsx', lookingFor)

        return regionDictionary
    @staticmethod
    def NumericTranslation():
        ratings = {
            u'Low': 1,
            u'High': 2,
            u'NA': 0,
            u'Alto': 2,
            u'Bajo': 1,
            u'低': 1,
            u'高': 2,
            u'N/D':0,
            'nan': 0,
            None: 0,
            '': 0,
            np.nan: 0,
        }
        return  ratings

    @staticmethod
    def Translation():
        ratings = {
            u'Low': u'Low',
            u'High': u'High',
            u'NA': '',
            u'Alto': u'High',
            u'Bajo': u'Low',
            u'低': u'Low',
            u'高': u'High',
            u'N/D': '',
            'nan': '',
            None: '',
            '': '',
            np.nan: '',
        }
        return ratings
def _openAndReturnFirstSheet(directory):
    if isfile(directory):
        wb = xlrd.open_workbook(directory)
        sh = wb.sheet_by_index(0)
        return sh
    else:
        raise IOError

def _writeJSON(directory, input):
    with open(directory, 'w') as f:
        f.write(input)