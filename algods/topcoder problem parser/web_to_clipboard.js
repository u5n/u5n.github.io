let copyToClipboard = function (textToCopy) {
    $("body")
        .append($('<textarea class="textToCopyInput"/></textarea>')
            .val(textToCopy))
        .find(".textToCopyInput")
        .select();

    document.execCommand('copy');
    $(".textToCopyInput").remove();
}

function load_script(src) {
    let e = document.createElement('script');
    e.src = src;
    e.onload = function () {
        console.log(`load script${src}`)
    };
    document.head.appendChild(e);
}

function generate_template(lang = 'c') {
    // $('.dropdown-menu>li>a').eq(2).click()
    let class_name = $('.statement>div').eq(1).children().last().text()
    let method = $('.statement>div').eq(2).children().last().text()
    let paras_type = $('.statement>div').eq(3).children().last().text()
    let return_type = $('.statement>div').eq(4).children().last().text()
    let method_sig = $('.statement>div').eq(5).children().last().text()
    let Examples = $('.statement>div:contains("Examples")').children('div')
    let tests_num = Examples.length
    let paras_num = paras_type.split(',').length
    let tests_paras = Array(tests_num).fill(null).map(e => [])
    let returns = []
    for (let i = 0; i < tests_num; i++) {
        let test_block = Examples.eq(i)
        for (let ii = 0; ii < paras_num; ii++)
            tests_paras[i].push(test_block.find('div>div').eq(ii).text())
        returns.push(test_block.find('div>div:contains("Returns")').text().replace('Returns: ', '').replace(/"/g, "'"))
    }
    res =
        `#include "../lib/m.h"
class ${class_name}{
    public:
    ${method_sig}{
        
        
    }
};

int main(){
    auto E=${class_name}();`
    switch (return_type) {
        case 'vector <int>':
        case 'vector <string>':
        case 'int []':
            for (let i = 0; i < tests_num; i++) {
                res += `
    Da(E.${method}(${tests_paras[i].join(',')}));
    print("except: ${returns[i]}");`
            }
            break
        default:
            for (let i = 0; i < tests_num; i++) {
                dec = i == 0 ? 'auto' : '';
                res += `
    ${dec} res=E.${method}(${tests_paras[i].join(',')});
    print(res==${returns[i]},res,"except: ${returns[i]}");`
            }
    }
    res += `
}
`
    return res
}

res = generate_template()
console.log(res)
copyToClipboard(res)