BEGIN { FS=", *"; Total=0; classified=0; correct=0; if (wait="") wait=10; if (k=="") k=1; if (m=="") m = 1 }
NR==1 { next }
NR<=wait + 1 { train(); next }
{
  c=classify();
  print $NF","c;
  if (c == $NF){
    correct++;
  }
  classified++;
  train();
}
END {
  printf("Accuracy: %.2f%%\n", (correct/classified)*100)
}
function train(    i,c) {
  Total++; c=$NF; Classes[c]++
  if (Classes[c] == 1){
    NumClasses++
  }
  for(i=1; i<NF; i++) {
    if($i=="?") continue
    Freq[c,i,$i]++
    if(++Seen[i,$i]==1) Attr[i]++ }}

function classify(    i,c,t,best,bestc) {
  best=-1e30
  for(c in Classes) {
    t=log((Classes[c]+m)/(Total + m * NumClasses))
    for(i=1; i<NF; i++) {
      if($i=="?") continue
      t+=log((Freq[c,i,$i]+k)/(Classes[c]+k*Attr[i])) }
    if(t>best) { best=t; bestc=c }}
  return bestc }
