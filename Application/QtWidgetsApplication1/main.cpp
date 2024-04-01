#include "TissueSpatialyzer.h"
#include <QtWidgets/QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    TissueSpatialyzer w;
    w.show();
    return a.exec();
}
