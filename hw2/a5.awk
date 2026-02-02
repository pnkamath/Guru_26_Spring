BEGIN { FS=", *" }
NR==1 { next }

NR<=11 {
  print $0
  next
}

$3=="?" { next }

{
  print $0
}
