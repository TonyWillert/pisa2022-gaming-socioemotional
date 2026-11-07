# Methods and analytical details

These notes expand the [case study](../README.md) and distinguish the documented thesis approach from later portfolio corrections.

## Data and coverage

I used the [OECD PISA 2022 database](https://www.oecd.org/en/data/datasets/pisa-2022-database.html), combining questionnaire responses on gaming with socio-emotional items and background characteristics. The retained analysis data contain **370,972 student records from 48 countries and regions in each of ten imputed datasets**. These are ten completed versions of the analysis sample, not ten independent samples.

Country selection followed the availability of gaming and socio-emotional measures: countries without gaming information or without socio-emotional measurement altogether were excluded. Austria and Belgium remained in the descriptive sample, although emotional control and trust were not collected there. These structurally missing scales require separate treatment in outcome analyses. The exact retained country IDs and sample sizes are supplied in [the country-selection table](../data/derived/countries.csv).

The 370,972 records describe the overall retained sample. Outcome coverage and the implementation of model-specific exclusions mean that this is not a verified sample size for every fitted regression.

## Measurement, imputation and models

**Daily playtime.** I combined weekday (`IC177Q01JA`) and weekend (`IC178Q01JA`) gaming responses into an approximate daily-hours measure. Weighting weekdays five times and weekend days twice gives each day of the week equal weight:

```r
# Original thesis coding, retained explicitly for comparability.
hours <- c(0, 0.5, 2, 4, 6.5, 8)
weekday_hours <- hours[weekday_code]
weekend_hours <- hours[weekend_code]
dpt <- (5 * weekday_hours + 2 * weekend_hours) / 7
```

The category representatives are approximations, not exact measured durations. In particular, the original assignment of 6.5 hours to the over-five-to-seven-hour category is not its midpoint; eight hours represents an open upper category. I retain these assumptions here to keep the descriptive calculation comparable with the thesis. A robust implementation and an example of reverse-coding and scoring assertiveness are in [the measurement examples](../R/01_measurement_examples.R).

**Socio-emotional competencies.** I analysed assertiveness, curiosity, emotional control, stress resistance, empathy, trust, cooperation, self-control and perseverance separately. Negatively worded items were reversed so that higher scale means indicate more of the relevant competency. Item means offer an interpretable scale, but their reliability and cross-country comparability remain measurement considerations; this portfolio does not claim to have revalidated the scales.

**Missing data.** Before imputation, 20.48% of daily playtime values, 13.12% of emotional-control scores, 12.28% of trust scores and 12.03% of HISEI values were missing in the retained sample. I chose multiple imputation to retain information beyond complete cases and represent uncertainty about missing values. Its usefulness depends on the missing-data assumptions and a sufficiently specified imputation model; it does not guarantee the removal of bias. The thesis describes joint multilevel imputation using `jomo`/`mitml`, a country random intercept and auxiliary information on achievement, migration, mathematics self-efficacy, safety and bullying. Ten completed datasets survive. The original server production code is unavailable, so the exact executed imputation specification and its diagnostics cannot be fully verified.

**Multilevel models.** Students share country contexts. A country random intercept allows baseline competency levels to differ rather than treating every observation as independent. I compared an unadjusted specification with one including gender and HISEI, the highest parental occupational-status index. These covariates address differences in student background that could contribute to the apparent gaming association:

```r
unadjusted <- competency ~ dpt + (1 | cid)
adjusted   <- competency ~ dpt + hisei + gender + (1 | cid)
```

The thesis describes fitting models separately to the imputed datasets and using `mitml::testEstimates()` for Rubin pooling. Standardised versions of the outcome, playtime and HISEI supported comparison of coefficient magnitudes. These are country random-intercept models, not an explicit separation of within-country and between-country slopes. [The model example](../R/03_model_specification.R) documents the specification without running a new analysis.

## Descriptive recalculation

### Descriptive context, recalculated for this case study

**Figure 1.** Mean daily playtime in the retained country and region samples. This portfolio calculation gives each of the ten imputation-specific means equal weight, correcting unequal imputation weighting in the original plotting script. Points are descriptive means, with no confidence intervals. Country samples are unweighted; they should not be interpreted as population rankings. Source: preserved thesis analysis data; [480 aggregate input rows](../data/derived/dpt_country_by_imputation.csv), [48 plotted values](../results/tables/daily_playtime.csv), and [figure script](../scripts/make_figure.py).

Under this corrected aggregation, country means range from **1.69 hours in Spain to 3.09 hours in Albania**. Their equal-country average is **2.32 hours**. Averaging over student records within each imputation instead gives **2.26 hours**: the two summaries answer different questions because country samples differ in size. Neither is a survey-weighted worldwide estimate.

The figure uses the preserved imputations without clipping or replacing their values. Approximately 2.69% of playtime entries across the ten completed datasets fall outside the original coded 0–8-hour range. This limits the plausibility of the descriptive estimates and is a reason to avoid fine country comparisons. The recalculation corrects the aggregation step; it does not repair or rerun the imputation.

The corrected calculation is deliberately explicit:

```r
# One input row per country and imputation; ten rows per country.
country_means <- aggregate(
  mean_dpt ~ cid + country, data = by_imputation, FUN = mean
)
```

[The executable summary example](../R/02_country_summary.R) reads the included aggregate data. Averaging country SDs would not provide an overall student-level SD, so no such value is presented as a global dispersion measure.

## Regenerating the descriptive figure

To regenerate the figure and its table from the included aggregates, run from the repository root:

```sh
python -m pip install -r requirements-figure.txt
python scripts/make_figure.py
```

The corresponding base-R summary can be regenerated with `Rscript R/02_country_summary.R`. See [data provenance and scope](../data/README.md) for the original-versus-recalculated distinction and the source documents. Individual-level data and the unredacted thesis are not included.


The Python figure pipeline was executed and checked against the existing audit calculations. The R examples were statically reviewed but not executed because no local R runtime was available. They are documented adaptations rather than a recovered end-to-end production pipeline. Further constraints are described in [limitations](limitations.md).
