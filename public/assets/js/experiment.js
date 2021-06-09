let select = document.getElementById('method')
let random = document.getElementById('random')
let equable = document.getElementById('equable')

select.onchange = (event) => {
    let selected = event.target.value
    switch (selected) {
        case 'Метод ближайшего соседа': {
            select.parentElement.parentElement.after(getKNeighborsParams())
            document.getElementById('hiddenMethod').value = 'KNeighbors'
            break
        }
    }
}

random.addEventListener('click', function () {
    equable.checked = random.checked !== true;
})

equable.addEventListener('click', function () {
    random.checked = equable.checked !== true;
})

function getKNeighborsParams() {
    let div = document.createElement('div')
    let label = document.createElement('label')
    label.textContent = 'Параметр k - количество соседей'
    let k = document.createElement('input')
    k.name = 'k'
    k.type = 'number'
    k.required = false
    k.min = '0'
    label.appendChild(k)
    div.appendChild(label)
    return div
}

