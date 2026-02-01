BEGIN {
  FS=","
  srand()
}

NR==1 { next }

{
  n++
  if (n <= 20) {
    R[n] = $0
  } else {
    j = int(rand()*n) + 1
    if (j <= 20)
      R[j] = $0
  }
}

END {
  for (i=1; i<=20; i++)
    print R[i]
}
