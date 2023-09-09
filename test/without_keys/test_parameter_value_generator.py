import unittest

import pybamm
from bot.utils.parameter_value_generator import parameter_value_generator


class TestParameterValueGenerator(unittest.TestCase):
    def test_parameter_value_generator(self):
        parameter = {"Lower voltage cut-off [V]": (None, None)}
        chemistry = "Chen2020"
        params = pybamm.ParameterValues(chemistry)

        new_params = parameter_value_generator(params, parameter)

        assert (
            new_params[next(iter(parameter.keys()))]
            >= params[next(iter(parameter.keys()))] * 0.5
        )
        assert (
            new_params[next(iter(parameter.keys()))]
            <= params[next(iter(parameter.keys()))] * 2
        )
        assert isinstance(new_params, pybamm.ParameterValues)

        chemistry = "Marquis2019"
        params = pybamm.ParameterValues(chemistry)
        new_params = parameter_value_generator(params, parameter)

        assert (
            new_params[next(iter(parameter.keys()))]
            >= params[next(iter(parameter.keys()))] * 0.5
        )
        assert (
            new_params[next(iter(parameter.keys()))]
            <= params[next(iter(parameter.keys()))] * 2
        )
        assert isinstance(new_params, pybamm.ParameterValues)

        chemistry = "Ai2020"
        params = pybamm.ParameterValues(chemistry)
        new_params = parameter_value_generator(params, parameter)

        assert (
            new_params[next(iter(parameter.keys()))]
            >= params[next(iter(parameter.keys()))] * 0.5
        )
        assert (
            new_params[next(iter(parameter.keys()))]
            <= params[next(iter(parameter.keys()))] * 2
        )
        assert isinstance(new_params, pybamm.ParameterValues)

        chemistry = "OKane2022"
        params = pybamm.ParameterValues(chemistry)
        new_params = parameter_value_generator(params, parameter)

        assert (
            new_params[next(iter(parameter.keys()))]
            >= params[next(iter(parameter.keys()))] * 0.5
        )
        assert (
            new_params[next(iter(parameter.keys()))]
            <= params[next(iter(parameter.keys()))] * 2
        )
        assert isinstance(new_params, pybamm.ParameterValues)

        parameter = {
            "Negative electrode exchange-current density [A.m-2]": (None, None)
        }

        chemistry = "Chen2020"
        params = pybamm.ParameterValues(chemistry)
        new_params = parameter_value_generator(params, parameter)

        assert isinstance(
            float(
                new_params[
                    "Negative electrode exchange-current density [A.m-2]"
                ].__str__()
            ),
            float,
        )
        assert isinstance(new_params, pybamm.ParameterValues)

        chemistry = "Marquis2019"
        params = pybamm.ParameterValues(chemistry)
        new_params = parameter_value_generator(params, parameter)

        assert isinstance(
            float(
                new_params[
                    "Negative electrode exchange-current density [A.m-2]"
                ].__str__()
            ),
            float,
        )
        assert isinstance(new_params, pybamm.ParameterValues)

        chemistry = "Ai2020"
        params = pybamm.ParameterValues(chemistry)
        new_params = parameter_value_generator(params, parameter)

        assert isinstance(
            float(
                new_params[
                    "Negative electrode exchange-current density [A.m-2]"
                ].__str__()
            ),
            float,
        )
        assert isinstance(new_params, pybamm.ParameterValues)

        chemistry = "OKane2022"
        params = pybamm.ParameterValues(chemistry)
        new_params = parameter_value_generator(params, parameter)

        assert isinstance(
            float(
                new_params[
                    "Negative electrode exchange-current density [A.m-2]"
                ].__str__()
            ),
            float,
        )
        assert isinstance(new_params, pybamm.ParameterValues)

        parameter = {"Negative electrode diffusivity [m2.s-1]": (None, None)}
        chemistry = "Chen2020"
        params = pybamm.ParameterValues(chemistry)
        new_params = parameter_value_generator(params, parameter)

        assert isinstance(new_params, pybamm.ParameterValues)


if __name__ == "__main__":
    unittest.main()
