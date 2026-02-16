BEGIN{FS=","}
NR==1{for(i=1;i<=NF;i++)h[i]=$i;next}
{for(i=1;i<=NF;i++)if(!(i in f))f[i]=$i;else if($i!=f[i])b[i]}
END{for(i=1;i<=length(h);i++)if(!(i in b)){print h[i];n++}print n>"/dev/stderr"}
