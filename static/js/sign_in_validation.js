const email_login = document.getElementById('id_username')
const pass_login = document.getElementById('id_password')

$("#sign-in-modal").on("hidden.bs.modal", function () {
    email_login.classList.remove('invalid')
    pass_login.classList.remove('invalid')
});

function sign_in_form_submit() {   

    $(window).click (function(e) { 
        if ($(e.target).hasClass('submit-sign-in-form')){
            e.preventDefault();
            
            email_val = email_login.value; 
            pass_val = pass_login.value;      
            $.ajax({
                type: 'GET',
                url: '/users/login-validation/',
                data: {
                    email_val: email_val,
                    pass_val: pass_val,
                    // csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    action: 'GET'

                },
                success: function(json) {
                    if (json['result'] === 'success'){
                        document.getElementById('sign-in-form').submit()
                    }else if (json['result'] === 'failed') {
                        email_login.classList.add('invalid')
                        pass_login.classList.add('invalid')
                    }
                },
                
            });
        };
    })
}