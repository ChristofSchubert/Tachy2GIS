# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Tachy2Gis
                                 A QGIS plugin
 This plugin allows to create geometries directly with a connected tachymeter
                              -------------------
        begin                : 2017-11-26
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Christian Trapp
        email                : mail@christiantrapp.net
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os.path
from . import resources

from PyQt5.QtSerialPort import QSerialPortInfo, QSerialPort
from PyQt5.QtWidgets import QAction, QHeaderView, QDialog, QFileDialog, QMessageBox
from PyQt5.QtCore import QSettings, QItemSelectionModel, QTranslator, QCoreApplication, QThread, qVersion, Qt
from PyQt5.QtGui import QIcon
from qgis.utils import iface
from qgis.core import *#QgsPoint,QgsMapLayerProxyModel, QgsExpressionContextUtils, QgsProject, QgsMessageLog, Qgis, QgsWkbTypes
from qgis.gui import QgsMapToolPan

from .T2G.VertexList import T2G_VertexList, T2G_Vertex
from .T2G.TachyReader import TachyReader
from .FieldDialog import FieldDialog
from .T2G.VertexPickerTool import T2G_VertexePickerTool
from .Tachy2GIS_dialog import Tachy2GisDialog

import datetime

# Initialize Qt resources from file resources.py

# Import the code for the dialog


class Tachy2Gis:

    """QGIS Plugin Implementation."""
    # Custom methods go here:

    def vertexReceived(self, line):
        newVtx = T2G_Vertex.fromGSI(line)
        self.mapTool.addVertex(vtx=newVtx)

    ## Clears the map canvas and in turn the vertexList
    def clearCanvas(self):
        self.mapTool.clear()

    ## Opens the field dialog in preparation of dumping new vertices to the target layer
    def dump(self):

        # the input table of the dialog is updated
        targetLayer = self.dlg.sourceLayerComboBox.currentLayer()
        # if the target layer holds point geometries, only the currently selected vertex is dumped and
        # removed from the list
        project = QgsProject.instance()
        QgsExpressionContextUtils.setProjectVariable(project, 'maxWerteAktualisieren', 'False')
        #QgsMessageLog.logMessage('Test', 'T2G Archäologie', Qgis.Info)
        if targetLayer.geometryType() == QgsWkbTypes.PointGeometry: # Timmel
             for i in range(0,len(self.vertexList)):
                #QgsExpressionContextUtils.setProjectVariable(project, 'SignalGeometrieNeu', 'True')
                self.dlg.vertexTableView.selectRow(i)
                self.vertexList.dumpToFile(targetLayer, self.fieldDialog.fieldData)
                #QgsExpressionContextUtils.setProjectVariable(project, 'SignalGeometrieNeu', 'False')
            # self.mapTool.deleteVertex()
            # otherwise the list is cleared
            #self.mapTool.clear()
        else:
            #QgsExpressionContextUtils.setProjectVariable(project, 'SignalGeometrieNeu', 'True')
            self.vertexList.dumpToFile(targetLayer, self.fieldDialog.fieldData)
            #QgsExpressionContextUtils.setProjectVariable(project, 'SignalGeometrieNeu', 'False')
            # otherwise the list is cleared
            #self.mapTool.clear()

        #QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(), 'SignalGeometrieNeu', 'False')
        targetLayer.commitChanges()
        # Attributdialog mit Filter zum schreiben öffnen
        # letzte id ermitteln
        idfeld = targetLayer.dataProvider().fieldNameIndex('id')

        if targetLayer.maximumValue(idfeld) == None:
            idmaxi = 0
        else:
            idmaxi = targetLayer.maximumValue(idfeld)

        if targetLayer.geometryType() == QgsWkbTypes.PointGeometry:
            query = "id >= " + str(int(idmaxi)-len(self.vertexList) + 1)
        else:
            query = "id = " + str(int(idmaxi))

        self.messpunktAdd()
        targetLayer.startEditing()
        targetLayer.fields().at(0).constraints().constraintDescription(), 'desc'
        #self.iface.openFeatureForm(targetLayer, 3, True)
        box = self.iface.showAttributeTable(targetLayer, query)
        box.exec_()
        self.mapTool.clear()
        targetLayer.commitChanges()
        QgsExpressionContextUtils.setProjectVariable(project, 'maxWerteAktualisieren', 'True')
        self.iface.mapCanvas().refreshAllLayers()
        targetLayer.removeSelection()

    def messpunktAdd(self):
        #T2G_Vertex.messliste.clear()
        #T2G_Vertex.messliste.append({'pointId': 1, 'targetX': 1, 'targetY': 1, 'targetZ': 1})
        #T2G_Vertex.messliste.append({'pointId': 2, 'targetX': 1, 'targetY': 1, 'targetZ': 1})
        #T2G_Vertex.messliste.append({'pointId': 3, 'targetX': 1, 'targetY': 1, 'targetZ': 1})
        layer = QgsProject.instance().mapLayersByName('Messpunkte')[0]
        layer.startEditing()
        for item in T2G_Vertex.messliste:
            ptnr = str(item['pointId']).lstrip("0")
            x = str(item['targetX'])
            y = str(item['targetY'])
            z = str(item['targetZ'])
            # Timmel Spiegelhöhe
            try:
                project = QgsProject.instance()
                reflH = QgsExpressionContextUtils.projectScope(project).variable('reflH')
                reflH = float(reflH)
                z = round(float(z) - reflH, 3)
            except:
                pass

            pt = QgsPoint(float(x), float(y), float(z))
            attL = {'ptnr': ptnr, 'x': x, 'y': y, 'z': z, 'reflH': reflH}
            self.addPoint3D(layer, pt, attL)
            QgsMessageLog.logMessage(str(ptnr)+'|'+str(x)+'|'+str(y)+'|'+str(z), 'Messpunkte', Qgis.Info)
        layer.commitChanges()
        layer.removeSelection()

    def addPoint3D(self, layer, point, attListe):
        #layer.startEditing()
        feature = QgsFeature()
        fields = layer.fields()
        feature.setFields(fields)
        feature.setGeometry(QgsGeometry(point))
        # Attribute
        layer.dataProvider().addFeatures([feature])
        layer.updateExtents()
        features = [feature for feature in layer.getFeatures()]
        lastfeature = features[-1]

        for item in attListe:
            #QgsMessageLog.logMessage(str(item), 'T2G', Qgis.Info)
            fIndex = layer.dataProvider().fieldNameIndex(item)
            layer.changeAttributeValue(lastfeature.id(), fIndex, attListe[item])
        T2G_VertexList.addStaticAttribut(self,layer, lastfeature)
        #layer.commitChanges()

    def snap(self):
        if self.dlg.checkBox.isChecked():
            T2G_VertexList.snap = 1
        else:
            T2G_VertexList.snap = 0


    ## Restores the map tool to the one that was active before T2G was started
    #  The pan tool is the default tool used by QGIS
    def restoreTool(self):
        if self.previousTool is None:
            self.previousTool = QgsMapToolPan(self.iface.mapCanvas())
        self.iface.mapCanvas().setMapTool(self.previousTool)
        self.iface.actionSelectRectangle().trigger()

    def setActiveLayer(self): #Timmel
        if Qt is None:
            return
        activeLayer = self.dlg.sourceLayerComboBox.currentLayer()
        if activeLayer is None or activeLayer.type() == QgsMapLayer.RasterLayer:
            return
        self.iface.setActiveLayer(activeLayer)
        self.vertexList.updateAnchors(activeLayer)
        
    def targetChanged(self):
        targetLayer = self.fieldDialog.targetLayerComboBox.setLayer # Timmel
        self.mapTool.setGeometryType(targetLayer)

    def toggleEdit(self):
        iface.actionToggleEditing().trigger()

    def connectSerial(self):
        port = self.dlg.portComboBox.currentText()
        self.tachyReader.setPort(port)

    def setLog(self):
        logFileName = QFileDialog.getSaveFileName()[0]
        self.dlg.logFileEdit.setText(logFileName)
        self.tachyReader.setLogfile(logFileName)

    def dumpEnabled(self):
        verticesAvailable = (len(self.vertexList) > 0) # tim > durch >= ersetzt
        # Selecting a target layer while there are no vertices in the vertex list may cause segfaults. To avoid this,
        # the 'Dump' button is disabled as long there are none:
        self.dlg.dumpButton.setEnabled(verticesAvailable)

    # Interface code goes here:
    def setupControls(self):
        """This method connects all controls in the UI to their callbacks.
        It is called in ad_action"""

        portNames = [port.portName() for port in QSerialPortInfo.availablePorts()]
        self.dlg.portComboBox.addItems(portNames)
        self.dlg.portComboBox.currentIndexChanged.connect(self.connectSerial)

        self.dlg.logFileButton.clicked.connect(self.setLog)

        self.dlg.deleteAllButton.clicked.connect(self.clearCanvas)
        self.dlg.finished.connect(self.mapTool.clear)
        self.dlg.dumpButton.clicked.connect(self.dump)
        self.dlg.deleteVertexButton.clicked.connect(self.mapTool.deleteVertex)
        
        self.dlg.vertexTableView.setModel(self.vertexList)
        self.dlg.vertexTableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.dlg.vertexTableView.setSelectionModel(QItemSelectionModel(self.vertexList))
        self.dlg.vertexTableView.selectionModel().selectionChanged.connect(self.mapTool.selectVertex)
        
        self.dlg.finished.connect(self.restoreTool)
        self.dlg.accepted.connect(self.restoreTool)
        self.dlg.rejected.connect(self.restoreTool)


        self.dlg.sourceLayerComboBox.layerChanged.connect(self.setActiveLayer)
        self.dlg.sourceLayerComboBox.layerChanged.connect(self.mapTool.clear)


        self.fieldDialog.targetLayerComboBox.layerChanged.connect(self.targetChanged)
        self.vertexList.layoutChanged.connect(self.dumpEnabled)

        self.dlg.checkBox.stateChanged.connect(self.snap)


    ## Constructor
    #  @param iface An interface instance that will be passed to this class
    #  which provides the hook by which you can manipulate the QGIS
    #  application at run time.
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Tachy2Gis_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr('&Tachy2GIS')
        self.toolbar = self.iface.addToolBar('Tachy2Gis')
        self.toolbar.setObjectName('Tachy2Gis')
        
        ## From here: Own additions
        self.vertexList = T2G_VertexList()
        
        self.mapTool = T2G_VertexePickerTool(self)
        self.previousTool = None
        self.fieldDialog = FieldDialog(self.iface.activeLayer())
        self.tachyReader = TachyReader(QSerialPort.Baud9600)
        self.pollingThread = QThread()
        self.tachyReader.moveToThread(self.pollingThread)
        self.pollingThread.start()
        self.tachyReader.lineReceived.connect(self.vertexReceived)
        self.tachyReader.beginListening()

    # noinspection PyMethodMayBeStatic

    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Tachy2Gis', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = Tachy2GisDialog(iface.mainWindow()) # Dialog im Vordergrund halten.
        self.setupControls()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Tachy2Gis/icon.png'
        self.add_action(
            icon_path,
            text=self.tr('Tachy2GIS'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr('&Tachy2GIS'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
        if self.pollingThread.isRunning():
            self.tachyReader.shutDown()
            self.pollingThread.terminate()
            self.pollingThread.wait()


    def run(self):
        """Run method that performs all the real work"""
        # Store the active map tool and switch to the T2G_VertexPickerTool
        self.previousTool = self.iface.mapCanvas().mapTool()
        self.iface.mapCanvas().setMapTool(self.mapTool)
        self.mapTool.alive = True
        #self.setActiveLayer()
        self.dlg.sourceLayerComboBox.setLayer(self.iface.activeLayer())
        self.dlg.show()

        outLayerList = []
        self.layerLine = QgsProject.instance().mapLayersByName('E_Line')[0]
        self.layerPoly = QgsProject.instance().mapLayersByName('E_Polygon')[0]
        self.layerPoint = QgsProject.instance().mapLayersByName('E_Point')[0]
        for lay in QgsProject.instance().mapLayers().values():
            if lay == self.layerLine or lay == self.layerPoly or lay == self.layerPoint:
                QgsMessageLog.logMessage('gleich', 'T2G Archäologie', Qgis.Info)
                pass
            else:
                QgsMessageLog.logMessage(lay.name(), 'T2G Archäologie', Qgis.Info)
                outLayerList.append(lay)
        self.dlg.sourceLayerComboBox.setExceptedLayerList(outLayerList)

        # Run the dialog event loop
        #result = self.dlg.exec_()
        # See if OK was pressed
        #self.dlg.close()
        #if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            #pass
