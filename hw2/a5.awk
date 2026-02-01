BEGIN { FS="," }
NR==1 { print; next }

NR<=10 {
  print
  next
}

$3=="?" { next }

{
  print
}
