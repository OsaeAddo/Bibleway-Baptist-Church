let password = document.querySelector('{{form.password.id_for_label}}');

togglePassword.addEventListener('change', (e) => {
    if (togglePassword.checked){
        passwordU.setAttribute('type', 'text');
    }else{
        passwordU.setAttribute('type', 'password');
    }
});