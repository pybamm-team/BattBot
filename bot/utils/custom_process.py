import multiprocessing
import traceback


# original code - https://stackoverflow.com/a/33599967/4992248
class Process(multiprocessing.Process):
    """
    Class which returns child Exceptions to Parent.
    """

    def __init__(self, *args, **kwargs):
        multiprocessing.Process.__init__(self, *args, **kwargs)
        self._parent_conn, self._child_conn = multiprocessing.Pipe()
        self._exception = None

    def run(self):
        try:
            multiprocessing.Process.run(self)
            self._child_conn.send(None)  # pragma: no cover
        except Exception as e:
            tb = traceback.format_exc()
            self._child_conn.send((e, tb))

    # the exception can now be accessed in the main process using object
    @property
    def exception(self):
        if self._parent_conn.poll():
            self._exception = self._parent_conn.recv()
        return self._exception
