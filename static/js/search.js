



function single_filters_set_value(){
    filters = document.querySelectorAll('.js-filter-single')
    for (filter of filters){
        
        // changing value only if user selected something
        if (filter.querySelector('.form-select option:checked').value != ''){
            filter.value = filter.id.split('-')[1] + ',' + filter.querySelector('.form-select option:checked').value
        }else{
            filter.value = ''
        }
    }
}


function multi_filters_set_value(){
    filters = document.querySelectorAll('.js-filter-multi')
    for (filter of filters){
        filter.value = filter.id.split('-')[1]
        options_checked = filter.querySelectorAll('.form-check-input')
        for (option of options_checked){
            if (option.checked === true){
                filter.value += ',' + option.value
            }
        }
        if (filter.value == filter.id.split('-')[1]){
            filter.value = ''
        }

    }
}


function range_filters_set_value(){
    filters = document.querySelectorAll('.js-filter-range')
    for (filter of filters){
        min = filter.querySelector('.js-filter-min').value
        max = filter.querySelector('.js-filter-max').value
        console.log('hey')

        // changing value only if user has entered something
        if (min != '' || max != ''){
            filter.value = filter.id.split('-')[1] + ',' + min + ',' + max
        }else{
            filter.value = ''
        }
    }
}

function get_values(){
    single_filters_set_value()
    multi_filters_set_value()
    range_filters_set_value()

    filters = document.querySelectorAll('.js-filter')
    value = ''
    for (filter of filters){        
        if (filter.value != ''){
            value += filter.value + '&'
        }
    }
    return value
}

function form_url(){
    url_params = get_values()
    url_params = '?' + url_params.replace(/^&+|/, "").replace(/&+$/, "")
    console.log(url_params)
    url = window.location.href.split('?')[0] + url_params
    console.log(url)
    window.location = url
}

document.querySelector('#submit-filters').addEventListener('click', form_url)

