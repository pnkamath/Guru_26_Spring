BEGIN { FS="," }

NR==1 {
  for (i=1; i<=NF; i++) h[i]=$i
  next
}

{
  for (i=1; i<=NF; i++) {
    if (!(i in first)) first[i]=$i
    else if ($i != first[i]) bad[i]=1
  }
}

END {
  n=0
  for (i=1; i<=length(h); i++)
    if (!(i in bad)) {
      print h[i]
      n++
    }
  print n > "/dev/stderr"
}
