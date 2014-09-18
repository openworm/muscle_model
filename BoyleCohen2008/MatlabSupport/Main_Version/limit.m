%function to limit x to the provided max and min
function output = limit(x, max_val, min_val)

output = max([min([max_val x]) min_val]);