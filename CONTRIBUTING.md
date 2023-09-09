# Contributing to BattBot

All contributions to this repository are welcomed, please have a look at the guidelines below for smoother contributions.
Some of the guidelines (which are common) have been picked up from the [PyBaMM](https://github.com/pybamm-team/PyBaMM/blob/develop/CONTRIBUTING.md) repository.

## Pre-installation

Though it isn't necessary to have a [Twitter Deveoper Account](https://developer.twitter.com/en/apply-for-access) for contributing to this repository, you can still apply for one to test out the tweeting functionality locally.

If you do have one, or have applied for one, you can follow the step below to set up the `Twitter API keys` -

- Add `CONSUMER_KEY`, `CONSUMER_SECRET`, `ACCESS_KEY` and `ACCESS_SECRET` to your environment variables with exactly these names.

**_DO NOT ADD THE API KEYS IN THE CODE. The tests will fail if you create a PR with API keys in your branch, and at this point you should reset the API keys from your developer account dashboard immediately._**

## Local installation

Follow the steps below to locally install the bot for development -

1. Fork [this](https://github.com/pybamm-team/BattBot) repository.
2. Clone the forked repository.
3. Run the following commands -

```bash
cd Battbot
python -m pip install -r requirements.txt
```

This will install all the dependencies in your local system including the latest version of [PyBaMM](https://github.com/pybamm-team/PyBaMM) on which this bot is based.

4. To check if the installation worked, execute (this will take some time) -

```bash
python -m unittest -v
# or if you haven't completed the pre-installation process, this -
python -m unittest discover ./test/without_keys/ -v
```

**Note: The tests written in `with_keys` subdirectory will fail if you haven't completed the pre-installation process, again, you don't necessarily need the `Twitter Developer Account` to contribute to this repository.**

## Workflow

1. If you find something that is wrong or something that can be improved, you can open up an [issue](https://github.com/pybamm-team/BattBot/issues) for discussing the topic with others.
2. Once you take up the issue (or a pre-existing issue), you can proceed with creating a branch on your fork.
3. Once you are done with the changes, you can test your code and the coverage by running -

```bash
echo "COVERAGE_PROCESS_START=$PWD/.coveragerc"  # to enable coverage to run tests in subprocesses
coverage run --concurrency=multiprocessing -m unittest -v
# or if you haven't completed the pre-installation process
coverage run --concurrency=multiprocessing -m unittest discover -v test/without_keys
coverage combine
coverage report  # for a better visualisation, you can run - coverage html
```

Once this executes, you will be able to see if any tests are failing or if the coverage dropped. You can always create a PR to get even better test/coverage suggestions and reviews.

4. Once everything passes, you can go ahead and create a [Pull Request](https://github.com/pybamm-team/BattBot/pulls) for the constructive review process.

## GitHub Actions

- The tweeting process is being carried out by GitHub Actions and hence, utmost care should be taken while editing the `.yml` file.

- All the replying process is being carried out by Heroku, hence the `Procfile`, `requirements.txt`, `runtime.txt` and `last_seen_id.txt` should be checked thoroughly before merging the code in the main (deployed) branch.

- This does not mean that the failing `with_keys` tests will pass (even if everything is working) on a PR as a PR from a fork cannot pull the `Twitter API Keys` from repository secrets due to security reasons.

- This however also does not mean that the tests will fail, only the tests which do not require the `Twitter API keys` will run on the PRs from a fork. This might effect the coverage but the other tests will pass.

## Writing your code

1. For styling we use [flake8](https://pypi.org/project/flake8/) and [black](https://pypi.org/project/black/) to maintain uniformity throughout the codebase.
2. While adding code, make sure to give your commits some meaningful messages.
3. When taking a snippet of code from somewhere else (say [StackOverflow](https://stackoverflow.com/)), always attribute the answer by providing the link in the comments.
4. Always try to avoid repetitive code, refactor it and then use it at different places.
5. While writing some probabilistic code, make sure to structure it in a way that it can be deterministically tested.

## Testing

All code requires testing. We use the [unittest](https://docs.python.org/3/library/unittest.html) package for our tests.

The tests right now are divided into two directories, which are `with_keys` and `without_keys`. The tests which require `Twitter API keys` to run should be placed in the `with_keys` directory so that they do not run on a PR from a fork. Other tests should be placed in the `without_keys` directory.

Every new feature should have its own test. To create ones, have a look at the test directory and see if there's a test for a similar method. Copy-pasting this is a good way to start.

Next, add some simple (and speedy!) tests of your main features. If these run without exceptions that's a good start! Next, check the output of your methods using any of these [assert method](https://docs.python.org/3.3/library/unittest.html#assert-methods).

## Documentation

Most of the documentation in this repository is of the form of docstrings and comments. Every class and function should have a docstring and the codebase should be well commented. Other than this, there is some documentation in markdown as well, which can be updated whenever required.

## Google Colab

Editable notebook, to run the random tweeted configurations is made available using Google Colab [here](https://colab.research.google.com/github/pybamm-team/BattBot/blob/main/).

## Codecov

Code coverage (how much of our code is actually seen by the (linux) unit tests) is tested using Codecov, a report is visible on https://app.codecov.io/gh/pybamm-team/BattBot/.

## Pre-commit checks

1. Style - `$ flake8 --max-line-length=89`
2. Tests - `$ python -m unittest -v` (if you have completed the pre-installation process) or `$ python -m unittest -v discover ./test/ without_keys` (if you have haven't completed the pre-installation process)
