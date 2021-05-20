import pybamm
import random
import sys
import importlib.util
from plotting.plot_graph import plot_graph
from models.model_generator import model_generator
from utils.chemistry_generator import chemistry_generator


def random_plot_generator():

    while True:

        try:
            choice = random.randint(0, 1)
            choice = 0

            if choice == 0:
                parameter_number = random.randint(0, 1)
                parameter_number = 0
                print(parameter_number)

                if parameter_number == 0:
                    (
                        current_function,
                        upper_voltage,
                        lower_voltage,
                        ambient_temp,
                        initial_temp,
                        reference_temp,
                    ) = chemistry_generator("Chen2020")

                elif parameter_number == 1:
                    (
                        current_function,
                        upper_voltage,
                        lower_voltage,
                        ambient_temp,
                        initial_temp,
                        reference_temp,
                    ) = chemistry_generator("Marquis2019")

                if lower_voltage < upper_voltage:
                    (parameter_values, sim, solution, model) = model_generator(
                        current_function=current_function,
                        upper_voltage=upper_voltage,
                        lower_voltage=lower_voltage,
                        ambient_temp=ambient_temp,
                        initial_temp=initial_temp,
                        reference_temp=reference_temp,
                        parameter_number=parameter_number,
                    )

                    time = plot_graph(solution, sim)

                    return model, parameter_values, time, parameter_number

        except:
           pass

