BEGIN{FS=","}
NR==1{next}
{rows[$0]++;line[NR]=$0}
END{for(i=2;i<=NR;i++)if(rows[line[i]]>1){print i;n++}print n>"/dev/stderr"}
