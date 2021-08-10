# Examples for simulation requests through twitter

This file contains a list of possible tweets that the bot can effectively read and reply to. The file will be updated whenever a new type of simulations is added to the bot.

**Using `#battbot` and mentioning `@battbot_` in every tweet request is mandatory.**

## Models
The model names that you can use in a tweet (casing of the sentence won't matter) -
 - `Doyle-Fuller-Newman model` or `DFN`
 - `Single particle model` or `SPM`
 - `Single particle model with electrolyte` or `SPMe`

## Parameter sets / Chemistries
The parameter sets or the chemistries that you can use in a tweet (casing of the sentence won't matter) -
 - `Chen2020`
 - `Marquis2019`
 - `Ai2020`

## Compare 2 or more models with a constant discharge
### Some examples -
```
@battbot_ compare SPM and SPMe for a constant dicharge of 1.25C at 290K with Chen2020 parameters #battbot.
@battbot_ #battbot can you compare Single particle model, Single particle model with electrolyte and DFN model at 300K with a c-rate of 0.5C with Marquis2019 chemistry?
@battbot_ #battbot compare spm, spme DFN model with a constant dicharge of 0.75C with Ai2020 at 280K
```

### Mandatory keywords -
Adding ',' anywhere and the casing of the sentence in the tweet text won't effect the simulation.
 - Adding the keyword `"Compare"`.
 For example -
 ```
 <space or no character>Compare<space or no character>
 Compare SPM and SPMe
 ```
 If not provided, the bot will give the following error -
 ```
 "I'm sorry, I couldn't understand the requested simulation."
 ```
 - Providing `models`.
 For example -
 ```
 <space or no character>SPM<space or no character>
 SPM, SPMe and DFN model
 Single particle model and Doyle-Fuller-Newman model
 ```
 If not provided, the bot will give the following error -
 ```
 "Please provide atleast 2 models."
 ```
 - Providing `parameter sets or chemistry`.
 For example -
 ```
 <space or no character>Chen2020<space or no character>
 with Chen2020 chemistry
 with Marquis2019
 using Ai2020 parameters
 ```
 If not provided, the bot will give the following error -
 ```
 "Please provide a parameter set in the format - Chen2020."
 ```
 - Providing `C-rate`.
 For example -
 ```
 <space or no character>1C<space or no character>
 for a constant dicharge of 1C
 with c-rate = 1.5C 
 with a dicharge of 3C
 ```
 If not provided or if incorrectly provided, the bot will give the following error -
 ```
 "Please provide 'C rate' in the format - 1C."
 ```
 - Providing `"Ambient temperature [K]`.
 For example -
 ```
 <space or no character>298K<space or no character>
 at a temperature of 290K
 at 298K
 ```
 If not provided or if incorrectly provided, the bot will give the following error -
 ```
 "Please provide 'Ambient temperature' in the format - 273.15K."
 ```
