BEGIN{
  FS=", *"
  n = 0
}
NR==1 { next }
{
  arr[$NF]++
  n++
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
