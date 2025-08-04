document.addEventListener('DOMContentLoaded', () => {
      const addSkillButton = document.getElementById('add-new-skill');
      if (addSkillButton) {
          console.log('Add New Skill button found');
          addSkillButton.addEventListener('click', () => {
              console.log('Add New Skill button clicked');
              const skillName = document.getElementById('name').value;
              console.log('Skill input:', skillName);
              if (!skillName) {
                  alert('Enter a skill');
                  return;
              }
              fetch('/add_skill/', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': getCookie('csrftoken'),
                  },
                  body: JSON.stringify({ skill: skillName }),
              })
              .then(response => {
                  if (!response.ok) {
                      throw new Error(`HTTP error! Status: ${response.status}`);
                  }
                  return response.json();
              })
              .then(data => {
                  if (data.success) {
                      const skillsList = document.getElementById('skills-list');
                      console.log('Skills list element:', skillsList);
                      const li = document.createElement('li');
                      li.textContent = skillName;
                      skillsList.appendChild(li);
                      document.getElementById('name').value = '';
                  } else {
                      alert('Error adding skill: ' + (data.error || 'Unknown error'));
                  }
              })
              .catch(error => {
                  console.error('Error adding skill:', error);
                  alert('Failed to add skill. Check console for details.');
              });
          });
      } else {
          console.error('Add New Skill button not found');
      }

      const addExperienceButton = document.getElementById('add-new-experience');
      if (addExperienceButton) {
          console.log('Add New Experience button found');
          addExperienceButton.addEventListener('click', () => {
              console.log('Add New Experience button clicked');
              alert('Test alert: Button clicked');
          });
      } else {
          console.error('Add New Experience button not found');
      }

      function getCookie(name) {
          let cookieValue = null;
          if (document.cookie && document.cookie !== '') {
              const cookies = document.cookie.split(';');
              for (let i = 0; i < cookies.length; i++) {
                  const cookie = cookies[i].trim();
                  if (cookie.substring(0, name.length + 1) === (name + '=')) {
                      cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                      break;
                  }
              }
          }
          return cookieValue;
      }

      window.toggleMenu = function() {
          const menu = document.querySelector('.menu');
          menu.classList.toggle('active');
      };
  });