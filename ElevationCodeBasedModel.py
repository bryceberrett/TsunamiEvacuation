"""
Model exported as python.
Name : Tsunami Evacuation 10
Group : Hazard Evacuation
With QGIS : 31400
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterVectorDestination
from qgis.core import QgsProcessingParameterRasterDestination
import processing


class TsunamiEvacuation10(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        # Input the area that will likely be safe from a Tsunami here. The objective will be greater, but this will encourage people to get to moderatly high ground first if possible.
        self.addParameter(QgsProcessingParameterNumber('1TeirofSafetyMinvalue', '1rst Teir of Safety Min value', type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=20))
        self.addParameter(QgsProcessingParameterNumber('1TeirofSafetyMinvalue (2)', '1rst Teir of Safety MAX value', type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=999))
        self.addParameter(QgsProcessingParameterNumber('1TeirofSafetyMinvalue (2) (2)', '1rst Teir of Safety New (lower) value', type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=1))
        self.addParameter(QgsProcessingParameterNumber('1TeirofSafetyMinvalue (2) (2) (2)', '1rst Teir of Safety Penalty (outside safety region)', type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=3))
        self.addParameter(QgsProcessingParameterRasterLayer('DEM', 'DEM', defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('EvacuationElevation', 'Evacuation Elevation', optional=True, type=QgsProcessingParameterNumber.Double, minValue=1, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('InundationAreaorHazardRegion', 'Inundation Area or Hazard Region', optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('LowBoundHazardRasterReclassify', 'Low Bound Hazard Raster Reclassify', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=9.95))
        self.addParameter(QgsProcessingParameterNumber('OffRoadDefaultTerrainValue', 'Off Road Default Terrain Value', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=2))
        self.addParameter(QgsProcessingParameterVectorLayer('RegionofInterest', 'Region of Interest', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('RoadWeightValue', 'Road Weight Value', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=1))
        self.addParameter(QgsProcessingParameterVectorLayer('Roads', 'Roads', optional=True, types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('SlopeRange1MinValue', 'Slope Range 1 Min Value', type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=-1000))
        self.addParameter(QgsProcessingParameterNumber('SlopeRange1MinValue (2)', 'Slope Range 1 Max Value', type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=30))
        self.addParameter(QgsProcessingParameterNumber('SlopeRange1MinValue (2) (2)', 'Slope Range 1 New Value', type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=1))
        self.addParameter(QgsProcessingParameterNumber('SlopeRange1MinValue (2) (2) (2)', 'Slope Range 2 New Value', type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=3))
        self.addParameter(QgsProcessingParameterNumber('SlopeRange1MinValue (2) (2) (2) (2)', 'Slope Range 3 New Value', type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=1000))
        self.addParameter(QgsProcessingParameterNumber('SlopeRange1MinValue (2) (3)', 'Slope Range 2 Max Value', type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=50))
        self.addParameter(QgsProcessingParameterNumber('SlopeRange1MinValue (2) (3) (2)', 'Slope Range 3 Max Value', type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=90))
        self.addParameter(QgsProcessingParameterNumber('SlopeRange1MinValue (3)', 'Slope Range 2 Min Value', type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=30))
        self.addParameter(QgsProcessingParameterNumber('SlopeRange1MinValue (3) (2)', 'Slope Range 3 Min Value', type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=50))
        self.addParameter(QgsProcessingParameterVectorLayer('StartingPoints', 'Starting Points', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('Var1AllOtherRange1Value', 'Var 1 AllOther Range 1 Value', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=1))
        self.addParameter(QgsProcessingParameterNumber('Var1AllOtherRange1Value (2)', 'Var 2 AllOther Range 1 Value', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=1))
        self.addParameter(QgsProcessingParameterNumber('Var1AllOtherRange1Value (2) (2)', 'Var 3 AllOther Range 1 Value', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=1))
        self.addParameter(QgsProcessingParameterNumber('Var1AllOtherRange1Value (2) (2) (2)', 'Var 4 AllOther Range 1 Value', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=1))
        self.addParameter(QgsProcessingParameterNumber('Var1AllOtherRange1Value (2) (2) (2) (2)', 'Var 5 AllOther Range 1 Value', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=1))
        self.addParameter(QgsProcessingParameterNumber('Var1MinRange1', 'Var 1 Min Range 1', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=-100000))
        self.addParameter(QgsProcessingParameterNumber('Var1MinRange1 (2)', 'Var 1 Max Range 1', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('Var1MinRange1 (2) (2)', 'Var 2 Max Range 1', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('Var1MinRange1 (2) (2) (2)', 'Var 3 Max Range 1', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('Var1MinRange1 (2) (2) (2) (2)', 'Var 4 Max Range 1', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('Var1MinRange1 (2) (2) (2) (2) (2)', 'Var 5 Max Range 1', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('Var1MinRange1 (3)', 'Var 2 Min Range 1', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=-10000))
        self.addParameter(QgsProcessingParameterNumber('Var1MinRange1 (3) (2)', 'Var 3 Min Range 1', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('Var1MinRange1 (3) (2) (2)', 'Var 4 Min Range 1', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('Var1MinRange1 (3) (2) (2) (2)', 'Var 5 Min Range 1', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('Var1NewRange1Value', 'Var 1 New Range 1 Value', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('Var1NewRange1Value (2)', 'Var 2 New Range 1 Value', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('Var1NewRange1Value (2) (2)', 'Var 3 New Range 1 Value', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('Var1NewRange1Value (2) (2) (2)', 'Var 4 New Range 1 Value', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('Var1NewRange1Value (2) (2) (2) (2)', 'Var 5 New Range 1 Value', optional=True, type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('VariableCellSize', 'Variable Cell Size', type=QgsProcessingParameterNumber.Double, minValue=1, maxValue=10, defaultValue=4))
        self.addParameter(QgsProcessingParameterVectorLayer('VariableObstacles1', 'Variable Obstacles 1', optional=True, types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('VariableObstacles2', 'Variable Obstacles 2', optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('VariableObstacles2 (2)', 'Variable Obstacles 3', optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('VariableObstacles2 (2) (2)', 'Variable Obstacles 4', optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('VariableObstacles2 (2) (2) (2)', 'Variable Obstacles 5', optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('EvacuationRoutes', 'Evacuation Routes', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorDestination('ObjectivePolygon', 'Objective Polygon', type=QgsProcessing.TypeVectorPolygon, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('SlopeRaster', 'Slope Raster', optional=True, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('DestinationPoints', 'Destination points', type=QgsProcessing.TypeVectorPoint, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('WeightedRaster', 'Weighted Raster', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorDestination('EvacuationContourMinHeight', 'Evacuation Contour Min Height', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('WeightedRaster', 'Weighted Raster', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('TierOfSafetyWeight', '1 Tier of Safety Weight', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('WeightedRoads', 'Weighted Roads', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('WeightedVariable1Raster', 'Weighted Variable 1 Raster', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('WeightedVariable2Raster', 'Weighted Variable 2 Raster', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('WeightedSlope', 'Weighted Slope', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(25, model_feedback)
        results = {}
        outputs = {}

        # Clip DEM
        alg_params = {
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': parameters['DEM'],
            'NODATA': None,
            'OPTIONS': '',
            'PROJWIN': '12362689.951099999,12376773.534200000,-917565.557600000,-903240.541600000 [EPSG:3395]',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ClipDem'] = processing.run('gdal:cliprasterbyextent', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Clipped Variable 1
        alg_params = {
            'CLIP': True,
            'EXTENT': parameters['RegionofInterest'],
            'INPUT': parameters['VariableObstacles1'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ClippedVariable1'] = processing.run('native:extractbyextent', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Variable 1 to Raster
        alg_params = {
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_RASTER_FORMAT_META': '',
            'GRASS_RASTER_FORMAT_OPT': '',
            'GRASS_REGION_CELLSIZE_PARAMETER': parameters['VariableCellSize'],
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'attribute_column': '',
            'input': outputs['ClippedVariable1']['OUTPUT'],
            'label_column': '',
            'memory': 300,
            'rgb_column': '',
            'type': [0,1,3],
            'use': 2,
            'value': 1,
            'where': '',
            'output': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Variable1ToRaster'] = processing.run('grass7:v.to.rast', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Variable 1 Reclassify
        alg_params = {
            'INPUT': outputs['Variable1ToRaster']['output'],
            'MAX': parameters['Var1MinRange1 (2)'],
            'MIN': parameters['Var1MinRange1'],
            'NODATA': 1,
            'NODATAOPT': True,
            'OTHEROPT': True,
            'OTHERS': parameters['Var1NewRange1Value'],
            'RNEW': parameters['Var1NewRange1Value'],
            'ROPERATOR': 0,
            'RESULT': parameters['WeightedVariable1Raster']
        }
        outputs['Variable1Reclassify'] = processing.run('saga:reclassifyvaluesrange', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['WeightedVariable1Raster'] = outputs['Variable1Reclassify']['RESULT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Clipped Variable 2
        alg_params = {
            'CLIP': True,
            'EXTENT': parameters['RegionofInterest'],
            'INPUT': parameters['VariableObstacles2'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ClippedVariable2'] = processing.run('native:extractbyextent', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Reclassify DEM first Tier safer zone
        alg_params = {
            'INPUT': outputs['ClipDem']['OUTPUT'],
            'MAX': parameters['1TeirofSafetyMinvalue (2)'],
            'MIN': parameters['1TeirofSafetyMinvalue'],
            'NODATA': 1,
            'NODATAOPT': True,
            'OTHEROPT': True,
            'OTHERS': parameters['1TeirofSafetyMinvalue (2) (2) (2)'],
            'RNEW': parameters['1TeirofSafetyMinvalue (2) (2)'],
            'ROPERATOR': 0,
            'RESULT': parameters['TierOfSafetyWeight']
        }
        outputs['ReclassifyDemFirstTierSaferZone'] = processing.run('saga:reclassifyvaluesrange', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['TierOfSafetyWeight'] = outputs['ReclassifyDemFirstTierSaferZone']['RESULT']

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Slope
        # Works
        alg_params = {
            '-a': True,
            '-e': False,
            '-n': False,
            'GRASS_RASTER_FORMAT_META': '',
            'GRASS_RASTER_FORMAT_OPT': '',
            'GRASS_REGION_CELLSIZE_PARAMETER': 0,
            'GRASS_REGION_PARAMETER': None,
            'aspect': 'TEMPORARY_OUTPUT',
            'dx': 'TEMPORARY_OUTPUT',
            'dxx': 'TEMPORARY_OUTPUT',
            'dxy': 'TEMPORARY_OUTPUT',
            'dy': 'TEMPORARY_OUTPUT',
            'dyy': 'TEMPORARY_OUTPUT',
            'elevation': outputs['ClipDem']['OUTPUT'],
            'format': 0,
            'min_slope': 0,
            'pcurvature': 'TEMPORARY_OUTPUT',
            'precision': 0,
            'tcurvature': 'TEMPORARY_OUTPUT',
            'zscale': 1,
            'slope': parameters['SlopeRaster']
        }
        outputs['Slope'] = processing.run('grass7:r.slope.aspect', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SlopeRaster'] = outputs['Slope']['slope']

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Variable 2 to Raster
        alg_params = {
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_RASTER_FORMAT_META': '',
            'GRASS_RASTER_FORMAT_OPT': '',
            'GRASS_REGION_CELLSIZE_PARAMETER': parameters['VariableCellSize'],
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'attribute_column': '',
            'input': outputs['ClippedVariable2']['OUTPUT'],
            'label_column': '',
            'memory': 300,
            'rgb_column': '',
            'type': [0,1,3],
            'use': 2,
            'value': 1,
            'where': '',
            'output': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Variable2ToRaster'] = processing.run('grass7:v.to.rast', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Clip Roads
        alg_params = {
            'INPUT': parameters['Roads'],
            'OVERLAY': parameters['RegionofInterest'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ClipRoads'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Elev Objective Raster
        alg_params = {
            'INPUT': outputs['ClipDem']['OUTPUT'],
            'MAX': 100000,
            'MIN': parameters['EvacuationElevation'],
            'NODATA': 0,
            'NODATAOPT': False,
            'OTHEROPT': True,
            'OTHERS': 0,
            'RNEW': 1,
            'ROPERATOR': 0,
            'RESULT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ElevObjectiveRaster'] = processing.run('saga:reclassifyvaluesrange', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Variable 2 Reclassify
        alg_params = {
            'INPUT': outputs['Variable2ToRaster']['output'],
            'MAX': parameters['Var1MinRange1 (2) (2)'],
            'MIN': parameters['Var1MinRange1 (3)'],
            'NODATA': 1,
            'NODATAOPT': True,
            'OTHEROPT': True,
            'OTHERS': parameters['Var1AllOtherRange1Value (2)'],
            'RNEW': parameters['Var1NewRange1Value (2)'],
            'ROPERATOR': 0,
            'RESULT': parameters['WeightedVariable2Raster']
        }
        outputs['Variable2Reclassify'] = processing.run('saga:reclassifyvaluesrange', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['WeightedVariable2Raster'] = outputs['Variable2Reclassify']['RESULT']

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Create No Data Values (Translate)
        alg_params = {
            'COPY_SUBDATASETS': False,
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': outputs['ElevObjectiveRaster']['RESULT'],
            'NODATA': 0,
            'OPTIONS': '',
            'TARGET_CRS': 'ProjectCrs',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CreateNoDataValuesTranslate'] = processing.run('gdal:translate', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Slope Reclassify 1
        # Works
        alg_params = {
            'INPUT': outputs['Slope']['slope'],
            'MAX': parameters['SlopeRange1MinValue (2)'],
            'MIN': parameters['SlopeRange1MinValue'],
            'NODATA': 0,
            'NODATAOPT': False,
            'OTHEROPT': False,
            'OTHERS': 0,
            'RNEW': parameters['SlopeRange1MinValue (2) (2)'],
            'ROPERATOR': 0,
            'RESULT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SlopeReclassify1'] = processing.run('saga:reclassifyvaluesrange', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Objective: Polygonize (raster to vector)
        alg_params = {
            'BAND': 1,
            'EIGHT_CONNECTEDNESS': False,
            'EXTRA': '',
            'FIELD': 'Evacuation Objective',
            'INPUT': outputs['CreateNoDataValuesTranslate']['OUTPUT'],
            'OUTPUT': parameters['ObjectivePolygon']
        }
        outputs['ObjectivePolygonizeRasterToVector'] = processing.run('gdal:polygonize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ObjectivePolygon'] = outputs['ObjectivePolygonizeRasterToVector']['OUTPUT']

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Contour Evac Area Min Height
        alg_params = {
            'GRID': outputs['ElevObjectiveRaster']['RESULT'],
            'VERTEX': 0,
            'ZMAX': parameters['EvacuationElevation'],
            'ZMIN': parameters['EvacuationElevation'],
            'ZSTEP': parameters['EvacuationElevation'],
            'CONTOUR': parameters['EvacuationContourMinHeight']
        }
        outputs['ContourEvacAreaMinHeight'] = processing.run('saga:contourlines', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['EvacuationContourMinHeight'] = outputs['ContourEvacAreaMinHeight']['CONTOUR']

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Slope Reclassify 2
        # Works
        alg_params = {
            'INPUT': outputs['SlopeReclassify1']['RESULT'],
            'MAX': parameters['SlopeRange1MinValue (2) (3)'],
            'MIN': parameters['SlopeRange1MinValue (3)'],
            'NODATA': 0,
            'NODATAOPT': False,
            'OTHEROPT': False,
            'OTHERS': 0,
            'RNEW': parameters['SlopeRange1MinValue (3)'],
            'ROPERATOR': 1,
            'RESULT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SlopeReclassify2'] = processing.run('saga:reclassifyvaluesrange', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Roads Raster
        alg_params = {
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_RASTER_FORMAT_META': '',
            'GRASS_RASTER_FORMAT_OPT': '',
            'GRASS_REGION_CELLSIZE_PARAMETER': 3,
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'attribute_column': '',
            'input': outputs['ClipRoads']['OUTPUT'],
            'label_column': '',
            'memory': 300,
            'rgb_column': '',
            'type': [0,1,3],
            'use': 2,
            'value': 1,
            'where': '',
            'output': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RoadsRaster'] = processing.run('grass7:v.to.rast', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Raster pixels to points
        alg_params = {
            'FIELD_NAME': 'VALUE',
            'INPUT_RASTER': outputs['CreateNoDataValuesTranslate']['OUTPUT'],
            'RASTER_BAND': 1,
            'OUTPUT': parameters['DestinationPoints']
        }
        outputs['RasterPixelsToPoints'] = processing.run('native:pixelstopoints', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['DestinationPoints'] = outputs['RasterPixelsToPoints']['OUTPUT']

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Roads Reclassify
        alg_params = {
            'INPUT': outputs['RoadsRaster']['output'],
            'MAX': 2,
            'MIN': -10000,
            'NODATA': parameters['OffRoadDefaultTerrainValue'],
            'NODATAOPT': True,
            'OTHEROPT': True,
            'OTHERS': parameters['RoadWeightValue'],
            'RNEW': parameters['RoadWeightValue'],
            'ROPERATOR': 0,
            'RESULT': parameters['WeightedRoads']
        }
        outputs['RoadsReclassify'] = processing.run('saga:reclassifyvaluesrange', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['WeightedRoads'] = outputs['RoadsReclassify']['RESULT']

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Slope Reclassify 3
        # Works
        alg_params = {
            'INPUT': outputs['SlopeReclassify2']['RESULT'],
            'MAX': parameters['SlopeRange1MinValue (2) (3) (2)'],
            'MIN': parameters['SlopeRange1MinValue (3) (2)'],
            'NODATA': 0,
            'NODATAOPT': False,
            'OTHEROPT': False,
            'OTHERS': 0,
            'RNEW': parameters['SlopeRange1MinValue (2) (2) (2) (2)'],
            'ROPERATOR': 0,
            'RESULT': parameters['WeightedSlope']
        }
        outputs['SlopeReclassify3'] = processing.run('saga:reclassifyvaluesrange', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['WeightedSlope'] = outputs['SlopeReclassify3']['RESULT']

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Weighed Cost Raster
        alg_params = {
            'CELLSIZE': 0,
            'CRS': None,
            'EXPRESSION': '\"\'Weighted Slope\' from algorithm \'Slope Reclassify 3\'@1\"  * \"\'Weighted Variable 2 Raster\' from algorithm \'Variable 2 Reclassify\'@1\" * \"\'Weighted Variable 1 Raster\' from algorithm \'Variable 1 Reclassify\'@1\" * \"\'Weighted Roads\' from algorithm \'Roads Reclassify\'@1\" * \"\'1 Tier of Safety Weight\' from algorithm \'Reclassify DEM first Tier safer zone\'@1\"',
            'EXTENT': None,
            'LAYERS': [outputs['ReclassifyDemFirstTierSaferZone']['RESULT'],outputs['RoadsReclassify']['RESULT'],outputs['Variable1Reclassify']['RESULT'],outputs['Variable2Reclassify']['RESULT'],outputs['SlopeReclassify3']['RESULT']],
            'OUTPUT': parameters['WeightedRaster']
        }
        outputs['WeighedCostRaster'] = processing.run('qgis:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['WeightedRaster'] = outputs['WeighedCostRaster']['OUTPUT']

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Eleminate negative values
        alg_params = {
            'INPUT': outputs['WeighedCostRaster']['OUTPUT'],
            'MAX': 1,
            'MIN': -999999999,
            'NODATA': 1,
            'NODATAOPT': True,
            'OTHEROPT': False,
            'OTHERS': 0,
            'RNEW': 1,
            'ROPERATOR': 0,
            'RESULT': parameters['WeightedRaster']
        }
        outputs['EleminateNegativeValues'] = processing.run('saga:reclassifyvaluesrange', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['WeightedRaster'] = outputs['EleminateNegativeValues']['RESULT']

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Least Cost Path
        alg_params = {
            'BOOLEAN_FIND_LEAST_PATH_TO_ALL_ENDS': True,
            'BOOLEAN_OUTPUT_LINEAR_REFERENCE': False,
            'INPUT_COST_RASTER': outputs['EleminateNegativeValues']['RESULT'],
            'INPUT_END_LAYER': outputs['RasterPixelsToPoints']['OUTPUT'],
            'INPUT_RASTER_BAND': 1,
            'INPUT_START_LAYER': parameters['StartingPoints'],
            'OUTPUT': parameters['EvacuationRoutes']
        }
        outputs['LeastCostPath'] = processing.run('Cost distance analysis:Least Cost Path', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['EvacuationRoutes'] = outputs['LeastCostPath']['OUTPUT']

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        return results

    def name(self):
        return 'Tsunami Evacuation 10'

    def displayName(self):
        return 'Tsunami Evacuation 10'

    def group(self):
        return 'Hazard Evacuation'

    def groupId(self):
        return 'Hazard Evacuation'

    def createInstance(self):
        return TsunamiEvacuation10()
