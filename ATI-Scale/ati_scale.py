import sys, os
from PyQt5 import QtWidgets, uic

UI_FILE = "ati.ui"
LOG_DIRECTORY = "log/"
LIKERT_SCALE_SIZE = 6
NUM_ITEMS = 9
INVERSION_ITEMS = [3, 6, 8]


class Item:
    def __init__(self, _id, value):
        self.id = _id
        self.set_value(value)

    def set_value(self, value):
        self.value = value
        self.__check_inversion(value)

    def __check_inversion(self, value):
        if value != -1:
            if self.id in INVERSION_ITEMS:
                self.value = LIKERT_SCALE_SIZE - value + 1

    def __repr__(self):
        return f"Item with id={self.id} and value={self.value}"


class ATI_Scale(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.pid = sys.argv[1]
        self.items = [Item(i + 1, -1) for i in range(NUM_ITEMS)]

        self.init_ui()

    def init_ui(self):
        self.ui = uic.loadUi(UI_FILE, self)

        for i in range(NUM_ITEMS):
            for k in range(LIKERT_SCALE_SIZE):
                eval(f"self.ui.i{i + 1}cb{k + 1}.clicked.connect(lambda x: self.handle_button_click({i}, {k + 1}, x))", locals())

        self.ui.btn_ok.clicked.connect(self.evaluate)

        self.ui.show()

    def handle_button_click(self, item, cb, value):
        if value:
            self.uncheck_cbs_item_except(item + 1, cb)
            self.items[item].set_value(cb)
        else:
            self.items[item].set_value(-1)

        self.toggle_ok_button()

    def uncheck_cbs_item_except(self, item, cb):
        for i in range(1, LIKERT_SCALE_SIZE + 1):
            eval(f"self.ui.i{item}cb{i}.setChecked(False)", locals())
        eval(f"self.ui.i{item}cb{cb}.setChecked(True)", locals())

    def toggle_ok_button(self):
        self.ui.btn_ok.setEnabled(-1 not in [item.value for item in self.items])

    def evaluate(self):
        ati_score = sum([item.value for item in self.items]) / NUM_ITEMS

        if not os.path.exists(LOG_DIRECTORY):
            os.mkdir(LOG_DIRECTORY)

        if not os.path.exists(LOG_DIRECTORY + "ati_scores.csv"):
            f = open(f"{LOG_DIRECTORY}ati_scores.csv", mode="w")
            print("pid,ati_means,item1,item2,item3,item4,item5,item6,item7,item8,item9", file=f)
        else:
            f = open(f"{LOG_DIRECTORY}ati_scores.csv", mode="a+")

        item1, item2, item3, item4, item5, item6, item7, item8, item9 = [item.value for item in self.items]

        print(f"{self.pid},{ati_score},{item1},{item2},{item3},{item4},{item5},{item6},{item7},{item8},{item9}", file=f)
        f.close()
        exit(0)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 ati_scale.py <pid>")
        sys.exit(-1)

    app = QtWidgets.QApplication(sys.argv)
    ATI_Scale()
    sys.exit(app.exec_())
