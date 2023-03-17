#include "dialogpyqtexemple.h"
#include "ui_dialogpyqtexemple.h"

DialogPyqtExemple::DialogPyqtExemple(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::DialogPyqtExemple)
{
    ui->setupUi(this);
}

DialogPyqtExemple::~DialogPyqtExemple()
{
    delete ui;
}
