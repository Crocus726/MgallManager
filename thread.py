from threading import Thread, Timer


class MgallThread(Thread):
    def __init__(self, parent, time):
        Thread.__init__(self)
        self.parent = parent
        self.time = time

    def block(self):
        self.timer = Timer(self.time, self.block)
        self.parent.tryBlock()
        self.timer.start()

    def delete(self):
        self.timer = Timer(self.time, self.delete)
        self.parent.tryDelete()
        self.timer.start()

    def stop(self):
        self.timer.cancel()
