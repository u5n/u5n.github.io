/*
1-
1+

1__ 1/4
1== 4

1+__ 1* 1/4


*/
function lexical_ana(a){
    let tone=0
    let quarter=1
    if(a){
        if (a[0]=='-')
            tone=-1
        else if(a[0]=='+')
            tone=1
        else if(a[0]=='_')
            quarter=1/2
            D([tone,quarter])
    }
    return [tone,quarter]
    
}