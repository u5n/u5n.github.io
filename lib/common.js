D=console.log
d = document
$ = d.querySelectorAll.bind(d)
$$ = d.querySelector.bind(d)

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}