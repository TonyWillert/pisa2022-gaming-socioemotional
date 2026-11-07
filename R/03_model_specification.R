# Explanatory specification adapted from the nine 2024 outcome scripts.
# This file does not fit models, recreate imputations, or validate old estimates.
# competency is a placeholder for one of the nine outcome columns.

unadjusted <- competency ~ dpt + (1 | cid)
adjusted <- competency ~ dpt + hisei + gender + (1 | cid)

# Original intended workflow:
# 1. Fit each specification separately within each completed dataset.
# 2. Use standardised outcome/DPT/HISEI for the standardised versions;
#    keep gender categorical (1 = female, 2 = male).
# 3. Pool model estimates with mitml::testEstimates(models).
#
# Before any future refit, resolve outcome coverage and the original zero-mask
# implementation, define explicit analysis filters, and use the same population
# for coefficients and fit statistics. No corrected refit is claimed here.
