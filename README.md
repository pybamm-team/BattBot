# PyBaMM-Twitter-Bot

![image](https://miro.medium.com/max/788/1*z_AwTGIVYneAzpzwPUGDxw.gif)

[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/battbot_.svg?style=social&label=Follow%20@battbot_)](https://twitter.com/battbot_)
![Twitter Bot](https://github.com/Saransh-cpp/TwitterBot/actions/workflows/python-app.yml/badge.svg?branch=master)
[![codecov](https://codecov.io/gh/Saransh-cpp/PyBaMM-Twitter-Bot/branch/main/graph/badge.svg?token=P1h4VGtlSt)](https://codecov.io/gh/Saransh-cpp/PyBaMM-Twitter-Bot)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Saransh-cpp/PyBaMM-Twitter-Bot/blob/main/)
[![black_code_style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)



An automated Battery Bot that tweets random battery configuration plots in the form of a GIF with the help of [PyBaMM](https://github.com/pybamm-team/PyBaMM). The bot focuses on comparing 2 or 3 different configurations. All the tweeted configurations are stored in [data.txt](https://github.com/Saransh-cpp/PyBaMM-Twitter-Bot/blob/main/bot/data.txt) and the latest tweeted configuration is stored in [config.txt](https://github.com/Saransh-cpp/PyBaMM-Twitter-Bot/blob/main/bot/config.txt) which can also be played with on Google Colab [here](https://colab.research.google.com/github/Saransh-cpp/PyBaMM-Twitter-Bot/blob/main/bot/run-simulation.ipynb).


## Citing PyBaMM

If you use PyBaMM in your work, please cite the paper

> Sulzer, V., Marquis, S. G., Timms, R., Robinson, M., & Chapman, S. J. (2020). Python Battery Mathematical Modelling (PyBaMM). _ECSarXiv. February, 7_.

You can use the bibtex

```
@article{sulzer2020python,
  title={Python Battery Mathematical Modelling (PyBaMM)},
  author={Sulzer, Valentin and Marquis, Scott G and Timms, Robert and Robinson, Martin and Chapman, S Jon},
  journal={ECSarXiv. February},
  volume={7},
  year={2020}
}
```

To cite papers relevant to your code, you add the following -

```python3
pybamm.print_citations()
```

to the end of your script. This will print bibtex information to the terminal; passing a filename to `print_citations` will print the bibtex information to the specified file instead. A list of all citations can also be found in the [citations file](https://github.com/pybamm-team/PyBaMM/blob/develop/pybamm/CITATIONS.txt).

## Contributing to PyBaMM-Twitter-Bot

All contributions to this repository are welcome. You can go through our [Contribution guidelines](https://github.com/pybamm-team/PyBaMM/blob/develop/CONTRIBUTING.md) to make the whole process smoother.
