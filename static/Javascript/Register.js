$(document).ready(() => {
    var loginForm = document.getElementById("form-login")
    var errorMessage = document.getElementById("errorMessage")
    loginForm.addEventListener("submit", evt => {
        evt.preventDefault()
        var form = evt.target;
        var email = form.email.value
        var password = form.password.value
        var confirmPassword = form.password_confirm
        var format = /^[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]*$/;
        if (password.length < 8 || confirmPassword.length < 8) {
            errorMessage.innerHTML = "Password less than 8 character";
        } else if (!checkUpperCase(password)) {
            errorMessage.innerHTML = "Your password must contain at least one capital letter";
        } else if (password.match(format)) {
            errorMessage.innerHTML = "Your password must contain at least one special character";
        } else if (password !== confirmPassword) {
            errorMessage.innerHTML = "Your password does not match with confirm password"
        } else {
            var body = JSON.stringify({
                email: email,
                password: password
            })
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = () => {
                if (xhr.readyState === 4 && xhr.status === 401) {
                    errorMessage.innerHTML = xhr.response
                    form.email.value = ""
                    form.password.value = ""
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