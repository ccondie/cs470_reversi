from threading import Thread
from ReversiAI_Python_v3 import AiGuyThread


class SimRunner(object):
    def __init__(self, ai_thread1, ai_thread2):
        ai_thread1.daemon = True
        ai_thread2.daemon = True

    def run(self):
        pass


if __name__ == '__main__':
    ai1 = AiGuyThread('localhost', 1, 3)
    ai2 = AiGuyThread('localhost', 2, 3)
    sim = SimRunner(ai1, ai2)

    sim.run()
