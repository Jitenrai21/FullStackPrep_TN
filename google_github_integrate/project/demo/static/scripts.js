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
