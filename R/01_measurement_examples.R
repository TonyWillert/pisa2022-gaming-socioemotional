# Adapted, documented extracts from the 2024 thesis preparation script:
# R-Analyse/Datenaufbereitung 2_0.R (also Datenaufbereitung I.R).
# Functions only: no files read/written; no packages installed.
# Input checks and explicit all-missing handling added for the portfolio.

recode_playtime <- function(code) {
  stopifnot(is.numeric(code))
  invalid <- !is.na(code) & !(code %in% 1:6)
  if (any(invalid)) stop("Expected codes 1:6 or NA.")
  # Historical assumptions: 6.5 is not the midpoint of >5 to 7;
  # 8 is a representative value for an open upper category.
  c(0, 0.5, 2, 4, 6.5, 8)[code]
}

compute_dpt <- function(weekday_code, weekend_code) {
  stopifnot(length(weekday_code) == length(weekend_code))
  (5 * recode_playtime(weekday_code) +
     2 * recode_playtime(weekend_code)) / 7
}

score_assertiveness <- function(items) {
  required <- sprintf("ST305Q%02dJA", 1:10)
  stopifnot(all(required %in% names(items)))
  x <- as.matrix(items[, required, drop = FALSE])
  stopifnot(is.numeric(x))
  if (any(!is.na(x) & !(x %in% 1:5))) {
    stop("Expected item responses 1:5 or NA.")
  }
  reverse <- c("ST305Q04JA", "ST305Q07JA", "ST305Q08JA")
  x[, reverse] <- 6 - x[, reverse]
  score <- rowMeans(x, na.rm = TRUE)
  score[rowSums(!is.na(x)) == 0L] <- NA_real_
  # As in the original mean-score approach, any observed item is sufficient.
  # This illustrates the historical rule, not a newly validated scoring rule.
  score
}
