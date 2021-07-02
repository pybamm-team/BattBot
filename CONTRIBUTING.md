# Contributing to PyBaMM-Twitter-Bot

All contributions in this repository are welcomed but, please have a look at the guidelines below before you contribute to this repository.

## Pre-installation
Though it isn't necessary to have a [Twitter Deveoper Account](https://developer.twitter.com/en/apply-for-access) for contributing to this repository, you can still apply for one to test out the tweeting functionality locally.

If you do have one, or have applied for one, you can follow the steps below to set up the `Twitter API keys` -
1. Add `CONSUMER_KEY`, `CONSUMER_SECRET`, `ACCESS_KEY` and `ACCESS_SECRET` to your environment variables with exactly these names.

***DO NOT ADD THE API KEYS IN THE CODE. The tests will fail if you create a PR with API keys in your branch, and at this point you should reset the API keys from your developer account dashboard immediately.***

## Local installation
Follow the steps below to locally install the bot for development -
1. Fork [this](https://github.com/Saransh-cpp/PyBaMM-Twitter-Bot) repository.
2. Clone the forked repository.
3. Run the following commands - 
```bash
cd PyBaMM-Twitter-Bot
python -m pip install -r requirements.txt
```
This will install all the dependencies in your local system including the develop [PyBaMM](https://github.com/pybamm-team/PyBaMM) on which this bot is based.

4. To check if the installation worked, execute (this will take some time) - 
```bash
python -m unittest
```
**Note: The tests written in `test_tweet_plot.py` will fail if you haven't completed the pre-installation process, again, you don't necessarily need the `Twitter Developer Account` to contribute to this repository.**

# Workflow
1. If you find something that is wrong or something that can be improved, you can open up an [issue](https://github.com/Saransh-cpp/PyBaMM-Twitter-Bot/issues) for discussing the topic with others.
2. Once you take up the issue (or a pre-existing issue), you can proceed with creating a branch on your fork.
3. Once you are done with the changes, you can test your code and the coverage by running -
```bash
coverage run -m unittest
coverage combine
coverage report  # for a better visualisation, you can run coverage html
```
Once this executes, you will be able to see if any tests are failing or if the coverage dropped. You can always create a PR to get even better test/coverage suggestions and and reviews.

4. Once everything passes, you can go ahead and create a [Pull Request](https://github.com/Saransh-cpp/PyBaMM-Twitter-Bot/pulls) for the constructive review process.
