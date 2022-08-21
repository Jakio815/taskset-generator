# A GUI program for task set generator.
# It helps to configure task sets to be generated, 
# and make graph to evaluate different schedulers.
#
# @author Yunsang Cho
# @author Hokeun Kim

import enum
from tasksets import BasicTaskSet, DagTaskSet
from plots import BasicPlot

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys
import os
import csv
from datetime import datetime

class TasksetGenerator(object):
    
    def __init__(self):
        self.config = {
            'schedulers': ['NP'],
            'type': 'basic',
            'timeout': {'value': 10, 'timeUnit': 'sec'},
            'min_workers': 1,
            'max_workers': 20,
            'deadline': {'value': 100, 'timeUnit': 'msec'}
        }
        self.basic_config = {
            'periodicity': 'sporadic',
            'period': {'value': 0, 'timeUnit': 'sec'},
            'num_tasks': 20,
            'utilization': 0.6,
            'seed': datetime.now()
        }
        self.dag_config = {
            'seed': int(round(datetime.now().timestamp())),
            'max_depth': 5,
            'num_outputs': 4,
            'execution_time': {'value': 100, 'timeUnit': 'msec'}
        }

    def setConfig(self, config) :
        configs = [self.config, self.basic_config, self.dag_config]

        for key, value in config.items():
            for c in configs:
                if key in c.keys():
                    c[key] = value
    
    # Generate taskset LF files to speicific directory.
    def makeLF(self, templateDir='./', outputDir='./'):
        TEMPLATE_PATH = f'{templateDir}/{self.config["type"].capitalize()}TaskSetGeneratorTemplate.lf'

        if not os.path.isfile(TEMPLATE_PATH):
            raise RuntimeError("No template file of task generator: " + TEMPLATE_PATH)
        if not os.path.exists(outputDir):
            # Create output directory if not exists.
            os.makedirs(outputDir)
            if not os.path.isdir(outputDir):
                raise RuntimeError("No output directory: " + outputDir)
        

        char_to_replace = {
            '$TOTAL_TIME$': f'{self.config["timeout"]["value"]} {self.config["timeout"]["timeUnit"]}'
        }   

        if self.config['type'] == 'basic':
            basic_taskset = BasicTaskSet.TaskSet(TEMPLATE_PATH=TEMPLATE_PATH)
            basic_taskset.setConfig(self.config)
            basic_taskset.setConfig(self.basic_config)
            generated_files = basic_taskset.makeLF(outputDir=outputDir)

        elif self.config['type'] == 'dag':
            dag_taskset = DagTaskSet.TaskSet(TEMPLATE_PATH=TEMPLATE_PATH)
            dag_taskset.setConfig(self.config)
            dag_taskset.setConfig(self.dag_config)
            generated_files = dag_taskset.makeLF(outputDir=outputDir)
        
        return generated_files
        

class Ui_MainWindow(object):

    def __init__(self):
        self.taskConfig = {
            'schedulers':[]
        }
    
    def setupUi(self, MainWindow):

        VerticalSize = 1024
        HorizontalSize = 660
        MainWindow.setWindowTitle('Taskset generator for LF schedulers')
        MainWindow.resize(VerticalSize, HorizontalSize)
        MainWindow.setMaximumWidth(VerticalSize)
        MainWindow.setMaximumHeight(HorizontalSize)
        MainWindow.setMinimumWidth(VerticalSize)
        MainWindow.setMinimumHeight(HorizontalSize)
        self.totalTimeUnit = "sec"
        self.periodTimeUnit = "sec"
        self.executionTimeUnit = "sec"

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.groupBox_scheduler = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_scheduler.setGeometry(QtCore.QRect(12, 12, 1000, 100))
        self.groupBox_scheduler.setObjectName("groupBox_scheduler")
        self.groupBox_scheduler.setTitle("Schedulers")

        self.label_scheduler = QtWidgets.QLabel(self.groupBox_scheduler)
        self.label_scheduler.setGeometry(QtCore.QRect(12, 32, 91, 25))
        self.label_scheduler.setObjectName("label_scheduler")
        self.label_scheduler.setText("Scheduler:")
        self.scheduler_NP = QtWidgets.QCheckBox(self.groupBox_scheduler)
        self.scheduler_NP.setGeometry(QtCore.QRect(120, 32, 40, 25))
        self.scheduler_NP.setObjectName('scheduler_NP')
        self.scheduler_NP.setText("NP")
        self.scheduler_GEDF_NP = QtWidgets.QCheckBox(self.groupBox_scheduler)
        self.scheduler_GEDF_NP.setGeometry(QtCore.QRect(180, 32, 100, 25))
        self.scheduler_GEDF_NP.setObjectName('scheduler_GEDF_NP')
        self.scheduler_GEDF_NP.setText("GEDF_NP")
        self.scheduler_GEDF_NP_CI = QtWidgets.QCheckBox(self.groupBox_scheduler)
        self.scheduler_GEDF_NP_CI.setGeometry(QtCore.QRect(280, 32, 120, 25))
        self.scheduler_GEDF_NP_CI.setObjectName('scheduler_GEDF_NP_CI')
        self.scheduler_GEDF_NP_CI.setText("GEDF_NP_CI")
        self.scheduler_adaptive = QtWidgets.QCheckBox(self.groupBox_scheduler)
        self.scheduler_adaptive.setGeometry(QtCore.QRect(400, 32, 145, 25))
        self.scheduler_adaptive.setObjectName('scheduler_adaptive')
        self.scheduler_adaptive.setText("adaptive")

        self.groupBox_generalConfiguration = QtWidgets.QGroupBox(self.centralwidget)              # General Config
        self.groupBox_generalConfiguration.setGeometry(QtCore.QRect(12, 122, 1000, 100))
        self.groupBox_generalConfiguration.setObjectName("groupBox_generalConfiguration")
        self.groupBox_generalConfiguration.setTitle("General Configuration")

        self.label_numOfIterations = QtWidgets.QLabel(self.groupBox_generalConfiguration)
        self.label_numOfIterations.setGeometry(QtCore.QRect(12, 32, 180, 25))
        self.label_numOfIterations.setObjectName("label_numOfIterations")
        self.label_numOfIterations.setText("Number of Iterations:")
        self.spinBox_numOfIterations = QtWidgets.QSpinBox(self.groupBox_generalConfiguration)
        self.spinBox_numOfIterations.setGeometry(QtCore.QRect(200, 32, 55, 25))
        self.spinBox_numOfIterations.setMaximum(100)
        self.spinBox_numOfIterations.setMinimum(1)
        self.spinBox_numOfIterations.setProperty('value', 1)
        self.spinBox_numOfIterations.setObjectName('spinBox_numOfIterations')
        
        self.label_deadline = QtWidgets.QLabel(self.groupBox_generalConfiguration)
        self.label_deadline.setGeometry(QtCore.QRect(12, 60, 180, 25))
        self.label_deadline.setObjectName("label_deadline")
        self.label_deadline.setText("Deadline:")

        self.spinBox_deadline = QtWidgets.QSpinBox(self.groupBox_generalConfiguration)
        self.spinBox_deadline.setGeometry(QtCore.QRect(200, 60, 55, 25))
        self.spinBox_deadline.setObjectName('spinBox_deadline')
        self.spinBox_deadline.setMaximum(10000)
        self.spinBox_deadline.setMinimum(1)
        self.spinBox_deadline.setProperty('value', 1)

        self.comboBox_deadlineUnit = QtWidgets.QComboBox(self.groupBox_generalConfiguration)
        self.comboBox_deadlineUnit.setGeometry(QtCore.QRect(270, 60, 55, 25))
        self.comboBox_deadlineUnit.setObjectName('comboBox_deadlineUnit')
        self.comboBox_deadlineUnit.addItems(['sec', 'msec', 'usec', 'nsec'])
        self.comboBox_deadlineUnit.currentIndexChanged.connect(lambda: self.selectionchange(self.comboBox_deadlineUnit, 'deadlineUnit'))

        self.groupBox_taskConfiguration = QtWidgets.QGroupBox(self.centralwidget)               # Task Config
        self.groupBox_taskConfiguration.setGeometry(QtCore.QRect(12, 232, 1000, 228))
        self.groupBox_taskConfiguration.setObjectName("groupBox_taskConfiguration")
        self.groupBox_taskConfiguration.setTitle("Task Configuration")

        self.tab_task = QtWidgets.QTabWidget(self.groupBox_taskConfiguration)
        self.tab_task.setGeometry(QtCore.QRect(1, 21, 999, 207))
        self.tab_task.setObjectName("tab_task")

        self.scrollArea_task_basic = QtWidgets.QScrollArea(self.tab_task)
        self.scrollArea_task_basic.setWidgetResizable(True)
        self.scrollArea_task_basic.setGeometry(QtCore.QRect(0, 0, 999, 208))
        self.scrollArea_task_basic.setObjectName("scrollArea_task_basic")
        self.scrollArea_task_basic.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea_task_basic.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scrollAreaWidgetContents_basic = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_basic.setObjectName('scrollAreaWidgetContents_basic')
        
        self.gridLayoutWidget_basic = QtWidgets.QWidget(self.scrollAreaWidgetContents_basic)
        self.gridLayoutWidget_basic.setObjectName("gridLayoutWidget_basic")

        self.gridLayout_basic = QtWidgets.QGridLayout(self.gridLayoutWidget_basic)
        self.gridLayout_basic.setObjectName("gridLayout_basic")

        self.scrollArea_task_basic.setWidget(self.scrollAreaWidgetContents_basic)
        self.scrollAreaWidgetContents_basic.setLayout(self.gridLayout_basic)   
        
        self.tab_task.addTab(self.scrollArea_task_basic, "Basic")

        self.label_periodicity = QtWidgets.QLabel(self.gridLayoutWidget_basic)
        self.label_periodicity.setObjectName("label_periodicity")
        self.label_periodicity.setText("Periodicity:")
        self.label_periodicity.setToolTip("Periodicity of the task: Sporadic/Periodic")
        self.gridLayout_basic.addWidget(self.label_periodicity, 0, 0)
        
        self.comboBox_periodicity = QtWidgets.QComboBox(self.gridLayoutWidget_basic)
        self.comboBox_periodicity.setObjectName("comboBox_periodicity")
        self.comboBox_periodicity.addItems(["sporadic", "periodic"])
        self.comboBox_periodicity.currentIndexChanged.connect(lambda: self.selectionchange(self.comboBox_periodicity, 'periodicity'))
        self.gridLayout_basic.addWidget(self.comboBox_periodicity, 0, 1)
        
        self.label_numOfTasks = QtWidgets.QLabel(self.gridLayoutWidget_basic)
        self.label_numOfTasks.setObjectName("label_numOfTasks")
        self.label_numOfTasks.setText("Number of tasks:")
        self.label_numOfTasks.setToolTip("Number of tasks")
        self.gridLayout_basic.addWidget(self.label_numOfTasks, 1, 0)
        
        self.spinBox_numOfTasks = QtWidgets.QSpinBox(self.gridLayoutWidget_basic)
        self.spinBox_numOfTasks.setObjectName('spinBox_numOfTasks')
        self.spinBox_numOfTasks.setMaximum(100)
        self.spinBox_numOfTasks.setMinimum(1)
        self.spinBox_numOfTasks.setProperty('value', 1)
        self.gridLayout_basic.addWidget(self.spinBox_numOfTasks, 1, 1)

        self.label_totalTime = QtWidgets.QLabel(self.gridLayoutWidget_basic)
        self.label_totalTime.setObjectName("label_totalTime")
        self.label_totalTime.setText("Total time:")
        self.label_totalTime.setToolTip("Total time")
        self.gridLayout_basic.addWidget(self.label_totalTime, 2, 0)

        self.spinBox_totalTime = QtWidgets.QSpinBox(self.gridLayoutWidget_basic)
        self.spinBox_totalTime.setObjectName('spinBox_totalTime')
        self.spinBox_totalTime.setMaximum(10000)
        self.spinBox_totalTime.setMinimum(1)
        self.spinBox_totalTime.setProperty('value', 1)
        self.gridLayout_basic.addWidget(self.spinBox_totalTime, 2, 1)

        self.comboBox_totalTimeUnit = QtWidgets.QComboBox(self.gridLayoutWidget_basic)
        self.comboBox_totalTimeUnit.setObjectName('comboBox_totalTimeUnit')
        self.comboBox_totalTimeUnit.addItems(['sec', 'msec', 'usec', 'nsec'])
        self.comboBox_totalTimeUnit.currentIndexChanged.connect(lambda: self.selectionchange(self.comboBox_totalTimeUnit, 'totalTimeUnit'))
        self.gridLayout_basic.addWidget(self.comboBox_totalTimeUnit, 2, 2)

        self.label_utilization = QtWidgets.QLabel(self.gridLayoutWidget_basic)
        self.label_utilization.setObjectName("label_utilization")
        self.label_utilization.setText("Utilization:")
        self.label_utilization.setToolTip("Utilization")
        self.gridLayout_basic.addWidget(self.label_utilization, 3, 0)

        self.lineEdit_utilization = QtWidgets.QLineEdit(self.gridLayoutWidget_basic)
        self.lineEdit_utilization.setObjectName('lineEdit_utilization')
        self.lineEdit_utilization.setText('0.4')
        self.gridLayout_basic.addWidget(self.lineEdit_utilization, 3, 1)

        self.label_basic_seed = QtWidgets.QLabel(self.gridLayoutWidget_basic)
        self.label_basic_seed.setObjectName("label_basic_seed")
        self.label_basic_seed.setText("Seed:")
        self.label_basic_seed.setToolTip("Seed value to initialize random function")
        self.gridLayout_basic.addWidget(self.label_basic_seed, 4, 0)

        self.lineEdit_basic_seed = QtWidgets.QLineEdit(self.gridLayoutWidget_basic)
        self.lineEdit_basic_seed.setObjectName('lineEdit_basic_seed')
        self.gridLayout_basic.addWidget(self.lineEdit_basic_seed, 4, 1)

        self.label_period = QtWidgets.QLabel(self.gridLayoutWidget_basic)
        self.label_period.setObjectName("label_period")
        self.label_period.setText("Period:")
        self.label_period.setToolTip("Period for each task")
        self.gridLayout_basic.addWidget(self.label_period, 4, 0)

        self.spinBox_period = QtWidgets.QSpinBox(self.gridLayoutWidget_basic)
        self.spinBox_period.setObjectName('spinBox_period')
        self.spinBox_period.setMaximum(10000)
        self.spinBox_period.setMinimum(1)
        self.spinBox_period.setProperty('value', 1)
        self.gridLayout_basic.addWidget(self.spinBox_period, 4, 1)

        self.comboBox_periodTimeUnit = QtWidgets.QComboBox(self.gridLayoutWidget_basic)
        self.comboBox_periodTimeUnit.setObjectName('comboBox_periodTimeUnit')
        self.comboBox_periodTimeUnit.addItems(['sec', 'msec', 'usec', 'nsec'])
        self.comboBox_periodTimeUnit.currentIndexChanged.connect(lambda: self.selectionchange(self.comboBox_periodTimeUnit, 'periodTimeUnit'))
        self.gridLayout_basic.addWidget(self.comboBox_periodTimeUnit, 4, 2)

        self.label_period.hide()
        self.spinBox_period.hide() 
        self.comboBox_periodTimeUnit.hide()

        self.scrollArea_task_dag = QtWidgets.QScrollArea(self.tab_task)
        self.scrollArea_task_dag.setWidgetResizable(True)
        self.scrollArea_task_dag.setGeometry(QtCore.QRect(0, 0, 999, 208))
        self.scrollArea_task_dag.setObjectName("scrollArea_task_dag")
        self.scrollArea_task_dag.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea_task_dag.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scrollAreaWidgetContents_dag = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_dag.setObjectName('scrollAreaWidgetContents_dag')

        self.gridLayoutWidget_dag = QtWidgets.QWidget(self.scrollAreaWidgetContents_dag)
        self.gridLayoutWidget_dag.setObjectName("gridLayoutWidget_dag")

        self.gridLayout_dag = QtWidgets.QGridLayout(self.gridLayoutWidget_dag)
        self.gridLayout_dag.setObjectName("gridLayout_dag")

        self.scrollArea_task_dag.setWidget(self.scrollAreaWidgetContents_dag)
        self.scrollAreaWidgetContents_dag.setLayout(self.gridLayout_dag)

        self.tab_task.addTab(self.scrollArea_task_dag, "DAG")
        
        self.label_numOfLevel = QtWidgets.QLabel(self.gridLayoutWidget_dag)
        self.label_numOfLevel.setObjectName("label_numOfLevel")
        self.label_numOfLevel.setText("Number of level:")
        self.label_numOfLevel.setToolTip("Number of level")
        self.gridLayout_dag.addWidget(self.label_numOfLevel, 0, 0)

        self.spinBox_numOfLevel = QtWidgets.QSpinBox(self.gridLayoutWidget_dag)
        self.spinBox_numOfLevel.setObjectName('spinBox_numOfLevel')
        self.spinBox_numOfLevel.setMaximum(30)
        self.spinBox_numOfLevel.setMinimum(1)
        self.spinBox_numOfLevel.setProperty('value', 1)
        self.gridLayout_dag.addWidget(self.spinBox_numOfLevel, 0, 1)
    
        self.label_capacityOfOneLevel = QtWidgets.QLabel(self.gridLayoutWidget_dag)
        self.label_capacityOfOneLevel.setObjectName("label_capacityOfOneLevel")
        self.label_capacityOfOneLevel.setText("Maximum number of components in one level:")
        self.label_capacityOfOneLevel.setToolTip("Number of level")
        self.gridLayout_dag.addWidget(self.label_capacityOfOneLevel, 1, 0)

        self.spinBox_capacityOfOneLevel = QtWidgets.QSpinBox(self.gridLayoutWidget_dag)
        self.spinBox_capacityOfOneLevel.setObjectName('spinBox_capacityOfOneLevel')
        self.spinBox_capacityOfOneLevel.setMaximum(30)
        self.spinBox_capacityOfOneLevel.setMinimum(1)
        self.spinBox_capacityOfOneLevel.setProperty('value', 1)
        self.gridLayout_dag.addWidget(self.spinBox_capacityOfOneLevel, 1, 1)
        
        self.label_dag_seed = QtWidgets.QLabel(self.gridLayoutWidget_dag)
        self.label_dag_seed.setObjectName("label_dag_seed")
        self.label_dag_seed.setText("Seed:")
        self.label_dag_seed.setToolTip("Seed value to initialize random function")
        self.gridLayout_dag.addWidget(self.label_dag_seed, 2, 0)

        self.lineEdit_dag_seed = QtWidgets.QLineEdit(self.gridLayoutWidget_dag)
        self.lineEdit_dag_seed.setObjectName('lineEdit_dag_seed')
        self.gridLayout_dag.addWidget(self.lineEdit_dag_seed, 2, 1)
        
        self.label_executionTime = QtWidgets.QLabel(self.gridLayoutWidget_dag)
        self.label_executionTime.setObjectName("label_executionTime")
        self.label_executionTime.setText("Execution time of each component:")
        self.label_executionTime.setToolTip("Execution time of one component")
        self.gridLayout_dag.addWidget(self.label_executionTime, 3, 0)

        self.spinBox_executionTime = QtWidgets.QSpinBox(self.gridLayoutWidget_dag)
        self.spinBox_executionTime.setObjectName('spinBox_executionTime')
        self.spinBox_executionTime.setMaximum(10000)
        self.spinBox_executionTime.setMinimum(1)
        self.spinBox_executionTime.setProperty('value', 1)
        self.gridLayout_dag.addWidget(self.spinBox_executionTime, 3, 1)
            
        self.comboBox_executionTimeUnit = QtWidgets.QComboBox(self.gridLayoutWidget_dag)
        self.comboBox_executionTimeUnit.setObjectName('comboBox_executionTimeUnit')
        self.comboBox_executionTimeUnit.addItems(['sec', 'msec', 'usec', 'nsec'])
        self.comboBox_executionTimeUnit.currentIndexChanged.connect(lambda: self.selectionchange(self.comboBox_executionTimeUnit, 'executionTimeUnit'))
        self.gridLayout_dag.addWidget(self.comboBox_executionTimeUnit, 3, 2)

        self.run = QtWidgets.QPushButton(self.centralwidget)
        self.run.setToolTip('Button to run the settings')
        self.run.setGeometry(QtCore.QRect(12, 610, 200, 25))
        self.run.setObjectName("run")
        self.run.setText("Run")

        self.exit = QtWidgets.QPushButton(self.centralwidget)
        self.exit.setToolTip('Exit the framework')
        self.exit.setGeometry(QtCore.QRect(812, 610, 200, 25))
        self.exit.setObjectName('exit')
        self.exit.setText('Exit')

        MainWindow.setCentralWidget(self.centralwidget)
        self.run.clicked.connect(self.clickRun)
        self.exit.clicked.connect(self.clickExit)
        
    def selectionchange(self, comboBox, type):
        if type == 'periodicity':
            if comboBox.currentText() == 'sporadic':
                self.label_basic_seed.show()
                self.lineEdit_basic_seed.show()
                self.label_period.hide()
                self.spinBox_period.hide()
                self.comboBox_periodTimeUnit.hide()
            elif comboBox.currentText() == 'periodic':
                self.label_basic_seed.hide()
                self.lineEdit_basic_seed.hide()
                self.label_period.show()
                self.spinBox_period.show()
                self.comboBox_periodTimeUnit.show()
        elif type == 'totalTimeUnit':
            self.totalTimeUnit = comboBox.currentText()
        elif type == 'executionTimeUnit':
            self.executionTimeUnit = comboBox.currentText()
        elif type == 'periodTimeUnit':
            self.periodTimeUnit = comboBox.currentText()
    
    def clickRun(self):
        try:
            self.Run()
        except RuntimeError as err:
            print("Python Error: {0}".format(err), file=sys.stderr)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Python Error")
            msg.setText("{0}".format(err))
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def Run(self):
        # Set data
        self.__updateConfig()
        if len(self.taskConfig['schedulers']) == 0:
            raise RuntimeError("Choose scheduler to evaluate")
        else:

            WORKING_DIR = os.getcwd()

            generator = TasksetGenerator()
            generator.setConfig(self.taskConfig)
            generated_files = generator.makeLF(templateDir=f'{WORKING_DIR}/templates', outputDir=f'{WORKING_DIR}/.gui/src/')
            print("Finished generating LF files!")
            
            plot_title = ''
            if self.taskConfig['type'] == 'basic':
                plot_title = f'{self.taskConfig["periodicity"].capitalize()} / Number of task: {self.taskConfig["num_tasks"]} / Utilization: {self.taskConfig["utilization"]}'
            elif self.taskConfig['type'] == 'dag':
                plot_title = f'DAG / Seed: {self.taskConfig["seed"]}'
            plot_generator = BasicPlot.PlotGenerator()
            plot_generator.setConfig({
                'title': plot_title,
                'dataset': generated_files,
                'num_iteration': self.spinBox_numOfIterations.value()
            })

            exe_times, deadline_misses = plot_generator.plot_graph()
            result = {
                'workers': [i for i in range(1, 21)],
                'exe_times': exe_times,
                'deadline_misses': deadline_misses
            }

            self.saveResult(result)


    def clickExit(self):
        app.quit()

    def __updateConfig(self):

        schedulers = {
            self.scheduler_NP: 'NP',
            self.scheduler_GEDF_NP: 'GEDF_NP',
            self.scheduler_GEDF_NP_CI: 'GEDF_NP_CI',
            self.scheduler_adaptive: 'adaptive'
        }

        self.taskConfig['schedulers'].clear()

        for key, value in schedulers.items():
            if key.isChecked():
                self.taskConfig['schedulers'].append(value)
            
        self.taskConfig['type'] = self.tab_task.currentWidget().objectName().split('_')[-1]
        self.taskConfig['timeout'] = {
            'value': self.spinBox_totalTime.value(),
            'timeUnit': self.comboBox_totalTimeUnit.currentText()
        }

        # FIXME: Should add spinboxs for min_workers and max_workers in GUI.
        self.taskConfig['min_workers'] = 1
        self.taskConfig['max_workers'] = 20
        self.taskConfig['deadline'] = {
            'value': self.spinBox_deadline.value(),
            'timeUnit': self.comboBox_deadlineUnit.currentText()
        }

        if self.taskConfig['type'] == 'basic':
            self.taskConfig['periodicity'] = self.comboBox_periodicity.currentText()
            self.taskConfig['period'] = {
               'value': self.spinBox_period.value(),
               'timeUnit': self.periodTimeUnit,
            }
            self.taskConfig['num_tasks'] = self.spinBox_numOfTasks.value()
            self.taskConfig['utilization'] = float(self.lineEdit_utilization.text())
            self.taskConfig['seed'] = int(self.lineEdit_basic_seed.text()) if len(self.lineEdit_basic_seed.text()) > 0 else int(round(datetime.now().timestamp()))
        elif self.taskConfig['type'] == 'dag':
            self.taskConfig['seed'] = int(self.lineEdit_dag_seed.text()) if len(self.lineEdit_dag_seed.text()) > 0 else datetime.now()
            self.taskConfig['max_depth'] = self.spinBox_numOfLevel.value()
            self.taskConfig['num_outputs'] = self.spinBox_capacityOfOneLevel.value()
            self.taskConfig['execution_time'] = {
                'value': self.spinBox_executionTime.value(),
                'timeUnit': self.comboBox_executionTimeUnit.currentText()
            }    
    
    def saveResult(self, result):
        WORKING_DIR = os.getcwd()
        output_dir = f'{WORKING_DIR}/.output'
        if os.path.exists(output_dir) == False:
            os.mkdir(output_dir)
        
        if self.taskConfig['type'] == 'basic':
            header = ['type', 'number of iterations', 'deadline', 'schedulers', 'number of tasks', 'total time', 'utilization', 'periodicity']
            configs = ['basic', self.spinBox_numOfIterations.value(), f'{self.taskConfig["deadline"]["value"]} {self.taskConfig["deadline"]["timeUnit"]}', 
                        ', '.join(self.taskConfig['schedulers']), self.taskConfig['num_tasks'], f'{self.taskConfig["timeout"]["value"]} {self.taskConfig["timeout"]["timeUnit"]}',
                        self.taskConfig['utilization'], self.taskConfig['periodicity']
                      ]
            if self.taskConfig['periodicity'] == 'sporadic':
                header.append('seed')
                configs.append(self.taskConfig['seed'])
            elif self.taskConfig['periodicity'] == 'periodic':
                header.append('period')
                configs.append(f'{self.taskConfig["period"]["value"]} {self.taskConfig["period"]["timeUnit"]}')

        elif self.taskConfig['type'] == 'dag':
            header = ['type', 'number of iterations', 'deadline', 'schedulers', 'number of level', 'maximum components in each level', 'seed', 'execution time']
            configs = ['dag', self.spinBox_numOfIterations.value(), f'{self.taskConfig["deadline"]["value"]} {self.taskConfig["deadline"]["timeUnit"]}', 
                        ', '.join(self.taskConfig['schedulers']), self.taskConfig['max_depth'], self.taskConfig['num_outputs'], self.taskConfig['seed'],
                        f'{self.taskConfig["execution_time"]["value"]} {self.taskConfig["execution_time"]["timeUnit"]}'
                      ]

        output_file = f'{output_dir}/{self.taskConfig["type"]}_{", ".join(self.taskConfig["schedulers"])}_{int(round(datetime.now().timestamp()))}.csv'
        
        with open(output_file, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            writer.writerow(header)
            writer.writerow(configs)


            outputs_header = ['scheduler', 'worker', 'physical execution time', 'deadline miss']
            outputs = []

            for scheduler in self.taskConfig['schedulers']:
                for i, worker in enumerate(result['workers']):
                    output = [scheduler, worker, result['exe_times'][scheduler][i], result['deadline_misses'][scheduler][i]]
                    outputs.append(output.copy())
                    output.clear()
            
            writer.writerow(outputs_header)
            writer.writerows(outputs)
                


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.statusBar().showMessage('Ready')
    MainWindow.show()
    sys.exit(app.exec_())
