D=console.log
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function load_script(src){
    let e=document.createElement('script');
    e.src=src;
    e.onload=function(){
        console.log(`load script${src}`)
    };
    document.head.appendChild(e);
}