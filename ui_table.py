from datetime import datetime
from time import sleep
from typing import List

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QObject, QThread, pyqtSignal

from philosopher import ForkStatus, Philosopher, PhilosopherStatus


# Main Thread
class Worker(QObject):
    finished = pyqtSignal()
    test = pyqtSignal()
    update_screen = pyqtSignal(list, list)
    console_log = pyqtSignal(str)

    # variables
    fork_list: List[ForkStatus] = []
    philosopher_list: List[Philosopher] = []

    def run(self):
        # initialize the variables
        self.fork_list = [
            ForkStatus.FREE,
            ForkStatus.FREE,
            ForkStatus.FREE,
            ForkStatus.FREE,
        ]

        self.philosopher_list = [
            Philosopher(
                name="Philo. " + str(index + 1),
                table_position=index,
                fork_list=self.fork_list,
                func_log_signal=self.console_log,
            )
            for index in range(4)
        ]

        # start the threads
        for philosopher in self.philosopher_list:
            philosopher.start()

        # update table
        self.update_screen.emit(self.fork_list, self.philosopher_list)

        while (
            all([philo.status for philo in self.philosopher_list])
            != PhilosopherStatus.DONE
        ):
            sleep(0.5)
            self.update_screen.emit(self.fork_list, self.philosopher_list)

        self.finished.emit()


# Page view
class TableView(QtWidgets.QWidget):
    # UI elements
    ui_window = uic.loadUi("ui_table.ui")
    console_text = None
    btn_run_test = None

    # Thread
    worker = None
    thread = None

    fork_label_list = []
    philosopher_label_list = []

    def __init__(self):
        super(TableView, self).__init__()

        self._setup_ui_elements()
        self.ui_window.show()

    def main_code(self):
        """
        The main code is here
        :return: None
        """
        self.thread = QThread()
        self.worker = Worker()

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.console_log.connect(self.console_log)
        self.worker.update_screen.connect(self.update_table)

        self.thread.start()

    def console_log(self, message_log: str):
        """
        Print the log on the screen
        :param message_log: string to print
        :return:
        """
        now = datetime.now()
        _log = self.console_text.toPlainText()
        _log = now.strftime("%d/%m, %H:%M:%S") + " ==> " + message_log + "\n" + _log
        self.console_text.setText(_log)

    def clear_log(self):
        """
        Clear the screen
        :return:
        """
        self.console_text.setText("")

    def update_table(
        self, fork_list: list[ForkStatus], philosopher_list: list[Philosopher]
    ):
        """
        Update forks and philosophers on the table
        :param fork_list:
        :param philosopher_list:
        :return:
        """
        self._update_fork_labels(fork_list=fork_list)
        self._update_philosopher_labels(philosopher_list=philosopher_list)

    def _update_fork_labels(self, fork_list: list[ForkStatus]):
        """
        Update the color of the fork labels
        :return:
        """
        for index, fork_status in enumerate(fork_list):
            if fork_status == ForkStatus.IN_USE:
                self.fork_label_list[index].setStyleSheet("color: #d36200;")
            else:
                self.fork_label_list[index].setStyleSheet("color: #55aa00;")
        pass

    def _update_philosopher_labels(self, philosopher_list: list[Philosopher]):
        """
        Update the color of the philosopher labels
        :return:
        """
        for index, philo_status in enumerate(philosopher_list):
            if philo_status.status == PhilosopherStatus.THINKING:
                self.philosopher_label_list[index].setStyleSheet("color: #55aa00;")

            elif philo_status.status == PhilosopherStatus.HUNGRY:
                self.philosopher_label_list[index].setStyleSheet("color: #aa0000;")

            elif philo_status.status == PhilosopherStatus.EATING:
                self.philosopher_label_list[index].setStyleSheet("color: #d36200;")

            else:  # eating
                self.philosopher_label_list[index].setStyleSheet("color: black;")
        pass

    def _setup_ui_elements(self):
        """
        Get UI elements
        :return:
        """
        # get ui elements
        self.btn_run_test = self.ui_window.btn_run_test
        btn_clear = self.ui_window.btn_clear

        self.btn_run_test.clicked.connect(lambda: self.main_code())
        btn_clear.clicked.connect(lambda: self.clear_log())

        # load forks and add to the list
        self.fork_label_list.append(self.ui_window.label_fork_1)
        self.fork_label_list.append(self.ui_window.label_fork_2)
        self.fork_label_list.append(self.ui_window.label_fork_3)
        self.fork_label_list.append(self.ui_window.label_fork_4)

        # load philosopher and to the list
        self.philosopher_label_list.append(self.ui_window.label_philo_1)
        self.philosopher_label_list.append(self.ui_window.label_philo_2)
        self.philosopher_label_list.append(self.ui_window.label_philo_3)
        self.philosopher_label_list.append(self.ui_window.label_philo_4)

        # Output log
        self.console_text = self.ui_window.console_text
