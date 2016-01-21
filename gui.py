#!/usr/bin/python

import sys
import glob
import shutil
import os
import random
import wfrp
from PyQt4 import QtGui, QtCore
from config import *

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
        config = load_config_file()
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle('W.F.R.P - Simulator')
        self.resize(1024,768)
        panel = QtGui.QWidget(self)
        
        hBox = QtGui.QHBoxLayout()
        hBox.setSpacing(5)
        
        v1Box = QtGui.QVBoxLayout()
        v1Box.setSpacing(2)
        
        '''button = QtGui.QPushButton('Quit',cWidget);
        button.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold));
        self.connect(button, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'));'''
        
        
        #ADD LIST OF FIGHTER FROM DATABASE
        
        label = QtGui.QLabel('Database');
        v1Box.addWidget(label)
        
        self.archiveListWidget = QtGui.QListWidget()
        self.archiveListWidget.setMinimumWidth(200)
        lof = getFightersFromArchive()        
        for i in lof:
            item = QtGui.QListWidgetItem(i)
            self.archiveListWidget.addItem(item)
        v1Box.addWidget(self.archiveListWidget)
        
        addFighter = QtGui.QPushButton(config['LENG_ADD'],panel);
        addFighter.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold));
        self.connect(addFighter, QtCore.SIGNAL('clicked()'), self.addFighterToActive);
        v1Box.addWidget(addFighter)
        
        hBox.addLayout(v1Box)
        
        v2Box = QtGui.QVBoxLayout()
        v2Box.setSpacing(2)
        
        #ADD LIST OF FIGHTER FROM FIGHTERS FOLDER
        
        label = QtGui.QLabel(config['LENG_ACTIVE_FIGHTERS']);
        v2Box.addWidget(label)
        
        self.fighterListWidget = QtGui.QListWidget()
        #self.connect(self.fighterListWidget,QtCore.SIGNAL('itemClicked(QListWidgetItem *)'),self.loadFighterInfoToGuy);
        self.connect(self.fighterListWidget,QtCore.SIGNAL('itemSelectionChanged()'),self.loadFighterInfoToGuy);
        self.fighterListWidget.setMinimumWidth(200)
        lof = getFightersFromActive()
        for i in lof:
            item = QtGui.QListWidgetItem(i)
            self.fighterListWidget.addItem(item)      
        v2Box.addWidget(self.fighterListWidget)
        
        delete = QtGui.QPushButton(config['LENG_DELETE'],panel);
        self.connect(delete, QtCore.SIGNAL('clicked()'), self.deleteFromActiveFighter);
        delete.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold));
        v2Box.addWidget(delete)
        
        hBox.addLayout(v2Box)
        
        v3Box = QtGui.QVBoxLayout()
        v3Box.setSpacing(2)
        
        hIBox = QtGui.QVBoxLayout()
        hIBox.setSpacing(2)
        
        label = QtGui.QLabel(config['LENG_NAME']);
        label.setMaximumHeight(30)
        hIBox.addWidget(label)
        self.inName = QtGui.QLineEdit();
        self.inName.setMaximumHeight(30)
        hIBox.addWidget(self.inName)
        
        #PRIMARY LABEL
        
        primaryText = config['LENG_PRIMARY']
        primaryText = [primaryText[i:i+4] for i in range(0, len(primaryText), 4)]
        hPBox =QtGui.QHBoxLayout()
        hPBox.setSpacing(1)
        for i in range(8):
            label = QtGui.QLabel(primaryText[i])
            label.setMaximumWidth(400/8)
            label.setMaximumHeight(30)
            hPBox.addWidget(label)
        hIBox.addLayout(hPBox)
        
        #PRIMARY INPUT
        hPBox =QtGui.QHBoxLayout()
        hPBox.setSpacing(1)
        self.primaryInput=[]
        for i in range(8):
            inName = QtGui.QLineEdit();
            inName.setMaximumWidth(400/8)
            inName.setMaximumHeight(30)
            self.primaryInput.append(inName)
            hPBox.addWidget(inName)        
        hIBox.addLayout(hPBox)
        
        #SECONDARY LABEL
        secondaryText = config['LENG_SECONDARY']
        secondaryText = [secondaryText[i:i+4] for i in range(0, len(secondaryText), 4)]
        hPBox =QtGui.QHBoxLayout()
        hPBox.setSpacing(1)
        for i in range(8):
            label = QtGui.QLabel(secondaryText[i])
            label.setMaximumWidth(400/8)
            label.setMaximumHeight(30)
            hPBox.addWidget(label)
        hIBox.addLayout(hPBox)
        
        #SECONDARY INPUT
        hPBox =QtGui.QHBoxLayout()
        hPBox.setSpacing(1)
        self.secondaryInput=[]
        for i in range(8):
            inName = QtGui.QLineEdit();
            inName.setMaximumWidth(400/8)
            inName.setMaximumHeight(30)
            self.secondaryInput.append(inName)
            hPBox.addWidget(inName)        
        hIBox.addLayout(hPBox)
        
        line = QtGui.QFrame();
        line.setFrameShape(QtGui.QFrame.HLine);
        line.setFrameShadow(QtGui.QFrame.Sunken);
        hIBox.addWidget(line);
        
        #WEAPON SECTION
        hPBox =QtGui.QHBoxLayout()
        hPBox.setSpacing(1)
        
        label = QtGui.QLabel(config['LENG_NAME']);
        label.setMaximumWidth(400/4)
        hPBox.addWidget(label)
        
        label = QtGui.QLabel(config['LENG_KIND']);
        label.setMaximumWidth(400/4)
        hPBox.addWidget(label)
        
        label = QtGui.QLabel(config['LENG_FUNCTION']);
        label.setMaximumWidth(400/4)
        hPBox.addWidget(label)
        
        label = QtGui.QLabel(config['LENG_RELOAD']);
        label.setMaximumWidth(400/4)
        hPBox.addWidget(label)
        hIBox.addLayout(hPBox)
        
        hPBox =QtGui.QHBoxLayout()
        hPBox.setSpacing(1)
        
        self.inWeaponName = QtGui.QLineEdit();
        self.inWeaponName.setMaximumWidth(400/4)
        hPBox.addWidget(self.inWeaponName)
        
        self.inWeaponKind = QtGui.QComboBox();
        self.inWeaponKind.setMaximumWidth(400/4)
        self.inWeaponKind.addItem("sword")
        self.inWeaponKind.addItem("bow")        
        hPBox.addWidget(self.inWeaponKind)
        
        self.inWeaponFunction = QtGui.QLineEdit();
        self.inWeaponFunction.setMaximumWidth(400/4)
        hPBox.addWidget(self.inWeaponFunction)   
        
        self.inWeaponReload = QtGui.QLineEdit();
        self.inWeaponReload.setMaximumWidth(400/4)
        hPBox.addWidget(self.inWeaponReload) 
        
        hIBox.addLayout(hPBox)
        
        line = QtGui.QFrame();
        line.setFrameShape(QtGui.QFrame.HLine);
        line.setFrameShadow(QtGui.QFrame.Sunken);
        hIBox.addWidget(line);
        
        label = QtGui.QLabel(config['LENG_ARMOR']);
        hIBox.addWidget(label)
        
        self.inArmor = QtGui.QLineEdit();
        hIBox.addWidget(self.inArmor)
        
        line = QtGui.QFrame();
        line.setFrameShape(QtGui.QFrame.HLine);
        line.setFrameShadow(QtGui.QFrame.Sunken);
        hIBox.addWidget(line);
        
        label = QtGui.QLabel(config['LENG_FACTION']);
        hIBox.addWidget(label)
        
        self.inFaction = QtGui.QLineEdit();
        hIBox.addWidget(self.inFaction)
        
        line = QtGui.QFrame();
        line.setFrameShape(QtGui.QFrame.HLine);
        line.setFrameShadow(QtGui.QFrame.Sunken);
        hIBox.addWidget(line);
        
        self.cb_dodge = QtGui.QCheckBox(config["LENG_DODGE"], panel)
        self.cb_dodge.setChecked(False)
        hIBox.addWidget(self.cb_dodge)
        self.cb_fend = QtGui.QCheckBox(config["LENG_FEND"], panel)
        self.cb_fend.setChecked(False)
        hIBox.addWidget(self.cb_fend)
        self.cb_sharp = QtGui.QCheckBox(config["LENG_SHARPSHOOTER"], panel)
        self.cb_sharp.setChecked(False)
        hIBox.addWidget(self.cb_sharp)
        
        self.inSpell = QtGui.QTextEdit();
        self.inSpell.setMaximumHeight(100)
        hIBox.addWidget(self.inSpell)
        
        
        updateStats = QtGui.QPushButton(config['LENG_UPDATE'],panel);
        updateStats.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold));
        self.connect(updateStats, QtCore.SIGNAL('clicked()'), self.updateFighter);
        hIBox.addWidget(updateStats)
        
        v3Box.addLayout(hIBox)
        
        line = QtGui.QFrame();
        line.setFrameShape(QtGui.QFrame.HLine);
        label.setLineWidth(5);
        line.setFrameShadow(QtGui.QFrame.Sunken);
        v3Box.addWidget(line);
        
        self.outputBox = QtGui.QTextEdit('Here the output:');
        self.outputBox.setMinimumHeight(150)
        v3Box.addWidget(self.outputBox)
        
        runSimulation = QtGui.QPushButton(config['LENG_RUN'],panel);
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
        
    def loadFighterInfoToGuy(self):
        f=self.fighterListWidget.currentItem().text()
        src = "fighters/"+f+".yaml"
        fighter = wfrp.load_pg_from_file(src,uid=0)
        print(fighter)
        self.cb_dodge.setChecked(False)
        self.cb_fend.setChecked(False)
        self.cb_sharp.setChecked(False)
        
        self.inName.setText(fighter.nome.split(" - ")[1])
        self.primaryInput[0].setText(str(fighter.ac))
        self.primaryInput[1].setText(str(fighter.ab))
        self.primaryInput[2].setText(str(fighter.f))
        self.primaryInput[3].setText(str(fighter.r))
        self.primaryInput[4].setText(str(fighter.ag))
        self.primaryInput[5].setText(str(fighter.i))
        self.primaryInput[6].setText(str(fighter.vol))
        self.primaryInput[7].setText(str(fighter.sim))
        
        self.secondaryInput[0].setText(str(fighter.a))
        self.secondaryInput[1].setText(str(fighter.fe))
        self.secondaryInput[2].setText(str(fighter.bf))
        self.secondaryInput[3].setText(str(fighter.br))
        self.secondaryInput[4].setText(str(fighter.m))
        self.secondaryInput[5].setText(str(fighter.mag))
        self.secondaryInput[6].setText(str(fighter.fol))
        self.secondaryInput[7].setText(str(fighter.pf))
        
        self.inFaction.setText(fighter.fazione)
        
        self.inWeaponName.setText(fighter.arma.name)
        if(fighter.arma.kind=="sword"):
            self.inWeaponKind.setCurrentIndex(0)
        else:
            self.inWeaponKind.setCurrentIndex(1)
        self.inWeaponFunction.setText(fighter.arma.rawStrenght)
        self.inWeaponReload.setText(str(fighter.arma.reloadMax))
        
        self.inArmor.setText(str(fighter.armatura))
        
        self.cb_dodge.setChecked(not fighter.cantDodge)
        if(fighter.maxFend>0):
            self.cb_fend.setChecked(True)
        if(fighter.sharpshooter>10):
            self.cb_sharp.setChecked(True)
            
        spell=''    
        if(len(fighter.knowSpell)>0):
            for s in fighter.knowSpell:
                spell=spell + str(s) +"\n"
        self.inSpell.setText(spell)
    
    def updateFighter(self):
        f=self.fighterListWidget.currentItem().text()
        if f is not None:
            dst = "fighters/"+f+".yaml"
            output=''
            output+='name: \''+self.inName.text()+'\'\n'
            output+='primary: ['
            for p in self.primaryInput:
                output+=p.text()+','
            output=output[0:-1]+']\n'
            output+='secondary: ['
            for p in self.secondaryInput:
                output+=p.text()+','
            output=output[0:-1]+']\n'
            output+='weapon: [\''+self.inWeaponName.text()+'\',\''+str(self.inWeaponKind.currentText())+'\',\''+self.inWeaponFunction.text()+'\',\''+self.inWeaponReload.text()+'\']\n'
            output+='armor: '+self.inArmor.text()+'\n'
            output+='faction: \''+self.inFaction.text()+'\'\n'
            output+='skill: '
            b=False
            if(self.cb_dodge.isChecked()):
                b=True
                output+='\n'
                output+='- \'canDodge()\''
            
            if(self.cb_fend.isChecked()):
                b=True
                output+='\n'
                output+='- \'maxNumberOfFend(1)\''
            
            if(self.cb_sharp.isChecked()):
                b=True
                output+='\n'
                output+='- \'isSharpshooter()\''
            
            if(b==False):
                output+='[]\n'
            
            if(len(self.inSpell.toPlainText())>0):
                output+='- \'magic(['
                spell=str(self.inSpell.toPlainText())
                output+=spell.replace('\n','')+'])\'\n'
                #for s in spell:
                #    output+=s+','
                #output=output[0:-1]+'])\'\n'
            
            print(output)
            out_file = open(dst,"w")
            out_file.write(output)
            out_file.close()
            
        
        
        
app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
    

