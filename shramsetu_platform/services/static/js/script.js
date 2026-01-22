const hiddenElements = document.querySelectorAll(".hidden");

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("show");
      }
    });
  },
  { threshold: 0.3 }
);

hiddenElements.forEach((el) => observer.observe(el));
function validateForm() {
  // Get values
  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const message = document.getElementById("message").value.trim();

  // Error fields
  const nameError = document.getElementById("nameError");
  const emailError = document.getElementById("emailError");
  const messageError = document.getElementById("messageError");
  const successMsg = document.getElementById("successMsg");

  // Reset
  nameError.textContent = "";
  emailError.textContent = "";
  messageError.textContent = "";
  successMsg.textContent = "";

  let isValid = true;

  if (name === "") {
    nameError.textContent = "Name is required";
    isValid = false;
  }

  if (email === "") {
    emailError.textContent = "Email is required";
    isValid = false;
  } else if (!email.includes("@")) {
    emailError.textContent = "Enter a valid email";
    isValid = false;
  }

  if (message === "") {
    messageError.textContent = "Project details are required";
    isValid = false;
  }

  if (isValid) {
    successMsg.textContent = "✅ Message sent successfully!";
  }
}
// EXTRA SCRIPT FOR LOGIN MODAL
function openAuth() {
    document.getElementById('authModal').style.display = 'flex';
}

function closeAuth() {
    document.getElementById('authModal').style.display = 'none';
}

function switchTab(role) {
    // 1. Update the hidden input value
    document.getElementById('userRole').value = role;

    // 2. Update the UI
    const title = document.getElementById('authTitle');
    const tabCustomer = document.getElementById('tabCustomer');
    const tabWorker = document.getElementById('tabWorker');
    const workerOptions = document.getElementById('workerOptions');

    if (role === 'worker') {
        title.innerText = "Worker Login";
        tabWorker.classList.add('active');
        tabCustomer.classList.remove('active');
        // If registering, show skill options
        if(document.getElementById('formAction').value === 'register') {
            workerOptions.style.display = 'block';
        }
    } else {
        title.innerText = "Customer Login";
        tabCustomer.classList.add('active');
        tabWorker.classList.remove('active');
        workerOptions.style.display = 'none';
    }
}

// Close if user clicks outside the box
window.onclick = function(event) {
    let modal = document.getElementById('authModal');
    if (event.target == modal) closeAuth();
}

let isLoginMode = true;

function toggleAuthMode() {
    isLoginMode = !isLoginMode;
    const title = document.getElementById('authTitle');
    const submitBtn = document.getElementById('submitBtn');
    const toggleLink = document.getElementById('toggleLink');
    const toggleMsg = document.getElementById('toggleMsg');
    const nameField = document.getElementById('usernameField');
    const confirmPass = document.getElementById('confirmPasswordField');
    const actionInput = document.getElementById('formAction'); // This is your hidden input

    if (isLoginMode) {
        actionInput.value = "login"; // ADD THIS LINE
        title.innerText = "Login";
        submitBtn.innerText = "Login";
        toggleMsg.innerText = "Don't have an account?";
        toggleLink.innerText = "Register Now";
        nameField.style.display = "none";
        confirmPass.style.display = "none";
    } else {
        actionInput.value = "register"; // ADD THIS LINE
        title.innerText = "Register";
        submitBtn.innerText = "Create Account";
        toggleMsg.innerText = "Already have an account?";
        toggleLink.innerText = "Login Here";
        nameField.style.display = "block";
        confirmPass.style.display = "block";
    }
}
document.getElementById('authForm').onsubmit = function(e) {
    if (!isLoginMode) {
        const pass = document.querySelector('input[name="password"]').value;
        const confirmPass = document.getElementById('confirmPasswordField').value;
        
        if (pass !== confirmPass) {
            alert("Passwords do not match!");
            e.preventDefault(); // Stop the form from submitting
        }
    }
};
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
}

// Optional: Ensure it starts hidden on all screens
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.remove('active');
    }
});