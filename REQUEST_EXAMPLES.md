# Examples for simulation requests through twitter

This file contains a list of possible tweets that the bot can effectively read and reply to. The file will be updated whenever a new type of simulations is added to the bot.

**Using `#battbot` and mentioning `@battbot_` in every tweet request is mandatory.**

## Model keys
The model names that you can use in a tweet (casing of the sentence won't matter) -
 - `Doyle-FUller-Newman model` or `DFN`
 - `Single particle model` or `spm`
 - `Single particle model with electrolyte` or `spme`

## Parameter set keys
The parameter sets or the chemistries that you can use in a tweet (casing of the sentence won't matter) -
 - `Chen2020`
 - `Marquis2019`
 - `Ai2020`

## Compare 2 models with a constant discharge
### Some examples -
```
@battbot_ compare SPM and SPMe with Chen2020 parameters #battbot.
@battbot_ #battbot can you compare Single particle model, Single particle model with electrolyte and DFN model with Marquis2019 parameters
@battbot_ #battbot compare spm, spme DFN model with Ai2020 parameters please
```

### Mandatory keywords -
 - Adding the keyword `"Compare"`.
 For example -
 ```
 "Compare" SPM and SPMe with Chen2020 parameters
 ```
 If not provided, the bot will give the following error -
 ```
 "I'm sorry, I couldn't understand the requested simulation. Some tweet examples - "
 ```
 - Providing models.
 For example -
 ```
 SPM and SPMe
 ```
 If not provided, the bot will give the following error -
 ```
 "Please provide atleast 2 models. Some tweet examples - "
 ```
 - Providing parameter sets or chemistry
 For example -
 ```
 <space>Chen2020<space>parameters<space or nothing>
 with Chen2020 parameters   # correct
 with Chen2020 parameters.  # incorrect, don't add '.'
 using Chen2020 parameters  # correct
 ```
 If not provided, the bot will give the following error -
 ```
 "Please provide a parameter set in the format - Chen2020 parameters - Some tweet examples - "
 ```
