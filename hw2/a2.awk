BEGIN { FS=", *" }

NR==1 { next }
{
    arr[$NF]++
}
END {
  for (c in arr){
    print c, arr[c]
    }
}
