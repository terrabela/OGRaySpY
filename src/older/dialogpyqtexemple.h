#ifndef DIALOGPYQTEXEMPLE_H
#define DIALOGPYQTEXEMPLE_H

#include <QDialog>

namespace Ui {
class DialogPyqtExemple;
}

class DialogPyqtExemple : public QDialog
{
    Q_OBJECT
    
public:
    explicit DialogPyqtExemple(QWidget *parent = 0);
    ~DialogPyqtExemple();
    
private:
    Ui::DialogPyqtExemple *ui;
};

#endif // DIALOGPYQTEXEMPLE_H
