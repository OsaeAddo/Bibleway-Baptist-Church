const navItem = document.querySelectorAll('.nav-link');

function linkAction(){
    navItem.forEach(n => n.classList.remove('active')); // Remove 'active' from class of all other items
    this.classList.add('active');   //add 'active' to class of current nav-item
}
navItem.forEach(n => n.addEventListener('click', linkAction));