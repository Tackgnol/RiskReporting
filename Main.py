from Components.Processor import DataProcessor
from Components.GetData import GetData
from Tkinter import Tk
from tkFileDialog import askopenfilename
from Components.Common import AZColors
from Components.Visualizer import Visualizer
from datetime import datetime
from Components.PowerPoint import PowerPoint
startTime = datetime.now()

def RunHeatmaps(xList, yList, count, colorScheme):
    for x in xList:
        for y in yList:
            visualizations.GenerateHeatMap(y+ ' indicator',x,count,colorScheme, 'count')


Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
fileDirectory = askopenfilename()

try:
    dataSouce = GetData(fileDirectory,';')
except ValueError as e:
    print(e)

except TypeError as e:
    print(e)


azColorScheme =  AZColors.AZColorScheme()
yList = [
    'Due Diligence ABAC',
    'Due Diligence Confidentiality',
    'Due Diligence Conflict of Interest',
    'Due Diligence Data Privacy',
    'Due Diligence Employment Principles',
    'Due Diligence Fair Trade and Competition',
    'Due Diligence Governance',
    'Due Diligence Product Communication',
    'Due Diligence Product Security',
    'Due Diligence R&D',
    'Due Diligence SHE',
    'Risk Assessment ABAC',
    'Risk Assessment Confidentiality',
    'Risk Assessment Conflict of Interest',
    'Risk Assessment Data Privacy',
    'Risk Assessment Employment Principles',
    'Risk Assessment Fair Trade and Competition',
    'Risk Assessment Governance',
    'Risk Assessment Product Communication',
    'Risk Assessment Product Security',
    'Risk Assessment R&D',
    'Risk Assessment SHE',
]

xList = [
    'Region',
    'Cluster',
    'Engagement Month',
    'Set Area'
]

DataProcessor.RegionMapping(dataSouce.Data)
DataProcessor.SubRegionMapping(dataSouce.Data)
for field in yList:
    DataProcessor.ReviewApprovalIndicator(dataSouce.Data, unicode(field))
DataProcessor.EngagementMonth(dataSouce.Data)
DataProcessor.EngagmentYear(dataSouce.Data)
DataProcessor.RatingOccurences(dataSouce.Data)
DataProcessor.ReviewApprovalTime(dataSouce.Data)
DataProcessor.SeperateCategoryAndSubCategory(dataSouce.Data)
DataProcessor.SetAreaMapping(dataSouce.Data)
DataProcessor.RatingMapping(dataSouce.Data)

visualizations = Visualizer(dataSouce.Data)
visualizations.GenerateMap(u'Region', u'Overrated Count', azColorScheme)
visualizations.GenerateMap(u'Region', u'Underrated Count', azColorScheme)
visualizations.GenerateMap(u'Region', u'Properly rated Count', azColorScheme)
visualizations.GenerateDistribution(u'Risk Assessment Approval Time')
visualizations.GenerateDistribution(u'Due Dilligence Approval Time')
visualizations.GenerateMultiValueHeatMap(u'Region', [u'Overrated Count',u'Properly rated Count' ,u'Underrated Count'], azColorScheme)
visualizations.GenerateMultiValueHeatMap(u'Cluster', [u'Overrated Count',u'Properly rated Count' ,u'Underrated Count'], azColorScheme)
visualizations.GenerateMultiValueHeatMap(u'Engagement Month', [u'Overrated Count',u'Properly rated Count' ,u'Underrated Count'], azColorScheme)
visualizations.GenerateMultiValueHeatMap(u'Set Area', [u'Overrated Count',u'Properly rated Count' ,u'Underrated Count'], azColorScheme)
visualizations.GenerateBarChart(u'Engagement Month', u'3PRM Overall Risk Normalized')
visualizations.GenerateBarChart(u'Engagement Month', u'New Assessment Filter Risk Normalized')
visualizations.GenerateBarChart(u'Region', u'3PRM Overall Risk Normalized')
visualizations.GenerateBarChart(u'Region', u'New Assessment Filter Risk Normalized')
visualizations.GenerateBarChart(u'Region', u'Third Party Language')
visualizations.GenerateBarChart(u'Set Area', u'Third Party Language')
visualizations.GenerateBarChart(u'Set Area', u'3PRM Overall Risk Normalized')
visualizations.GenerateBarChart(u'Set Area', u'New Assessment Filter Risk Normalized')

RunHeatmaps(xList, yList, u'AZ Engagement Name', azColorScheme)

dataSouce.Data.to_excel('C:\Users\ktlj659\Documents\Python\\3PRM\Exports\Excels\export.xlsx')
print(datetime.now()-startTime)

presentation = PowerPoint()
presentation.AddSlide(1)
presentation.Presentation.save('C:\Users\ktlj659\Documents\Python\\3PRM\Exports\PowerPoints\\test.pptx')

