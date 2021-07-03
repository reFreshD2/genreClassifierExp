let select = document.getElementById('method')
let random = document.getElementById('random')
let equable = document.getElementById('equable')
let method = document.getElementById('hiddenMethod')
let params = document.getElementById('params')

select.onchange = (event) => {
    let selected = event.target.value
    switch (selected) {
        case 'Метод ближайшего соседа': {
            params.innerHTML = ""
            params.append(getKNeighborsParams())
            method.value = 'KNeighbors'
            break
        }
        case 'Метод ближайшего соседа с убывающими весами': {
            params.innerHTML = ""
            params.append(getKneighborsWeightParams())
            method.value = 'KNeighborsWeight'
            break
        }
        case 'Метод парзенова окна': {
            params.innerHTML = ""
            params.append(getParzenParams())
            method.value = 'Parzen'
            break
        }
        case 'Бинарное решающее дерево': {
            params.innerHTML = ""
            params.append(getDecisionTreeParams())
            method.value = 'DecisionTree'
            break
        }
        case 'Решающие леса': {
            params.innerHTML = ""
            params.append(getRandomForestParams())
            method.value = 'RandomForest'
            break
        }
        case 'Метод опорных векторов': {
            params.innerHTML = ""
            params.append(getSVCParams())
            method.value = 'SVC'
            break
        }
        case 'Метод градиентного спуска': {
            params.innerHTML = ""
            params.append(getSGDParams())
            method.value = 'SGD'
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

function getNumberInput(type, name, labelTitle) {
    let label = document.createElement('label')
    label.textContent = labelTitle
    let num = document.createElement('input')
    num.name = name
    num.type = 'number'
    num.min = '0'
    if (type === 'float') {
        num.step = 'any'
    }
    label.appendChild(num)
    return label
}

function getSelect(options, labelTitle) {
    let label = document.createElement('label')
    label.textContent = labelTitle
    let select = document.createElement('select')
    let optSelect = document.createElement('option')
    optSelect.textContent = 'Выберите значение'
    optSelect.disabled = true
    optSelect.selected = true
    select.append(optSelect)
    options.forEach(value => {
        let opt = document.createElement('option')
        opt.textContent = value
        select.append(opt)
    })
    label.append(select)
    return label
}

function getHidden(name) {
    let hidden = document.createElement('input')
    hidden.hidden = true
    hidden.id = name
    hidden.name = name
    return hidden
}

function getKNeighborsParams() {
    let div = document.createElement('div')
    let number = getNumberInput('int', 'k', 'Параметр k - количество соседей')
    div.appendChild(number)
    return div
}

function getKneighborsWeightParams() {
    let div = getKNeighborsParams()
    let opts = ['Линейная', 'Экспоненциальная']
    let select = getSelect(opts, 'Функция весов')
    let weight = getHidden('weight')
    select.children.item(0).onchange = (event) => {
        let selected = event.target.value
        switch (selected) {
            case 'Линейная': {
                document.getElementById('weight').value = 'linear'
                break
            }
            case 'Экспоненциальная': {
                document.getElementById('weight').value = 'exp'
                break
            }
        }
    }
    let newDiv = document.createElement('div')
    newDiv.append(div, select, weight)
    return newDiv
}

function getParzenParams() {
    let div = document.createElement('div')
    let h = getNumberInput('float', 'h', 'Параметр h - ширина окна')
    let opts = ['E-Ядро', 'P-Ядро', 'T-Ядро', 'Q-Ядро']
    let select = getSelect(opts, 'Функция ядра')
    let hidden = getHidden('kernel')
    select.children.item(0).onchange = (event) => {
        let selected = event.target.value
        switch (selected) {
            case 'E-Ядро': {
                document.getElementById('kernel').value = 'E'
                break
            }
            case 'P-Ядро': {
                document.getElementById('kernel').value = 'P'
                break
            }
            case 'T-Ядро': {
                document.getElementById('kernel').value = 'T'
                break
            }
            case 'Q-Ядро': {
                document.getElementById('kernel').value = 'Q'
                break
            }
        }
    }
    let divH = document.createElement('div')
    divH.append(h)
    let divSelect = document.createElement('div')
    divSelect.append(select)
    div.append(divH, divSelect, hidden)
    return div
}

function getDecisionTreeParams() {
    let depth = getNumberInput('int', 'depth', 'Параметр depth - глубина дерева')
    let opts = ['Джини', 'Энтропия']
    let select = getSelect(opts, 'Критерий информативности')
    let hidden = getHidden('criteria')
    select.children.item(0).onchange = (event) => {
        let selected = event.target.value
        switch (selected) {
            case 'Джини': {
                document.getElementById('criteria').value = 'gini'
                break
            }
            case 'Энтропия': {
                document.getElementById('criteria').value = 'entropy'
                break
            }
        }
    }
    let div = document.createElement('div')
    let divDepth = document.createElement('div')
    let divSelect = document.createElement('div')
    divSelect.append(select)
    divDepth.append(depth)
    div.append(divDepth, divSelect, hidden)
    return div
}

function getRandomForestParams() {
    let divDecision = getDecisionTreeParams()
    let nEst = getNumberInput('int', 'nEstimators', 'Параметр nEstimators - количество деревьев')
    let div = document.createElement('div')
    div.append(nEst)
    divDecision.append(div)
    return divDecision
}

function getSVCParams() {
    let C = getNumberInput('float', 'C', 'Параметр C - регулирующий параметр')
    let opts = ['Линейное', 'Полиномиальное', 'RBF-Ядро', 'Сигмоид']
    let select = getSelect(opts, 'Функция ядар')
    let kernel = getHidden('kernel')
    select.children.item(0).onchange = (event) => {
        let selected = event.target.value
        switch (selected) {
            case 'Линейное': {
                document.getElementById('kernel').value = 'linear'
                break
            }
            case 'Полиномиальное': {
                document.getElementById('kernel').value = 'poly'
                break
            }
            case 'RBF-Ядро': {
                document.getElementById('kernel').value = 'rbf'
                break
            }
            case 'Сигмоид': {
                document.getElementById('kernel').value = 'sigmoid'
                break
            }
        }
    }
    let div = document.createElement('div')
    let divC = document.createElement('div')
    let divSelect = document.createElement('div')
    divC.append(C)
    divSelect.append(select)
    div.append(divC, divSelect, kernel)
    return div
}

function getSGDParams() {
    let optLoss = ['Шарнир', 'Логарифчиская', 'Модифицированный хубер', 'Квадратный шарнир', 'Перцептрон']
    let selectLoss = getSelect(optLoss, 'Функция потерь')
    let loss = getHidden('loss')
    selectLoss.children.item(0).onchange = (event) => {
        let selected = event.target.value
        switch (selected) {
            case 'Шарнир': {
                document.getElementById('loss').value = 'hinge'
                break
            }
            case 'Логарифчиская': {
                document.getElementById('loss').value = 'log'
                break
            }
            case 'Модифицированный хубер': {
                document.getElementById('loss').value = 'modified_huber'
                break
            }
            case 'Квадратный шарнир': {
                document.getElementById('loss').value = 'squared_hinge'
                break
            }
            case 'Перцептрон': {
                document.getElementById('loss').value = 'perceptron'
                break
            }
        }
    }
    let optPenalty = ['l1', 'l2', 'elasticnet']
    let selectPenalty = getSelect(optPenalty, 'Функция штрафов')
    let penalty = getHidden('penalty')
    selectPenalty.children.item(0).onchange = (event) => {
        let selected = event.target.value
        switch (selected) {
            case 'l1': {
                document.getElementById('penalty').value = 'l1'
                break
            }
            case 'l2': {
                document.getElementById('penalty').value = 'l2'
                break
            }
            case 'elasticnet': {
                document.getElementById('penalty').value = 'elasticnet'
                break
            }
        }
    }
    let div = document.createElement('div')
    let divLoss = document.createElement('div')
    let divPenalty = document.createElement('div')
    divLoss.append(selectLoss)
    divPenalty.append(selectPenalty)
    div.append(divLoss, divPenalty, loss, penalty)
    return div
}
