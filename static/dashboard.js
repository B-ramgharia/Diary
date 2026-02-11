
// 1. Target the submenu element for the toggle function
let submenu = document.getElementById("submenu");

function togglem() {
    if (submenu) {
        submenu.classList.toggle("open-menu");
    }
}



const loggedInUser = localStorage.getItem('activeUser');

if (loggedInUser) {
    // If a user is found, display their name
    document.getElementById("UserName").innerText = loggedInUser;
} else {
    // Optional: Redirect to login if someone tries to access dashboard without logging in
    // window.location.href = 'login.html';
    document.getElementById("UserName").innerText = "Guest";
}


// Target the logout button
const logoutBtn = document.getElementById('logoutBtn');

if (logoutBtn) {
    logoutBtn.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent the link from jumping

        // 1. Remove the active user session
        localStorage.removeItem('activeUser');

        // 2. Optional: Remove other temporary session data if you have any
        // localStorage.clear(); // Note: This deletes EVERYTHING in storage

        alert("You have been logged out.");

        // 3. Redirect to the login/home page
        window.location.href = '/'; 
    });
}




