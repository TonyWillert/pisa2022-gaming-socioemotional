# Limitations and scope

These notes expand the restrictions relevant to the [case study](../README.md).

## Interpretation and generalisation

The original findings broadly followed the expected negative direction, but their small magnitude matters: the study does not support treating gaming time as a strong explanation of socio-emotional differences. The shift for stress resistance is particularly useful for interpreting the research question. An apparently positive unadjusted association did not persist after accounting for gender and parental occupational status. This illustrates why I compared model specifications instead of relying on a single overall correlation.

The findings are compatible with time displacement, but do not establish that displacement occurred. Game content, motives and social settings were not measured by the playtime variable. Two adolescents reporting the same number of hours could have quite different experiences. This is the central distinction I draw between the quantity of gaming and the processes through which it might relate to development.

The international perspective adds descriptive context, not a demonstrated cultural explanation. The figure shows variation in playtime across the retained samples. Country random intercepts allow different baseline competency levels, but do not formally test whether gaming slopes differ by country. Claims about regulation, stigma or cultural norms would require measured contextual variables and a model designed to test them.

## Measurement and model implementation

The cross-sectional, self-reported data do not establish temporal or causal direction. The surviving models do not implement the full PISA survey design or school-level clustering, and country inclusion depends on questionnaire coverage. The original coefficients are historical results whose exact model execution has not been independently reproduced. Item-scoring inconsistencies and the original exclusion-mask implementation require resolution before a new inferential analysis.

The new figure has a verified arithmetic trail, but retains the original imputations and their out-of-range playtime values. It is a corrected descriptive summary of the preserved data, rather than a validation of the imputation model. These limits also mean that the study alone cannot establish benefits or harms of particular games, justify specific playtime thresholds, or demonstrate the effectiveness of an educational intervention.

The surviving preparation code uses nine curiosity items for reliability but ten for the scale mean; the self-control alpha differs between a script comment and the thesis. Minimum-item rules and cross-country measurement comparability have not been newly validated.

The original masks assign zero weight to Austria, Belgium and Costa Rica for all nine outcomes. There are 350,422 positive-weight records in 45 countries per imputation, but the scripts do not explicitly remove null-weight rows from the model frame. This is not a verified fitted-model N. R-squared calculations omit those masks, while coefficient and ICC calculations use them. These implementation differences require resolution before a new inferential analysis.

## Imputation and descriptive calculations

Across ten completed datasets, 95,826 playtime entries fall below zero and 3,890 exceed eight hours (2.6880% of imputation entries, not the percentage of distinct affected people). Several competency scores also exceed their coded 1-5 range. Values were not clipped or replaced. The figure corrects unequal aggregation weights while retaining these limitations. Averaging country SDs would not yield an overall student-level SD.

The historical bivariate summary is not presented as a validated result: it averages individual outcome correlations rather than constructing a composite score, and its root-mean-square SE does not implement Rubin pooling or account for dependencies between outcomes.

The reported age mean of 15.79 years is not confirmed for the preserved analysis variable (mean 16.266206). The denominator for the overall 8.87% missingness claim is unclear. Neither statistic is used in the main case study. Person and school identifiers are absent from the preserved analysis projection, limiting independent verification of individual case alignment.

## Reproducibility boundary

I ran the original imputation on a university server. I did not copy its production code to my personal computer before routine server cleanup; I retained the methods description and imputed data.

The methods description and completed data support downstream checking, but do not confirm the exact executed imputation specification, package versions or convergence diagnostics. An archived run summary cannot be conclusively linked to the analysed files, so its diagnostic values should not be attributed to those files.

The original coefficients remain historical thesis results without independently refitted estimates or newly validated significance tests. The repository reproduces a descriptive figure from aggregates and documents selected R examples. No new imputation or regression fitting was performed. [Methods](methods.md#regenerating-the-descriptive-figure) describes the executable scope; [data provenance](../data/README.md) identifies sources.
