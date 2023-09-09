import unittest

from bot.utils.custom_process import Process


class TestCustomProcess(unittest.TestCase):
    def test_custom_process(self):
        p = Process(target=call_using_custom_process, args=(True,))

        p.start()
        # time-out
        p.join(5)

        if p.exception:
            e, traceback = p.exception

        assert str(e) == "The test is working"
        assert isinstance(e, Exception)


def call_using_custom_process(is_working):
    if is_working:
        raise Exception("The test is working")


if __name__ == "__main__":
    unittest.main()
