// check current url 
let maxsz = Object.keys(map_id_name).length;
let url = new URL(window.location.href);
let c = url.searchParams.get("id");
if (c !== null) {
    window.location.href = id_to_url(c);
}

function inputkeyUpFunc(obj) {
    if (obj.value > maxsz) {
        obj.value = maxsz;
    }
    let hyperlink = document.getElementById("input-id-link");
    if (obj.value in map_id_name) {
        hyperlink.text = map_id_name[obj.value];
        hyperlink.href = id_to_url(obj.value);
    } else {
        hyperlink.text = "";
    }
}

// search only when input text change 
// lru_cache with size 1
let prePattern;
function searchKeyUpFunc(obj) {
    let pattern = obj.value.trim().toLowerCase();
    if (pattern === prePattern) {
        prePattern = pattern;
        return;
    } else {
        prePattern = pattern;
    }
    let tbody = document.querySelector("#search-result-table>tbody");
    tbody.innerHTML = "";
    if (pattern === "") return;

    let resultArr = filterNames(pattern);

    for (let res of resultArr) {
        let id = res[0];
        let newRow = tbody.insertRow();
        let Col0 = newRow.insertCell();
        let Col1 = newRow.insertCell();
        Col0.appendChild(document.createTextNode(id));
        problemlink = document.createElement('a');
        problemlink.href = id_to_url(id);
        // problem link innerHTML
        let plIH = map_id_name[id].replaceAll('-', ' ');
        if (res.length == 4) {
            let [_, l, m, r] = res;
            plIH = plIH.slice(0, l) +
                "<span class='burlywood'>" + plIH.slice(l, m) + "</span>" +
                "<span class='burlywoodDeep'>" + plIH[m] + "</span>" +
                "<span class='burlywood'>" + plIH.slice(m + 1, r) + "</span>" +
                plIH.slice(r);
        } else if (res.length == 3) {
            let [_, l, r] = res;
            plIH = plIH.slice(0, l) +
                "<span class='burlywood'>" + plIH.slice(l, r) + "</span>" +
                plIH.slice(r);
        } else {
            let diffIdx = res[1];
            let newplIH = plIH.slice(0, diffIdx[0] + 1);
            let diffIdx_sz = diffIdx.length;
            for (let i = 0; i <= diffIdx_sz - 2; i += 1) {
                newplIH += "<span class='burlywood'>" + plIH.slice(diffIdx[i] + 1, diffIdx[i + 1]) + "</span>";
                if (i !== diffIdx_sz - 2)
                    newplIH += "<span class='burlywoodDeep'>" + plIH[diffIdx[i + 1]] + "</span>";
            }
            newplIH += plIH.slice(diffIdx[diffIdx_sz - 1]);
            plIH = newplIH;
        }
        problemlink.innerHTML = plIH;
        Col1.appendChild(problemlink);
    }
}

function filterNames(pattern) {
    let n = pattern.length;
    let resultArr = [];
    // match prefix
    if (n <= 2) {
        for (let id = 1; id <= maxsz; id += 1) {
            let name = map_id_name[id];
            if (name.startsWith(pattern)) {
                resultArr.push([id, 0, n]);
            }
        }
    }
    // regular expression
    else if( pattern[0]==='/' && pattern[n-1]==='/'){
        let re;
        try{
            re = new RegExp(pattern.slice(1,n-1));
        } catch(err){
            console.log(err)
            return resultArr;
        }
        for (let id = 1; id <= maxsz; id += 1) {
            let target = map_id_name[id].replaceAll('-',' ');
            let matchres = target.match(re);
            if(matchres!==null){
                resultArr.push([id, matchres.index, matchres.index + matchres[0].length]);
            }
        }
    } 
    // similar match 
    else {
        // check if b is substring of map_id_name.values
        let checked = Array(maxsz + 1);
        let re = new RegExp(pattern.replace('*','[a-zA-Z0-9 ]'));
        for (let id = 1; id <= maxsz; id += 1) {
            let target = map_id_name[id].replaceAll('-',' ');
            let matchres = target.match(re);
            if (matchres !== null) {
                resultArr.push([id, matchres.index, matchres.index + matchres[0].length]);
                checked[id] = 1;
            }
        }

        // add at most 1 char
        // check if b is substring of map_id_name.values
        for (let i = 0; i <= n; i += 1) {
            let pat_add = pattern.slice(0, i) + '[a-zA-Z0-9 ]' + pattern.slice(i);
            let re = new RegExp(pat_add.replace('*','[a-zA-Z0-9 ]'));
            for (let id = 1; id <= maxsz; id += 1) {
                if (checked[id] === 1) continue;
                let target = map_id_name[id].replaceAll('-',' ');
                let matchres = target.match(re);
                if (matchres !== null) {
                    resultArr.push([id, matchres.index, matchres.index + i, matchres.index + matchres[0].length]);
                    checked[id] = 1;
                }
            }
        }
        
        // O(maxsz*m*n)
        // refer to function of sub_hamming, simulate multiple substitute operation
        for (let id = 1; id <= maxsz; id += 1) {
            if (checked[id] === 1) continue;
            let target = map_id_name[id].replaceAll('-',' ');
            let [sz, diffIdx] = sub_hamming(target, pattern);
            if (sz / n >= 0.8) resultArr.push([id, diffIdx]);
        }
    }
    return resultArr;
}


/* 
    string utility 
*/


// allow asterisk in pattern string
function isEqual(c1, c2) {
    return c1 === c2 || (c2 === '*');
}

function sub_hamming(a, b) {
    // find substring of a @ asub, substring of b @ bsub, 
    // that has mininum `a.length-hamming_distance(asub,bsub)`
    // O(mn), O(min(m,n))
    let m = a.length, n = b.length;
    let diffIdx; // index of different chars
    let bestDiffIdx; // best `diffIdx`
    let match = 0; // length of `minDiffIdx`
    for (let shi = -m + 1; shi < n; shi += 1) {
        let l = Math.max(-shi, 0), r = Math.min(n - shi, m);
        diffIdx = [l - 1];
        for (let i = l; i < r; i += 1) {
            if (!isEqual(a[i], b[i + shi])) {
                diffIdx.push(i);
            }
        }
        diffIdx.push(r);
        if (r - l - diffIdx.length + 2 > match) {
            match = r - l - diffIdx.length + 2;
            bestDiffIdx = diffIdx;
        }
    }
    return [match, bestDiffIdx];
}
