{
  if (NR > 1){
    arr[$NF, $1]++
  }
}
END {
  for (k in arr){
    split(k, parts, SUBSEP)
    print parts[1], parts[2], arr[k]
  }
}
