const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
  container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
  container.classList.remove("right-panel-active");
});

window.addEventListener('DOMContentLoaded', () => {
  const messageTag = document.body.getAttribute('data-message-tag');
  const container = document.getElementById('container');

  if (messageTag && messageTag.includes('signup')) {
    container.classList.add("right-panel-active");
  } else {
    container.classList.remove("right-panel-active");
  }

  // Auto hide messages after 5 seconds
  setTimeout(() => {
    document.querySelectorAll('.messages').forEach(el => {
      el.style.opacity = 1;
      let fadeOut = setInterval(() => {
        if (el.style.opacity > 0) {
          el.style.opacity -= 0.1;
        } else {
          clearInterval(fadeOut);
          el.style.display = 'none';
        }
      }, 50);
    });
  }, 5000);
});

function isMobileView() {
  return window.innerWidth <= 850;
}

const toggleButtons = document.querySelector('.toggle-buttons');
const signInForm = document.querySelector('.sign-in-container');
const signUpForm = document.querySelector('.sign-up-container');
const btnSignIn = document.getElementById('toggle-signin');
const btnSignUp = document.getElementById('toggle-signup');

function showSignIn() {
  signInForm.classList.add('active');
  signUpForm.classList.remove('active');
  btnSignIn.classList.add('active');
  btnSignUp.classList.remove('active');
}

function showSignUp() {
  signUpForm.classList.add('active');
  signInForm.classList.remove('active');
  btnSignUp.classList.add('active');
  btnSignIn.classList.remove('active');
}

function setupMobileView() {
  if (isMobileView()) {
    toggleButtons.style.display = 'block';
    // Show sign-in form by default
    showSignIn();
  } else {
    toggleButtons.style.display = 'none';
    // On desktop, show both forms for overlay style
    signInForm.classList.remove('active');
    signUpForm.classList.remove('active');
  }
}

// On buttons click
btnSignIn.addEventListener('click', showSignIn);
btnSignUp.addEventListener('click', showSignUp);

// On load and resize, set correct view
window.addEventListener('load', setupMobileView);
window.addEventListener('resize', setupMobileView);
