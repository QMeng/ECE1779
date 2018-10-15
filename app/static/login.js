// Get the modal
var loginModal = document.getElementById('loginModal');
var signupModal = document.getElementById('signupModal');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal||event.target == modal2){
        loginModal.style.display = "none";
        signupModal.style.display = "none";
    }
};

