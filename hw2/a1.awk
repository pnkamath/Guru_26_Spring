BEGIN { FS="," }
NR==1 { next }
$NF=="diaporthe-stem-canker"
