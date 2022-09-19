const email = document.getElementById('sign-up-email')
const pass1 = document.getElementById('id_password1')
const pass2 = document.getElementById('id_password2')

function sign_up_validation() {

    var error_invalid_email = ''
    var error_short_pass = ''
    var error_notmatching_pass = ''

    if (email.value === ""){
        email.classList.add("invalid")
        error_invalid_email = 'Enter valid email address'
    } else {
        email.classList.remove('invalid')
    }

    if (pass1.value.length < 8) {
        pass1.classList.add('invalid')
        error_short_pass = 'minimum 8 characters'
        document.getElementById('pass1-error').classList.remove('black')
    } else{
        pass1.classList.remove('invalid')
        document.getElementById('pass1-error').classList.add('black')
    }

    if (pass1.value !== pass2.value){
        pass2.classList.add('invalid')
        error_notmatching_pass = "passwords don't match"
        document.getElementById('pass2-error').innerHTML = error_notmatching_pass
    } else {
        pass2.classList.remove('invalid')
    }
    if (error_invalid_email || error_short_pass || error_notmatching_pass !== "") {
        return false
    } else {

        return true
    }
}

$("#sign-up-modal").on("hidden.bs.modal", function () {
    email.classList.remove('invalid')
    pass1.classList.remove('invalid')
    pass2.classList.remove('invalid')
});


function sign_up_form_submit() {   

    $(window).click (function(e) { 

        if ($(e.target).hasClass('submit-sign-up-form')){
            console.log('! here')
            current_page = window.location.href
            e.preventDefault();
            if (sign_up_validation()){
                
                email_val = email.value;        
                $.ajax({
                    type: 'GET',
                    url: '/users/registration-validation/',
                    data: {
                    email_val: email_val,
                    current_page: current_page,
                    action: 'GET'
                    },
                    success: function(json) {
                    if(json['result'].length === 0){
                        document.getElementById("sign-up-form").submit();
                    } else {
                        document.getElementById('sign-up-email-error').innerHTML = json['result'][0]
                        email.classList.add('invalid')
                    } 
                    },
                    error: function (request, type, errorThrown) {
                        $('#sign-up-form').html(request.responseText);
                    }
                });
            };
        }
    });
}
