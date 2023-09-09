# Examples for simulation requests through twitter

This file contains a list of possible tweets that the bot can effectively read and reply to. The file will be updated whenever a new type of simulations is added to the bot.

**Using `#battbot` and mentioning `@battbot_` in every tweet request is mandatory.**

Adding ',', ':' or '-' anywhere in the tweet text won't affect the simulation.
Casing of the experiment conditions should be correct, other than that it won't affect the simulation.

## Models

The model names that you can use in a tweet (casing of the model won't matter) -

- `Doyle-Fuller-Newman model` or `DFN`
- `Single particle model` or `SPM`
- `Single particle model with electrolyte` or `SPMe`

## Parameter sets / Chemistries

The parameter sets or the chemistries that you can use in a tweet (casing of the chemistry won't matter) -

- `Chen2020`
- `Marquis2019`
- `Ai2020`

## Compare 2 or more models with a constant discharge or with an experiment

### Some examples -

```
@battbot_ compare SPM and SPMe for a constant discharge of 1.25C at 290K with Chen2020 parameters #battbot.
@battbot_ #battbot can you compare Single particle model, Single particle model with electrolyte and DFN model at 300K with a c-rate of 0.5C with Marquis2019 chemistry?
@battbot_ #battbot compare spm, spme DFN model with a constant dicharge of 0.75C with Ai2020 at 280K
@battbot_ #battbot compare spm and spme with chen2020 parameters with the experiment - [('Discharge at C/10 for 10 hours or until 3.3 V','Rest for 1 hour','Charge at 1 A until 4.1 V','Hold at 4.1 V until 50 mA','Rest for 1 hour')] * 3 at 298K
```

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
  Provide 2 or more models for `"model comparison"`. For example -

```
<space or no character>SPM<space or no character>
SPM, SPMe and DFN model
Single particle model and Doyle-Fuller-Newman model
```

If not provided, the bot will give the following error -

```
"Please provide at least 2 models."
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

- Providing `"Ambient temperature [K]"`.
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

- Providing `experiment`.
  Adding the keyword `experiment` is only required if you want to simulate an experiment. Casing of the experiment should be correct and "'" should be used to specify the conditions. For example -

```
with<space or no character>experiment<space or no character>- [('Discharge at C/10 for 10 hours or until 3.3 V','Rest for 1 hour','Charge at 1 A until 4.1 V','Hold at 4.1 V until 50 mA','Rest for 1 hour')]<space>*<space>3
use the<space or no character>experiment<space or no character>[('Discharge at C/10 for 10 hours or until 3.3 V','Rest for 1 hour','Charge at 1 A until 4.1 V','Hold at 4.1 V until 50 mA','Rest for 1 hour')]<space>*<space>3
```

If the experiment is not provided after adding the `experiment` keyword or if it is provided incorrectly, the bot will give the following error -

```
"Please provide experiment in the format - "[('Discharge at C/10 for 10 hours or until 3.3 V', 'Rest for 1 hour', 'Charge at 1 A until 4.1 V', 'Hold at 4.1 V until 50 mA', 'Rest for 1 hour')] * 2."
```

## Compare 2 or more values of a parameter with a constant discharge or with an experiment

Always provide the configuration/information in the following order -

1. Parameter to vary
2. Varied values
3. Experiment

### Some examples -

```
@battbot_ #battbot Vary "Electrode height [m]", values - [0.1, 0.4, 0.7] with DFN model with a constant dicharge of 0.75C with Ai2020 at 280K
@battbot_ #battbot vary "Electrode height [m]" with the values [0.1, 0.4, 0.7] with spm using chen2020 parameters with the experiment - [('Discharge at C/10 for 10 hours or until 3.3 V','Rest for 1 hour','Charge at 1 A until 4.1 V','Hold at 4.1 V until 50 mA','Rest for 1 hour')] * 3 at 298K
```

- Adding the keyword `"Vary"`.
  For example -

```
<space or no character>Vary<space or no character>
Vary "Electrode height [m]"
```

If not provided, the bot will give the following error -

```
"I'm sorry, I couldn't understand the requested simulation."
```

- Adding a `parameter to vary` enclosed with `" "`.
  For example -

```
"Electrode height [m]"
Vary "Electrode height [m]"
```

If not provided, the bot will give the following error -

```
'Please provide a parameter to vary and the varied values in the format - "Parameter to vary" with the values [1, 2, 3].'
```

- Providing `values`.
  Should be enclosed with `[]`. For example -

```
[1, 2, 3]
Vary "Electrode height [m]", values - [0.1, 0.4, 0.7]
Vary "Electrode height [m]", [0.1, 0.4, 0.7]
Vary "Electrode height [m]" with values - [0.1, 0.4, 0.7]
```

If not provided, the bot will give the following error -

```
'Please provide a parameter to vary and the varied values in the format - "Parameter to vary" with the values [1, 2, 3].'
```

- Providing `model`.
  Provide only 1 model for `"parameter comparison"`. For example -

```
<space or no character>SPM<space or no character>
SPM
Doyle-Fuller-Newman model
```

If not provided, the bot will give the following error -

```
"Please provide a model."
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

- Providing `"Ambient temperature [K]"`.
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

- Providing `experiment`.
  Adding the keyword `experiment` is only required if you want to simulate an experiment. Casing of the experiment should be correct and always use "'" to specify the conditions. For example -

```
with<space or no character>experiment<space or no character>- [('Discharge at C/10 for 10 hours or until 3.3 V','Rest for 1 hour','Charge at 1 A until 4.1 V','Hold at 4.1 V until 50 mA','Rest for 1 hour')]<space>*<space>3
use the<space or no character>experiment<space or no character>[('Discharge at C/10 for 10 hours or until 3.3 V','Rest for 1 hour','Charge at 1 A until 4.1 V','Hold at 4.1 V until 50 mA','Rest for 1 hour')]<space>*<space>3
```

If the experiment is not provided after adding the `experiment` keyword or if it is provided incorrectly, the bot will give the following error -

```
"Please provide experiment in the format - "[('Discharge at C/10 for 10 hours or until 3.3 V', 'Rest for 1 hour', 'Charge at 1 A until 4.1 V', 'Hold at 4.1 V until 50 mA', 'Rest for 1 hour')] * 2."
```
