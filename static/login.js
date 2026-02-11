const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');

registerLink.addEventListener('click', () => {
    wrapper.classList.add('active');
});

loginLink.addEventListener('click', () => {
    wrapper.classList.remove('active');
});

// register form submission
document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var email = document.getElementById('regEmail').value; 
    var Password = document.getElementById('regPassword').value;
    var Username = document.getElementById('regUsername').value; 

    if(localStorage.getItem(email)){
        alert("Email already exists");
        return;
    }

    // Corrected: Use userData consistently
    const userData = { password: Password, username: Username };
    
    // Save the user data using the email as the key
    localStorage.setItem(email, JSON.stringify(userData));
    
    alert('Registration successful!');
    wrapper.classList.remove('active'); 
});

// login form submission
document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var email = document.getElementById('loginEmail').value;
    var Password = document.getElementById('loginPassword').value;

    var storedData = localStorage.getItem(email);

    if(storedData === null){
        alert("Email not found");
        return;
    } else {
      
        var user = JSON.parse(storedData);

        
        if(user.password === Password){
            alert('Login successful! Welcome ' + user.username);
            localStorage.setItem('activeUser',user.username)
            window.location.href = 'dashboard.html';
        }
        else {
            alert('Incorrect password');
            return;
        }
    }
});