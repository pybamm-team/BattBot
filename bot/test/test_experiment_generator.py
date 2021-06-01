import unittest
import pybamm
from experiment.experiment_generator import experiment_generator


class TestExperimentSolver(unittest.TestCase):
    def test_experiment_generator_with_rest(self):
        cycle, number = experiment_generator({"rest1": True, "rest2": True})
        self.assertTrue(len(cycle) == 5)
        self.assertIsInstance(number, int)
        self.assertEqual(cycle[0][:9], "Discharge")
        self.assertEqual(cycle[1][:4], "Rest")
        self.assertEqual(cycle[2][:6], "Charge")
        self.assertEqual(cycle[3][:4], "Hold")
        self.assertEqual(cycle[4][:4], "Rest")

        pybamm.Experiment(cycle * number)

    def test_experiment_generator_with_random_experiment(self):
        cycle, number = experiment_generator()
        self.assertTrue(len(cycle) == 5 or len(cycle) == 3 or len(cycle) == 4)
        self.assertIsInstance(number, int)
        self.assertEqual(cycle[0][:9], "Discharge")

        if len(cycle) == 3:
            self.assertEqual(cycle[1][:6], "Charge")
            self.assertEqual(cycle[2][:4], "Hold")
        elif len(cycle) == 4:
            if cycle[1][:4] == "Rest":
                self.assertEqual(cycle[2][:6], "Charge")
                self.assertEqual(cycle[3][:4], "Hold")
            elif cycle[3][:4] == "Rest":
                self.assertEqual(cycle[1][:6], "Charge")
                self.assertEqual(cycle[2][:4], "Hold")
        elif len(cycle) == 5:
            self.assertEqual(cycle[1][:4], "Rest")
            self.assertEqual(cycle[2][:6], "Charge")
            self.assertEqual(cycle[3][:4], "Hold")
            self.assertEqual(cycle[4][:4], "Rest")

        pybamm.Experiment(cycle * number)


if __name__ == "__main__":
    unittest.main()
