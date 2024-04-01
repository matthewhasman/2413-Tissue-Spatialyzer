/********************************************************************************
** Form generated from reading UI file 'TissueSpatialyzer.ui'
**
** Created by: Qt User Interface Compiler version 6.6.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_TISSUESPATIALYZER_H
#define UI_TISSUESPATIALYZER_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_TissueSpatialyzerClass
{
public:
    QWidget *centralWidget;
    QWidget *widget;
    QVBoxLayout *verticalLayout;
    QPushButton *run_button;
    QPushButton *calibration_button;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *TissueSpatialyzerClass)
    {
        if (TissueSpatialyzerClass->objectName().isEmpty())
            TissueSpatialyzerClass->setObjectName("TissueSpatialyzerClass");
        TissueSpatialyzerClass->resize(814, 529);
        centralWidget = new QWidget(TissueSpatialyzerClass);
        centralWidget->setObjectName("centralWidget");
        widget = new QWidget(centralWidget);
        widget->setObjectName("widget");
        widget->setGeometry(QRect(210, 60, 401, 351));
        verticalLayout = new QVBoxLayout(widget);
        verticalLayout->setSpacing(6);
        verticalLayout->setContentsMargins(11, 11, 11, 11);
        verticalLayout->setObjectName("verticalLayout");
        verticalLayout->setContentsMargins(0, 0, 0, 0);
        run_button = new QPushButton(widget);
        run_button->setObjectName("run_button");
        run_button->setEnabled(false);
        QFont font;
        font.setPointSize(22);
        run_button->setFont(font);

        verticalLayout->addWidget(run_button);

        calibration_button = new QPushButton(widget);
        calibration_button->setObjectName("calibration_button");
        calibration_button->setFont(font);

        verticalLayout->addWidget(calibration_button);

        TissueSpatialyzerClass->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(TissueSpatialyzerClass);
        menuBar->setObjectName("menuBar");
        menuBar->setGeometry(QRect(0, 0, 814, 22));
        TissueSpatialyzerClass->setMenuBar(menuBar);
        mainToolBar = new QToolBar(TissueSpatialyzerClass);
        mainToolBar->setObjectName("mainToolBar");
        TissueSpatialyzerClass->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(TissueSpatialyzerClass);
        statusBar->setObjectName("statusBar");
        TissueSpatialyzerClass->setStatusBar(statusBar);

        retranslateUi(TissueSpatialyzerClass);

        QMetaObject::connectSlotsByName(TissueSpatialyzerClass);
    } // setupUi

    void retranslateUi(QMainWindow *TissueSpatialyzerClass)
    {
        TissueSpatialyzerClass->setWindowTitle(QCoreApplication::translate("TissueSpatialyzerClass", "TissueSpatialyzer", nullptr));
        run_button->setText(QCoreApplication::translate("TissueSpatialyzerClass", "Run Experiment", nullptr));
        calibration_button->setText(QCoreApplication::translate("TissueSpatialyzerClass", "Calibration", nullptr));
    } // retranslateUi

};

namespace Ui {
    class TissueSpatialyzerClass: public Ui_TissueSpatialyzerClass {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_TISSUESPATIALYZER_H
