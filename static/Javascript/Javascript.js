$(document).ready(() => {
    var loginForm = document.getElementById("form-login")
    var errorMessage = document.getElementById("errorMessage")
    var forgot = document.getElementById("ForgotPassword")
    loginForm.addEventListener("submit", evt => {
        evt.preventDefault()
        var form = evt.target;
        var email = form.email.value
        var password = form.password.value
        var format = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+/;
        if (password.length < 8) {
            errorMessage.innerHTML = "Password less than 8 character";
        } else if (!checkUpperCase(password)) {
            errorMessage.innerHTML = "Your password must contain at least one capital letter";
        } else if (!format.test(password)) {
            errorMessage.innerHTML = "Your password must contain at least one special character";
        } else {
            var body = JSON.stringify({
                email: email,
                password: password
            })
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = () => {
                if (xhr.readyState === 4 && xhr.status === 10) {
                    errorMessage.innerHTML = xhr.response
                    form.email.value = ""
                    form.password.value = ""
                    forgot.innerHTML = "Forgot password?"
                } else if (xhr.readyState === 4 && xhr.status === 200) {
                    window.location = xhr.response
                    console.log(xhr.response)
                }
            }
            xhr.open("POST", "/", true);
            xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
            xhr.send(body);
        }
        return;
    })
})

function checkUpperCase(pass) {
    for (i = 0; i < pass.length; i++) {
        if (pass.charAt(i) === pass.charAt(i).toUpperCase()) {
            return true;
        }
    }
    return false;
}