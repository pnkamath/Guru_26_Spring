BEGIN { FS=", *" }
NR==1 { next }
{
  cnt[$2]++
}
END {
  max=0
  for (v in cnt) {
    if (cnt[v] > max) {
      max = cnt[v]
      best = v
    }
  }
  print best, max
}
