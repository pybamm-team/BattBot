# BattBot

<p align="center">
    <img src="https://user-images.githubusercontent.com/74055102/197869338-9f7a41aa-65e8-42f4-b5cf-d8480d3e2ae4.png"/>
    <img src="https://user-images.githubusercontent.com/74055102/198250858-e4e9063b-f941-45b6-9c89-34a8b95378fa.gif"/>
</p>

<div align="center">

[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/battbot_.svg?style=social&label=Follow%20@battbot_)](https://twitter.com/battbot_)
[![PyBaMM Twitter bot](https://github.com/pybamm-team/BattBot/actions/workflows/ci.yml/badge.svg)](https://github.com/pybamm-team/BattBot/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/pybamm-team/BattBot/branch/main/graph/badge.svg?token=6wEJ6AiiGG)](https://codecov.io/gh/pybamm-team/BattBot)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pybamm-team/BattBot/blob/main/)
[![black_code_style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

</div>

An automated Battery Bot that tweets random battery configuration plots in the form of a GIF with the help of [PyBaMM](https://github.com/pybamm-team/PyBaMM). The bot focuses on comparing 2 or 3 different configurations and can also reply to a simulation request. All the random tweeted configurations are stored in [data.txt](https://github.com/pybamm-team/BattBot/blob/main/bot/data.txt) and the latest tweeted configuration is stored in [config.txt](https://github.com/pybamm-team/BattBot/blob/main/bot/config.txt) that can also be played with on Google Colab [here](https://colab.research.google.com/github/pybamm-team/BattBot/blob/main/bot/run-simulation.ipynb). Some examples for the simulation requests through a tweet are available here - [`REQUEST_EXAMPLES.md`](https://github.com/pybamm-team/BattBot/blob/main/REQUEST_EXAMPLES.md).

## Deployment (The CI/CD pipeline)

One half of the bot is deployed on `GitHub Actions` and the other half is deployed on `Heroku`. The GitHub Actions deployment tweets random configurations at 7 am and 7 pm UTC whereas the Heroku deployment runs the script every minute to look out for tweet requests.

`GitHub Actions` is also responsible for running the tests, updating the [stored random configurations](https://github.com/pybamm-team/BattBot/blob/main/bot/data.txt), and keeping the [run-simulations](https://colab.research.google.com/github/pybamm-team/BattBot/blob/main/bot/run-simulation.ipynb) notebook in working condition (by updating the latest tweeted configuration in [config.txt](https://github.com/pybamm-team/BattBot/blob/main/bot/config.txt)). The [`last_seen_id`](https://github.com/pybamm-team/BattBot/blob/main/bot/last_seen_id.txt) (ID of the tweet to which the bot replied last) is also [synced](https://github.com/pybamm-team/BattBot/blob/main/bot/twitter_api/sync_last_seen_id.py#L20) on scheduled runs to keep the `Heroku` and `GitHub Actions` deployment in sync with each other.

Once everything in the `Continuous Integration` (`GitHub Actions`) part of the pipeline passes, the `Continuous Deployment` phase starts and the bot is deployed on `Heroku`, where it is built again with the updated `last_seen_id` (`Heroku` does not store the locally updated files permanently because of its [ephemeral filesystem](https://devcenter.heroku.com/articles/active-storage-on-heroku#ephemeral-disk), another reason to update `last_seen_id` using `GitHub Actions`).

The files that keep `Heroku` deployment running -

- [requirements.txt](https://github.com/pybamm-team/BattBot/blob/main/requirements.txt)
- [runtime.txt](https://github.com/pybamm-team/BattBot/blob/main/runtime.txt)
- [Procfile](https://github.com/pybamm-team/BattBot/blob/main/Procfile)

The file that keeps `GitHub Actions` deployment running -

- [python-app.yml](https://github.com/pybamm-team/BattBot/blob/main/.github/workflows/python-app.yml)

## Random Tweets

- The random configuration is generated in [`config_generator.py`](https://github.com/pybamm-team/BattBot/blob/main/bot/plotting/config_generator.py), hence, all the new possible options in the future should be added in this file.
- This configuration is passed down to [`random_plot_generator`](https://github.com/pybamm-team/BattBot/blob/main/bot/plotting/random_plot_generator.py#L9) which then calls different scripts based on if degradation is present in the configuration.
- Comparison plots (which are `"model comparison"` and `"parameter comparison"`) with no degradation are generated in [`ComparisonGenerator`](https://github.com/pybamm-team/BattBot/blob/main/bot/plotting/comparison_generator.py#L7)
- The GIFs are created in [`create_gif.py`](https://github.com/pybamm-team/BattBot/blob/main/bot/plotting/create_gif.py#L9) and are resized using [`resize_gif.py`](https://github.com/pybamm-team/BattBot/blob/main/bot/utils/resize_gif.py#L5) to make them suitable for `Twitter API`.
- The GIFs are then finally tweeted out by the [`Tweet`](https://github.com/pybamm-team/BattBot/blob/main/bot/twitter_api/tweet_plot.py#L13) class.

## Requested Tweets

- The replying functionality is a hybrid of [`tweepy`](https://docs.tweepy.org/en/stable/) and inbuilt python libraries `requests` and `requests_oauthlib`.
- The [`Reply`](https://github.com/pybamm-team/BattBot/blob/main/bot/twitter_api/tweet_reply.py#L11) class is responsible for reading the tweet requests and for creating a configuration from that tweet's text.
- This configuration is then passed down to `random_plot_generator` which now simulates and solves it (as it does with the random configuration).

## Uploading and Replying (Twitter API)

- A GIF is uploaded and tweeted using the [`Upload`](https://github.com/pybamm-team/BattBot/blob/main/bot/twitter_api/upload.py#L13) class. It uploads a media file in chunks (keeping in mind `Twitter API`'s time out) to a `Twitter API`'s endpoint and then finally tweets it.
- `Tweet` and `Reply` classes inherit the `Upload` class to tweet random and user-requested GIFs.

## Tests and coverage

The tests and the workflows are designed in a way that protects the `Twitter API keys` from getting revealed. The tests that require `Twitter API keys` to run, never run on a PR coming from a forked repository, as that would expose the `API keys` and anyone with a malicious script on that PR will be able to print/store/read them. More information on the structure of the `test` directory can be found [here](https://github.com/pybamm-team/BattBot/blob/main/CONTRIBUTING.md#testing).

The bot uses a lot of multiprocessing calls (using a custom [`Process`](https://github.com/pybamm-team/BattBot/blob/main/bot/utils/custom_process.py#L6) class) which makes the code coverage a bit unusual. The [`sitecustomize.py`](https://github.com/pybamm-team/BattBot/blob/main/sitecustomize.py) and [`.coveragerc`](https://github.com/pybamm-team/BattBot/blob/main/.coveragerc) files make sure that coverage is used to run tests in subprocesses. Complete documentation for this can be found [here](https://coverage.readthedocs.io/en/coverage-5.5/subprocess.html).

The coverage report on a PR coming from a fork will show that the coverage goes down (even if everything is covered) as some tests won't run on that PR as described above.

## Citing PyBaMM

If you use PyBaMM in your work, please cite the paper

> Sulzer, V., Marquis, S. G., Timms, R., Robinson, M., & Chapman, S. J. (2021). Python Battery Mathematical Modelling (PyBaMM). _Journal of Open Research Software, 9(1)_.

You can use the bibtex

```
@article{Sulzer2021,
  title = {{Python Battery Mathematical Modelling (PyBaMM)}},
  author = {Sulzer, Valentin and Marquis, Scott G. and Timms, Robert and Robinson, Martin and Chapman, S. Jon},
  doi = {10.5334/jors.309},
  journal = {Journal of Open Research Software},
  publisher = {Software Sustainability Institute},
  volume = {9},
  number = {1},
  pages = {14},
  year = {2021}
}
```

To cite papers relevant to your code, you can add the following -

```python3
pybamm.print_citations()
```

to the end of your script. This will print bibtex information to the terminal; passing a filename to `print_citations` will print the bibtex information to the specified file instead. A list of all citations can also be found in the [citations file](https://github.com/pybamm-team/PyBaMM/blob/develop/pybamm/CITATIONS.txt).

## Contributing to BattBot

All contributions to this repository are welcome. You can go through our [contribution guidelines](https://github.com/pybamm-team/BattBot/blob/main/CONTRIBUTING.md) to make the whole process smoother.
