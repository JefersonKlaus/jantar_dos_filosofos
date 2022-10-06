import random
from enum import Enum
from threading import Thread
from time import sleep
from typing import List

from PyQt5.QtCore import pyqtSignal


class PhilosopherStatus(Enum):
    THINKING = 1
    HUNGRY = 2
    EATING = 3
    DONE = 4


class ForkStatus(Enum):
    IN_USE = 1
    FREE = 2
    WAITING = 3


class Philosopher(Thread):
    name = None
    table_position = 0
    status = PhilosopherStatus.THINKING

    fork_list = None
    left_fork = None
    right_fork = None

    _func_log_signal = None
    _FINISH_WHEN_EAT_COUNT = 5

    def __init__(
        self,
        name: str,
        table_position: int,
        fork_list: List[ForkStatus],
        func_log_signal: pyqtSignal(str) = None,
    ):
        """
        :param name: Name of philosopher
        :param table_position: 0 = position 1 | 3 = position 4 ...
        :param fork_list: Shared list of forks
        """
        Thread.__init__(self)
        self._func_log_signal = func_log_signal

        self.name = name
        self.table_position = table_position
        self.fork_list = fork_list

        # get positions of forks
        self.right_fork = table_position
        if table_position == len(fork_list) - 1:
            self.left_fork = 0
        else:
            self.left_fork = table_position + 1

        self.status = PhilosopherStatus.THINKING
        self.log(self.name + ": " + "Começou a pensar")

    def run(self):
        _eat_times = 0
        while _eat_times < self._FINISH_WHEN_EAT_COUNT:

            if (
                self.status == PhilosopherStatus.HUNGRY
            ):  # when he is hungry does not sleep
                sleep(1)
            else:
                sleep(random.randint(4, 8))  # random time

            if self.status == PhilosopherStatus.THINKING:
                self.status = PhilosopherStatus.HUNGRY  # after think began hungry
                self.log(self.name + ": " + "Faminto")
                continue

            if self.status == PhilosopherStatus.EATING:
                self.fork_list[self.right_fork] = ForkStatus.FREE
                self.fork_list[self.left_fork] = ForkStatus.FREE
                self.status = PhilosopherStatus.THINKING  # after eat came back to think
                self.log(self.name + ": " + "Pensando")
                continue

            if self.status == PhilosopherStatus.HUNGRY:
                # check the RIGHT FORK
                if self.fork_list[self.right_fork] == ForkStatus.FREE:
                    self.fork_list[self.right_fork] = ForkStatus.WAITING
                else:
                    self.log(self.name + ": " + "Garfo esq. ocupado")
                    continue  # keep the same status

                # check the LEFT FORK
                if self.fork_list[self.left_fork] == ForkStatus.FREE:
                    self.fork_list[self.left_fork] = ForkStatus.WAITING
                else:
                    self.fork_list[self.right_fork] = ForkStatus.FREE
                    self.log(self.name + ": " + "Garfo dir. ocupado")
                    continue  # keep the same status

                self.fork_list[self.right_fork] = ForkStatus.IN_USE
                self.fork_list[self.left_fork] = ForkStatus.IN_USE
                self.status = PhilosopherStatus.EATING
                _eat_times = _eat_times + 1
                self.log(self.name + ": " + "Comendo (" + str(_eat_times) + ")")

        # philosopher is done
        sleep(random.randint(4, 8))
        self.fork_list[self.right_fork] = ForkStatus.FREE
        self.fork_list[self.left_fork] = ForkStatus.FREE
        self.status = PhilosopherStatus.DONE
        self.log(self.name + ": " + "!! ACABOU !!")

    def log(self, message):
        if self._func_log_signal:
            self._func_log_signal.emit(message)
