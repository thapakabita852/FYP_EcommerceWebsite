document.addEventListener("DOMContentLoaded", function () {
  // Tab switching functionality
  const navItems = document.querySelectorAll(".nav-item");
  const panels = document.querySelectorAll(".panel");
  const pageTitle = document.getElementById("page-title");

  // Initially hide all panels except the first one
  panels.forEach((panel, index) => {
    if (index !== 0) {
      panel.classList.add("hidden");
      panel.classList.remove("active");
    } else {
      panel.classList.add("active");
      panel.classList.remove("hidden");
    }
  });

  // Initially set the first nav item as active
  if (navItems.length > 0) {
    navItems[0].classList.add("active");
  }

  function switchTab(tabId) {
    // Update navigation items
    navItems.forEach((item) => {
      item.classList.remove("active");
      if (item.dataset.tab === tabId) {
        item.classList.add("active");
        pageTitle.textContent = item.querySelector("span").textContent;
      }
    });

    // Update panels
    panels.forEach((panel) => {
      if (panel.id === tabId) {
        panel.classList.remove("hidden");
        panel.classList.add("active");
      } else {
        panel.classList.add("hidden");
        panel.classList.remove("active");
      }
    });
  }

  navItems.forEach((item) => {
    item.addEventListener("click", () => {
      switchTab(item.dataset.tab);
    });
  });

  // Profile editing functionality
  const editProfileBtn = document.getElementById("edit-profile-btn");
  const cancelEditBtn = document.getElementById("cancel-edit-btn");
  const profileForm = document.getElementById("profile-form");

  if (editProfileBtn && cancelEditBtn && profileForm) {
    // Initially hide the form
    profileForm.classList.add("hidden");

    editProfileBtn.addEventListener("click", () => {
      profileForm.classList.remove("hidden");
      editProfileBtn.classList.add("hidden");
    });

    cancelEditBtn.addEventListener("click", () => {
      profileForm.classList.add("hidden");
      editProfileBtn.classList.remove("hidden");
    });
  }

  // Password visibility toggle
  const passwordInputs = document.querySelectorAll('input[type="password"]');
  passwordInputs.forEach((input) => {
    const wrapper = document.createElement("div");
    wrapper.className = "password-input-wrapper";
    input.parentNode.insertBefore(wrapper, input);
    wrapper.appendChild(input);

    const toggleBtn = document.createElement("button");
    toggleBtn.type = "button";
    toggleBtn.className = "password-toggle";
    toggleBtn.innerHTML = '<i class="fas fa-eye"></i>';
    wrapper.appendChild(toggleBtn);

    toggleBtn.addEventListener("click", () => {
      const type = input.type === "password" ? "text" : "password";
      input.type = type;
      toggleBtn.innerHTML = `<i class="fas fa-eye${
        type === "password" ? "" : "-slash"
      }"></i>`;
    });
  });

  // Form validation
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", (e) => {
      const requiredFields = form.querySelectorAll("[required]");
      let isValid = true;

      requiredFields.forEach((field) => {
        if (!field.value.trim()) {
          isValid = false;
          field.classList.add("error");
          showError(field, "This field is required");
        } else {
          field.classList.remove("error");
          removeError(field);
        }
      });

      // Password match validation for password change form
      if (form.id === "password-form") {
        const newPassword = form.querySelector("#new_password1");
        const confirmPassword = form.querySelector("#new_password2");
        if (newPassword && confirmPassword) {
          if (newPassword.value !== confirmPassword.value) {
            isValid = false;
            showError(confirmPassword, "Passwords do not match");
          }
        }
      }

      if (!isValid) {
        e.preventDefault();
      }
    });
  });

  // Helper functions for form validation
  function showError(field, message) {
    removeError(field);
    const errorDiv = document.createElement("div");
    errorDiv.className = "error-message";
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
  }

  function removeError(field) {
    const error = field.parentNode.querySelector(".error-message");
    if (error) {
      error.remove();
    }
  }

  // File input preview for profile picture
  const profilePictureInput = document.getElementById("profile_picture");
  if (profilePictureInput) {
    profilePictureInput.addEventListener("change", function(e) {
      const file = e.target.files[0];
      if (file && file.type.startsWith("image/")) {
        const reader = new FileReader();
        reader.onload = function(e) {
          const currentPicture = document.querySelector(".profile-picture img");
          if (currentPicture) {
            currentPicture.src = e.target.result;
          }
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // Add smooth scroll to top when switching tabs
  function scrollToTop() {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  }

  navItems.forEach((item) => {
    item.addEventListener("click", scrollToTop);
  });
});