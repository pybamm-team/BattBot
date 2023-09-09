import unittest

import pybamm
from bot.experiment.experiment_generator import experiment_generator


class TestExperimentSolver(unittest.TestCase):
    def test_experiment_generator_with_rest(self):
        cycle = experiment_generator({"rest1": True, "rest2": True})
        assert len(cycle[0]) == 5
        assert cycle[0][0][:9] == "Discharge"
        assert cycle[0][1][:4] == "Rest"
        assert cycle[0][2][:6] == "Charge"
        assert cycle[0][3][:4] == "Hold"
        assert cycle[0][4][:4] == "Rest"

        pybamm.Experiment(cycle)

    def test_experiment_generator_with_random_experiment(self):
        cycle = experiment_generator()
        assert len(cycle[0]) == 5 or len(cycle[0]) == 3 or len(cycle[0]) == 4
        assert cycle[0][0][:9] == "Discharge"

        if len(cycle[0]) == 3:
            assert cycle[0][1][:6] == "Charge"
            assert cycle[0][2][:4] == "Hold"
        elif len(cycle[0]) == 4:
            if cycle[0][1][:4] == "Rest":
                assert cycle[0][2][:6] == "Charge"
                assert cycle[0][3][:4] == "Hold"
            elif cycle[0][3][:4] == "Rest":
                assert cycle[0][1][:6] == "Charge"
                assert cycle[0][2][:4] == "Hold"
        elif len(cycle[0]) == 5:
            assert cycle[0][1][:4] == "Rest"
            assert cycle[0][2][:6] == "Charge"
            assert cycle[0][3][:4] == "Hold"
            assert cycle[0][4][:4] == "Rest"

        pybamm.Experiment(cycle)


if __name__ == "__main__":
    unittest.main()
