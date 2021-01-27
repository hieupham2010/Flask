$(document).ready(() => {
    var loginForm = document.getElementById("form-login")
    var errorMessage = document.getElementById("errorMessage")
    var sendOTP = document.getElementById("sendOTP")
    loginForm.addEventListener("submit", evt => {
        evt.preventDefault()
        var form = evt.target;
        var email = form.email.value
        var otp = form.OTP.value
        var body = JSON.stringify({
            email: email,
            otp: otp
        })
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = () => {
            if (xhr.readyState === 4 && xhr.status === 200) {
                window.location = xhr.response
            } else if (xhr.readyState === 4 && xhr.status === 10) {
                errorMessage.innerHTML = xhr.response
                sendOTP.innerHTML = "Resend OTP code"
            }
        }
        xhr.open("POST", "/LoginOTP", true);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
        xhr.send(body);
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