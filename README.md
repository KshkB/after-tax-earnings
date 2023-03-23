# After tax earnings

In this repository you will find a script, `income_analyzer.py`, and an executable notebook, `income_analysis.ipynb`, aiming to model a person's afer-tax earnings in a given progressive taxation system.

The executable notebook is currently filled in with the tax brackets and rates defining the progressive taxation system in Australia. Change these as desired to define different progressive taxation systems.

And furthermore, change other parameters in the notebook as desired and execute the cell blocks to generate different earnings estimates and plots.

## The earnings model

As part of generating earnings estimates after a given number of years, the model takes into account the following *conditions*:

- tax brackets and rates defining the progressive taxation system;
- yearly wage;
- yearly wage growth;
- savings rate (proportion of yearly, after-tax earnings saved for reinvestment);
- savings return (annualised yearly return on savings invested).

And conversely the model can also generate, in a given progressive taxation system and conditions above, the number of years required earn a given target earnings. 

## Requirements

In order to plot the earnings curve as a function of time, ensure you have the library `matplotlib` installed.
