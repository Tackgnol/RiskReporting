from Components.Processor import DataProcessor
from Components.GetData import GetData
from Tkinter import Tk
from tkFileDialog import askopenfilename
from Components.Common import AZColors
from Components.Visualizer import Visualizer

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
fileDirectory = askopenfilename()
try:
    dataSouce = GetData(fileDirectory,';')
except ValueError as e:
    print(e)

except TypeError as e:
    print(e)


azColorScheme =  AZColors.AZColorScheme()
fieldList = [
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

DataProcessor.RegionMapping(dataSouce.Data)
DataProcessor.SubRegionMapping(dataSouce.Data)
for field in fieldList:
    DataProcessor.ReviewApprovalIndicator(dataSouce.Data, unicode(field))
DataProcessor.EngagementMonth(dataSouce.Data)
DataProcessor.EngagmentYear(dataSouce.Data)
DataProcessor.RatingOccurences(dataSouce.Data)
DataProcessor.ReviewApprovalTime(dataSouce.Data)
DataProcessor.SeperateCategoryAndSubCategory(dataSouce.Data)
DataProcessor.SetAreaMapping(dataSouce.Data)


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
visualizations.GenerateBarChart(u'Engagement Month')
for field in fieldList:
    visualizations.GenerateHeatMap(field + u' indicator', u'Region', u'AZ Engagement Name', azColorScheme, 'count')

for field in fieldList:
    visualizations.GenerateHeatMap(field + u' indicator', u'Cluster', u'AZ Engagement Name', azColorScheme, 'count')

for field in fieldList:
    visualizations.GenerateHeatMap(field + u' indicator', u'Engagement Month', u'AZ Engagement Name', azColorScheme, 'count')

for field in fieldList:
    visualizations.GenerateHeatMap(field + u' indicator', u'Set Area', u'AZ Engagement Name', azColorScheme, 'count')

dataSouce.Data.to_excel('C:\Users\ktlj659\Documents\Python\\3PRM\Exports\Excels\export.xlsx')