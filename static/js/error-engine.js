// return all classes and ids
let id = (id) => document.getElementById(id);
let classes = (classes) => document.getElementsByClassName(classes);
let username = id('username'),
    password = id('password'),
    form = id('form'),
    
    errorMsg = classes('error'),
    successIcon = classes('success-icon'),
    failureIcon = classes('failure-icon');
