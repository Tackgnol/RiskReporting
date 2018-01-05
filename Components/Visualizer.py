
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import cartopy.crs as ccrs
import numpy as np
import cartopy.io.shapereader as shapereader
from matplotlib.colors import ListedColormap
from numpy import count_nonzero, sum
from scipy import stats

from Components.Common import FileSystem


class Visualizer():
    def __init__(self, dataFrame):
        # type: (dataFrame) -> None
        self._dataFrame = dataFrame # type: DataFrame
    def GenerateMultiValueHeatMap(self, y, valueList, colorSet):
        # type: (str, str, str, list, str) -> None

        _dataSet = self._2DDataFrameFromValues(y, valueList)
        AZPallete = ListedColormap(
            sns.color_palette(
                colorSet
            ).as_hex())

        sns.heatmap(
            _dataSet,
            cmap=AZPallete,
            annot=True,
            fmt='d',
            linewidths=.5
        )
        plt.yticks(rotation=0, fontsize=6)
        plt.savefig('./Exports/Heatmaps/' + 'Global - ' + y + '.png', dpi=400, bbox_inches='tight')
        plt.clf()

    def GenerateMap(self, showBy, sumBy, colorSet):
        # type: (str, str, list) -> None
        _dataSet = self._oneColPivot(showBy, sumBy, sumBy) # type: DataFrame
        regionList = self._generateRegionList(_dataSet)
        regionsDict = FileSystem.GetDictionary('mapCountries')
        countriesMap = self._getListOfCountries()
        colors = np.array(colorSet)

        regionColorDict = {}
        legendHandles = []

        for i in range(0,6):
            regionColorDict[regionList[i][0]] = colors[i]
            regionLabel = str(regionList[i][0]) + ' - ' + str(regionList[i][1])
            newRegion = mpatches.Patch(color=colors[i], label=regionLabel)
            legendHandles.append(newRegion)

        ax = plt.axes(projection=ccrs.PlateCarree())
        for country in shapereader.Reader(countriesMap).records():
            try:
                selectedColor = regionColorDict[regionsDict[country.attributes['NAME_LONG']]]
            except:
                selectedColor = '#ffffff'

            ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                          facecolor=selectedColor)

        plt.legend(handles=legendHandles, loc='center left', bbox_to_anchor=(1, 0.5))
        plt.title(sumBy)
        plt.savefig('./Exports/Maps/' + showBy + ' - ' + sumBy + '.png', dpi=400, bbox_inches='tight')
        plt.clf()

    def GenerateHeatMap(self, x,y, values, colorSet, operation):
        # type: (str, str, str, list, str) -> None
        if operation == 'count':
            dataSet = self._pivotDataCount(y, x, values)
        else:
            dataSet = self._pivotDataSum(y,x,values)

        AZPallete = ListedColormap(
            sns.color_palette(
                colorSet
            ).as_hex())

        sns.heatmap(
            dataSet,
            cmap=AZPallete,
            annot=True,
            fmt='d',
            linewidths=.5
        )
        plt.yticks(rotation=0, fontsize = 6)
        plt.savefig('./Exports/Heatmaps/'+ x + ' - ' + y + '.png', dpi=400, bbox_inches='tight')
        plt.clf()

    def GenerateDistribution(self, field):
        _dataSet = self._dataFrame[field].dropna()
        sns.distplot(_dataSet, kde=False, fit=stats.gamma)
        plt.title('Distribution of' + field)
        plt.savefig('./Exports/Distributions/Distribution of '+ field +'.png', dpi=400, bbox_inches='tight')
        plt.clf()

    def GenerateBarChart(self,field, hue):
        sns.countplot(x=field,  hue=hue, data=self._dataFrame, )
        plt.title(field)
        plt.xticks(rotation=45, fontsize=6)
        plt.savefig('./Exports/Barcharts/' + field + ' - ' + hue  + '.png', dpi=400, bbox_inches='tight')
        plt.clf()


    def _pivotDataCount(self, rows, columns, count):
        # type: (str, str, str) -> DataFrame
        return self._dataFrame.pivot_table(count, rows, columns, count_nonzero, 0)


    def _pivotDataSum(self, rows, columns, sumBy):
        # type: (str, str, str) -> DataFrame
        return self._dataFrame.pivot_table(sumBy, rows, columns, sum, 0)

    def _oneColPivot(self, rows, values, sortBy = None):
        # type: (str, str) -> DataFrame
        _dataSet = self._dataFrame.pivot_table(index=[rows], values=[values], aggfunc = sum)
        if sortBy:
            _dataSet = _dataSet.sort_values(by=[sortBy], ascending=False)
        return _dataSet

    def _generateRegionList(self, dataSet):
        regionList = []
        for index, row in dataSet.iterrows():
            regionList.append((index, row.values[0]))

        return regionList

    def _getListOfCountries(self):
        mapName = 'admin_0_countries'
        return shapereader.natural_earth(resolution='110m',
                                         category='cultural',
                                         name=mapName)
    def _2DDataFrameFromValues(self,row, values):
        # type: (str, list) -> DataFrame
        frame = self._dataFrame.pivot_table(values, row, aggfunc = sum)
        return frame



