document.addEventListener('DOMContentLoaded', function(){
    document.querySelector('#profile').addEventListener('click', function(){
        document.querySelector('#profile-view').style.opacity = '100%';
        document.querySelector('#profile-view').style.width = '40%';
        document.querySelector('#profile-view').style.height = '75%';
        document.querySelector('#food').style.opacity = '30%';
        document.querySelector('#weight').style.opacity = '30%';
    })
    document.querySelector('#profile-view svg').addEventListener('click', function(){
        document.querySelector('#profile-view').style.opacity = '0';
        document.querySelector('#profile-view').style.width = '0';
        document.querySelector('#profile-view').style.height = '0';
        document.querySelector('#food').style.opacity = '100%';
        document.querySelector('#weight').style.opacity = '100%';
    })
})