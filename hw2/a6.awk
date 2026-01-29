BEGIN{
  n = 0
}
{
  if (NR > 1){
    arr[$NF]++
    n++
  }
}

END{
  entropy(arr, n)
}

function  entropy(arr, n){
  for (i in arr){
    s += (arr[i] / n) * log(arr[i] / n)
  }
  print s * -1
}
