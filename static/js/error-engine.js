// return all classes and ids
let id = (id) => document.getElementById(id);
let classes = (classes) => document.getElementsByClassName(classes);
let username = id('username'),
    password = id('password'),
    form = id('form'),
    
    errorMsg = classes('error'),
    successIcon = classes('success-icon'),
    failureIcon = classes('failure-icon');

// add event listener to the form's submit button
form.addEventListener("submit", (e) => {
    e.preventDefault();
    
    // implement form validation engine
    engine(username, 0, "Username cannot be blank");
    engine(password, 2, "Password cannot be blank");
})

