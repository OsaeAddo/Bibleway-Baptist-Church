var loader;


let loadNow = (opacity)=> {
    if (opacity <= 0){
        displayContent()
    }else {
        loader.style.opacity = opacity
        window.setTimeout(
            function() {
                loadNow(opacity - 0.01)
            }, 85
        )
    }
}

let displayContent = ()=> {
    loader.style.display = 'none'
    document.getElementById('content').style.display = 'block'
}

document.addEventListener("DOMContentLoaded", function() {
    loader = document.getElementById('loader')
    loadNow(1)
})