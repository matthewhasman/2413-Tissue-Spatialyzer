#pragma once

#include <QtWidgets/QMainWindow>
#include "ui_TissueSpatialyzer.h"

class TissueSpatialyzer : public QMainWindow
{
    Q_OBJECT

public:
    TissueSpatialyzer(QWidget* parent = nullptr);
    ~TissueSpatialyzer();

private:
    Ui::TissueSpatialyzerClass ui;

};