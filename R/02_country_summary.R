# Portfolio recalculation: equal weights across all ten imputations.
# Adapted from Forrestplot dpt.R; replaces its recursive pairwise averaging.
# Run from repository root: Rscript R/02_country_summary.R
# Aggregate inputs only. No microdata, imputation or model fitting.

by_imputation <- read.csv("data/derived/dpt_country_by_imputation.csv")
stopifnot(nrow(by_imputation) == 480L,
          length(unique(by_imputation$cid)) == 48L,
          all(is.finite(by_imputation$mean_dpt)),
          !anyDuplicated(by_imputation[c("cid", "imp")]))
groups <- split(by_imputation$imp, by_imputation$cid)
stopifnot(all(vapply(groups, function(x) {
  identical(sort(as.integer(x)), 1:10)
}, logical(1))))
country_means <- aggregate(
  mean_dpt ~ cid + country, data = by_imputation, FUN = mean
)
country_means <- country_means[
  order(-country_means$mean_dpt, country_means$country),
]
country_means$rank <- seq_len(nrow(country_means))
dir.create("results/tables", recursive = TRUE, showWarnings = FALSE)
# Separate output allows comparison with the Python-generated figure table.
write.csv(country_means, "results/tables/daily_playtime_R.csv", row.names = FALSE)
