const passwordU = document.getElementById('id_password');
const togglePassword = document.getElementById('showPassword');

togglePassword.addEventListener('change', (e) => {
    if (togglePassword.checked){
        passwordU.setAttribute('type', 'text');
    }else{
        passwordU.setAttribute('type', 'password');
    }
});