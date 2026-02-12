BEGIN { FS = ","}
{ for (i=1;i<=NF;i++) if ($i ~ /\?/) { rows[NR]=1; cols[i]=1 } }
END {
  print "COL_COUNT:"length(cols); print "ROW_COUNT:"length(rows)
  for (c in cols) print "COL:"c
  for (r in rows) print "ROW:"r
}
