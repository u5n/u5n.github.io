/*
1-
1+

1_ 1/4
1= 4

1+_  1*1/4


*/
function lexical_ana(a){
    let tone=0
    let sharp=0
    let quarter=1
    if(a){
        if (a[0]=='-')
            tone=-1
        else if(a[0]=='+')
            tone=1
        else if(a[0]=='_')
            quarter=1/2
        else if(a[0]=='=')
            quarter=2
        else if(a[0]=='#')
            sharp=1
        
        if(a.length==2){
            if(a[1]=='_')
                quarter=1/2
            else if(a[1]=='=')
                quarter=2
        }
    }
    return [tone,sharp,quarter]
    
}
