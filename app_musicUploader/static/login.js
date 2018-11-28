// Get the modal
var loginModal = document.getElementById('loginModal');
var signupModal = document.getElementById('signupModal');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event){
    if (event.target == loginModal || event.target == signupModal) {
        loginModal.style.display = "none";
        signupModal.style.display = "none";
    }
};

