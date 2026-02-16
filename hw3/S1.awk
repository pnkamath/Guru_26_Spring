BEGIN { FS=","; len=0; n=0}
NR == 1 { len = NF}
NF != len {n++;print NR}
END { print n > "/dev/stderr"}
