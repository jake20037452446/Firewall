// ================================
// NAVIGATION TOGGLE (FIXED)
// ================================
function toggleNav() {
  const nav = document.querySelector(".navLinks");
  if (!nav) return;

  nav.classList.toggle("active");
}

// ================================
// SMOOTH SCROLL
// ================================
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener("click", function (e) {
    const targetId = this.getAttribute("href");
    const target = document.querySelector(targetId);

    if (target) {
      e.preventDefault();
      target.scrollIntoView({
        behavior: "smooth",
        block: "start"
      });

      // close mobile menu after click
      document.querySelector(".navLinks")?.classList.remove("active");
    }
  });
});



// ================================
// ACTIVE NAV HIGHLIGHT
// ================================
const sections = document.querySelectorAll("section");
const navLinks = document.querySelectorAll(".navLinks a");

window.addEventListener("scroll", () => {
  let current = "";

  sections.forEach(section => {
    const sectionTop = section.offsetTop - 150;

    if (window.scrollY >= sectionTop) {
      current = section.id;
    }
  });

  navLinks.forEach(link => {
    link.classList.remove("active");

    if (link.getAttribute("href") === "#" + current) {
      link.classList.add("active");
    }
  });
});

// ================================
// EMAILJS + REVIEW SYSTEM (FIXED)
// ================================
document.addEventListener("DOMContentLoaded", () => {

  // init EmailJS once
  if (window.emailjs) {
    emailjs.init("iRfxXO-79aV0Ue0kx");
  }

  const submitBtn = document.getElementById("submitRating");
  const nameInput = document.getElementById("userName");
  const reviewInput = document.getElementById("userReview");
  const ratingInput = document.getElementById("ratingValue");
  const reviewList = document.getElementById("reviewList");

  if (!submitBtn || !nameInput || !reviewInput || !ratingInput) return;

  submitBtn.addEventListener("click", async (e) => {
    e.preventDefault();

    const name = nameInput.value.trim();
    const review = reviewInput.value.trim();
    const rating = ratingInput.value || "5";

    if (!name || !review) {
      alert("Please fill out name and review.");
      return;
    }

    try {
      await emailjs.send("service_w469std", "template_dipb7rm", {
        user_name: name,
        user_review: review,
        user_rating: rating,
        to_email: "firewallone718@gmail.com"
      });

      alert("Review sent successfully!");

      // add review to page
      if (reviewList) {
        const box = document.createElement("div");
        box.style.padding = "12px";
        box.style.marginTop = "10px";
        box.style.background = "rgba(0,0,0,0.05)";
        box.style.borderRadius = "10px";
        box.style.fontFamily = "sans-serif";

        box.innerHTML = `
          <strong>${name}</strong><br>
          <span>${review}</span>
        `;

        reviewList.prepend(box);
      }

      // clear inputs
      nameInput.value = "";
      reviewInput.value = "";

    } catch (err) {
      console.error("EmailJS Error:", err);
      alert("Failed to send review.");
    }
  });
});