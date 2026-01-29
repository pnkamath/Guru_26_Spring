{
  if (NR > 1){
    arr[$NF]++
  }
}
END {
  for (c in arr){
    print c, arr[c]
    }  
}
