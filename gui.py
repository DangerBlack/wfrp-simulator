#!/usr/bin/python

import sys
import glob
import shutil
import os
import random
import wfrp
from PyQt4 import QtGui, QtCore

def getFighterRaw(folder="database/*"):    
    listOfFighter=[]
    for f in glob.glob(folder):
        listOfFighter.append(f.split("/")[1].split(".yaml")[0])
    return listOfFighter

def getFightersFromArchive():
    return getFighterRaw("database/*")

def getFightersFromActive():
    return getFighterRaw("fighters/*")


class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle('W.F.R.P - Simulator')
        self.resize(800, 600)
        panel = QtGui.QWidget(self)
        
        hBox = QtGui.QHBoxLayout()
        hBox.setSpacing(5)
        
        v1Box = QtGui.QVBoxLayout()
        v1Box.setSpacing(2)
        
        '''button = QtGui.QPushButton('Quit',cWidget);
        button.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold));
        self.connect(button, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'));'''
        
        
        #ADD LIST OF FIGHTER FROM DATABASE
        self.archiveListWidget = QtGui.QListWidget()
        self.archiveListWidget.setMinimumWidth(200)
        lof = getFightersFromArchive()        
        for i in lof:
            item = QtGui.QListWidgetItem(i)
            self.archiveListWidget.addItem(item)
        v1Box.addWidget(self.archiveListWidget)
        
        addFighter = QtGui.QPushButton('Add >',panel);
        addFighter.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold));
        self.connect(addFighter, QtCore.SIGNAL('clicked()'), self.addFighterToActive);
        v1Box.addWidget(addFighter)
        
        hBox.addLayout(v1Box)
        
        v2Box = QtGui.QVBoxLayout()
        v2Box.setSpacing(2)
        
        #ADD LIST OF FIGHTER FROM FIGHTERS FOLDER
        self.fighterListWidget = QtGui.QListWidget()
        self.fighterListWidget.setMinimumWidth(200)
        lof = getFightersFromActive()
        for i in lof:
            item = QtGui.QListWidgetItem(i)
            self.fighterListWidget.addItem(item)      
        v2Box.addWidget(self.fighterListWidget)
        
        delete = QtGui.QPushButton('Delete',panel);
        self.connect(delete, QtCore.SIGNAL('clicked()'), self.deleteFromActiveFighter);
        delete.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold));
        v2Box.addWidget(delete)
        
        hBox.addLayout(v2Box)
        
        v3Box = QtGui.QVBoxLayout()
        v3Box.setSpacing(2)
        
        hIBox = QtGui.QVBoxLayout()
        hIBox.setSpacing(2)
        
        label = QtGui.QLabel('Name');
        label.setMaximumHeight(30)
        hIBox.addWidget(label)
        inName = QtGui.QLineEdit();
        inName.setMaximumHeight(30)
        hIBox.addWidget(inName)
        
        #PRIMARY LABEL
        hPBox =QtGui.QHBoxLayout()
        hPBox.setSpacing(1)
        for i in range(8):
            label = QtGui.QLabel('AB')
            label.setMaximumWidth(400/8)
            label.setMaximumHeight(30)
            hPBox.addWidget(label)
        hIBox.addLayout(hPBox)
        
        #PRIMARY INPUT
        hPBox =QtGui.QHBoxLayout()
        hPBox.setSpacing(1)
        for i in range(8):
            inName = QtGui.QLineEdit();
            inName.setMaximumWidth(400/8)
            inName.setMaximumHeight(30)
            hPBox.addWidget(inName)        
        hIBox.addLayout(hPBox)
        
        #SECONDARY LABEL
        hPBox =QtGui.QHBoxLayout()
        hPBox.setSpacing(1)
        for i in range(8):
            label = QtGui.QLabel('AB')
            label.setMaximumWidth(400/8)
            label.setMaximumHeight(30)
            hPBox.addWidget(label)
        hIBox.addLayout(hPBox)
        
        #SECONDARY INPUT
        hPBox =QtGui.QHBoxLayout()
        hPBox.setSpacing(1)
        for i in range(8):
            inName = QtGui.QLineEdit();
            inName.setMaximumWidth(400/8)
            inName.setMaximumHeight(30)
            hPBox.addWidget(inName)        
        hIBox.addLayout(hPBox)
        
        checkBox = QtGui.QCheckBox("Normal checkbox", panel)
        checkBox.setChecked(True)
        hIBox.addWidget(checkBox)
        checkBox = QtGui.QCheckBox("Normal checkbox", panel)
        checkBox.setChecked(True)
        hIBox.addWidget(checkBox)
        checkBox = QtGui.QCheckBox("Normal checkbox", panel)
        checkBox.setChecked(True)
        hIBox.addWidget(checkBox)
        
        inSpell = QtGui.QTextEdit();
        inSpell.setMaximumHeight(100)
        hIBox.addWidget(inSpell)
        
        
        updateStats = QtGui.QPushButton('Update',panel);
        updateStats.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold));
        self.connect(updateStats, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'));
        hIBox.addWidget(updateStats)
        
        
        v3Box.addLayout(hIBox)
        
        
        self.outputBox = QtGui.QTextEdit('Here the output:');
        self.outputBox.setMinimumHeight(250)
        v3Box.addWidget(self.outputBox)
        
        runSimulation = QtGui.QPushButton('Run Simulation',panel);
        runSimulation.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold));
        runSimulation.setMinimumHeight(50)
        self.connect(runSimulation, QtCore.SIGNAL('clicked()'), self.runSimulationWFRP);
        v3Box.addWidget(runSimulation)
        
        
        
        hBox.addLayout(v3Box)
        
        panel.setLayout(hBox)
        self.setCentralWidget(panel)

    def addFighterToActive(self):
        f=self.archiveListWidget.currentItem().text()
        print(f)
        if f is not None:
            src = "database/"+f+".yaml"
            ran = random.randint(0,100)
            dst = "fighters/"+f+"_"+str(ran)+".yaml"
            shutil.copyfile(src,dst)
            item = QtGui.QListWidgetItem(f+"_"+str(ran))
            self.fighterListWidget.addItem(item)
    
    def deleteFromActiveFighter(self):
        f=self.fighterListWidget.currentItem().text()
        print(f)
        if f is not None:
            src = "fighters/"+f+".yaml"
            os.remove(src)
            self.fighterListWidget.takeItem(self.fighterListWidget.currentRow())
    
    def runSimulationWFRP(self):
        out=wfrp.main()
        self.outputBox.setText(out)
        
app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
    

