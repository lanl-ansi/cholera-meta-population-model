## Cholera meta-population model

Analysing cholera epidemics in Argentina in the 90s using case count and genetic sequence data.
The code implements fitting procedure for a meta-population susceptible-infected-asymptomatic-recovered (SIAR) model.
More details about the model and used data can be found in the paper cited below.
Algorithm allows to:
- Fit the data from three argentinian cities, which were hit by cholera in the 90s.
    - fit_data.py
- Run the same fitting procedure, but with an additional assumption that only undercounting is present.
    - only_undercount.py
- Run synthetic experiment with different types of noise.
    - synth_gamma_.py
    - synth_gauss_.py
    - synth_negbinom_.py
- Run the same fitting procedure, but with additional noise on the travelling parameters.
    - travel_noise.py

## Reference

The code was developed while working on the following article:
https://arxiv.org/abs/...

If you found the repository useful in your work, we kindly ask that you cite:
```
...
```

## License

This code is provided under a BSD license as part of the Optimization, Inference and Learning for Advanced Networks project, C18014.
