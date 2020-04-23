# Pretzel Logic: Retention Benchmarking

## menu_name
Name of menu item. Default to Study menu. (Requires restart)

## display_mode
Allows quickly changing of display views.  
Options include:  
full: default  
quick: display 1 level of young/mature only.  
classic: Emulates the original "True Retention" for those who don't like too much stats.  


## stylesheet
Path and filename of stylesheet to use.

## failed_grade
Set the failed grade for your reviews.  
Custom schedulers such as Plan9 or Plan0 may use grade 2 as the failing grade.

## pass_threshold
Only calculates retention when this value has been met.

## highlight_threshold
Highlights retention if passing count is met.

## custom_ivl_range_between
Specifefy an interval range to check on.  
It's an array or array, so add and remove as needed.  
from-to,from-to...

## interval_range
Segments the intervals into young and mature.  
Added and remove as necessary.

## timeframe
Divides frames into mutiple timeframes starting from today to a week, a month, a year, etc...

## start_day_offset
Offsets the starting day. This allows users to peek into a specific date range.  
An offset of 7 with a 1 week timeframe will return the stats for week 2 or days 8-14.  

