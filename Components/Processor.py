# coding: utf-8
import datetime
import numpy as np
import  json
import  os

from Components.Common import FileSystem
class DataProcessor():

    @staticmethod
    def ReviewApprovalIndicator(dataFrame, columnHeading):
        # type: (DataFrame, str) -> DataFrame

        dataFrame[columnHeading + ' indicator'] = dataFrame.apply(
            lambda row: _analyzeReviewApproval(
                row[columnHeading],
                row[columnHeading + ' Review/Approval']),
            axis=1)
        return  dataFrame

    @staticmethod
    def EngagementMonth(dataFrame):
        # type: (DataFrame) -> DataFrame
        dataFrame['Engagement Month'] = dataFrame.apply(
            lambda row: row['Start Date'].month,
            axis = 1
        )
    @staticmethod
    def EngagmentYear(dataFrame):
        # type: (DataFrame) -> DataFrame
        dataFrame['Engagement Year'] = dataFrame.apply(
            lambda  row: row['Start Date'].year,
            axis = 1
        )
    @staticmethod
    def RatingMapping(dataFrame):
        trans = FileSystem.Translation()
        dataFrame['3PRM Overall Risk Normalized'] = dataFrame.apply(
            lambda row: trans[row[u'3PRM Overall Risk']],
            axis = 1
        )
        dataFrame['New Assessment Filter Risk Normalized'] = dataFrame.apply(
            lambda row: trans[row[u'New Assessment Filter Risk']],
            axis = 1
        )

    @staticmethod
    def RegionMapping(dataFrame):
        # type: (DataFrame) -> DataFrame
        regions = Regions()
        dataFrame['Region'] = dataFrame.apply(
            lambda row: regions.GetRegions(row[u'Country']),
            axis = 1
        )

    @staticmethod
    def SubRegionMapping(dataFrame):
        subRegions = SubRegions()
        dataFrame['SubRegion'] = dataFrame.apply(
            lambda row: subRegions.GetSubRegions(row[u'Country']),
            axis=1
        )
    @staticmethod
    def SetAreaMapping(dataFrame):
        JSON = FileSystem.GetDictionary('SetAreas')
        dataFrame['Set Area'] = dataFrame.apply(
            lambda  row: JSON[row['Operating Unit']],
            axis = 1
        )
    @staticmethod
    def SeperateCategoryAndSubCategory(dataFrame):
        dataFrame['Procurement Category'] = dataFrame.apply(
            lambda row : unicode(row['Activity / Detail Activity']).split(', ')[0] ,
            axis=1
        )
        dataFrame['Procurement SubCategory'] = dataFrame.apply(
            lambda row : unicode(row['Activity / Detail Activity']).split(', ')[1] ,
            axis=1
        )
    @staticmethod
    def RatingOccurences(dataFrame):
        headerList = list(dataFrame)
        dataFrame['Underrated Count'] = dataFrame.apply(
            lambda  row: _countRatings(row, headerList, 'Underrated'),
            axis = 1
        )
        dataFrame['Overrated Count'] = dataFrame.apply(
            lambda  row: _countRatings(row, headerList, 'Overrated'),
            axis = 1
        )
        dataFrame['Properly rated Count'] = dataFrame.apply(
            lambda  row: _countRatings(row, headerList, 'Properly rated'),
            axis = 1
        )


    @staticmethod
    def ReviewApprovalTime(dataFrame):
        dataFrame['Due Dilligence Approval Time'] = dataFrame.apply(
            lambda row: _dateDifferenceInDays(
                row[u'Start Date'],
                row[u'Due Diligence Review/Approval Status Date']
            ),
            axis = 1
        )
        dataFrame['Risk Assessment Approval Time'] = dataFrame.apply(
            lambda row: _dateDifferenceInDays(
                row[u'Start Date'],
                row[u'Risk Assessment Review/Approval Status Date']
            ),
            axis = 1
        )
def _countRatings(row, headerList, rating):
    # type: (obj, list, str) -> int
    count = 0
    for header in headerList:
        if 'indicator' in header:
            if row[unicode(header)] == rating:
                count = count+1
    return  count

def _dateDifferenceInDays(startDate, endDate):
    try:
        endDate = datetime.datetime.strptime(endDate, "%m/%d/%Y")
        return abs((endDate - startDate).days)
    except:
        return None

def _analyzeReviewApproval(originalValue, validatedValue):
    # type: (str, str) -> str

    translation = FileSystem.NumericTranslation()
    # validatedValue = unicode(validatedValue).encode('utf-8')
    # originalValue = unicode(originalValue).encode('utf-8')
    if translation[validatedValue] > translation[originalValue]:
        return 'Underrated'
    elif translation[validatedValue] < translation[originalValue]:
        return 'Overrated'
    else:
        if translation[validatedValue] + translation[originalValue] == 0:
            return None
        else:
            return  'Properly rated'



class Regions():
    # ToDo Regions as Singleton
    def __init__(self):
        self.JSON = FileSystem.GetDictionary('Regions')

    def GetRegions(self,input):
        # type: (str) -> str
        regionList = []
        placesList = input.split(', ')
        for place in placesList:
            if self._mapRegion(place) == 'Global':
                return 'Global'
            regionList.append(self._mapRegion(place))
        regionList = list(set(regionList))
        if len(regionList) == 1:
            return regionList[0]
        elif len(regionList) >= 4:
            return 'Global'
        else:
            return 'MultiRegion'

    def _mapRegion(self, input):
        # type: (str) -> str
        return self.JSON[input]


class SubRegions():
    # ToDo Regions as Singleton
    def __init__(self):
        self.JSON = FileSystem.GetDictionary('SubRegions')

    def GetSubRegions(self,input):
        # type: (str) -> str
        regionList = []
        placesList = input.split(', ')
        for place in placesList:
            if self._mapSubRegion(place) == 'Global':
                return 'Global'
            regionList.append(self._mapSubRegion(place))
        regionList = list(set(regionList))
        if len(regionList) == 1:
            return regionList[0]
        elif len(regionList) > 15:
            return 'Global'
        else:
            return 'MultiRegion'

    def _mapSubRegion(self, input):
        # type: (str) -> str
        return self.JSON[input]


