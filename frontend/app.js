const RENDER_API_URL = "https://mezani-competition.onrender.com";
const API_BASE_URL = window.location.hostname.endsWith("vercel.app")
  ? ""
  : RENDER_API_URL;

const form = document.getElementById("registrationForm");
const submitButton = document.getElementById("submitButton");
const formStatus = document.getElementById("formStatus");

function showStatus(message, type = "info") {
  formStatus.textContent = message;
  formStatus.className = `form-status ${type}`;
}

function getFormData() {
  const data = new FormData(form);

  return {
    name: data.get("name"),
    email: data.get("email"),
    phone: data.get("phone"),
    gender: data.get("gender"),
    category: data.get("category"),
    experience: data.get("experience"),
    age_group: data.get("age_group"),
  };
}

async function registerParticipant(formData) {
  const response = await fetch(`${API_BASE_URL}/api/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });

  const contentType = response.headers.get("content-type") || "";
  const result = contentType.includes("application/json")
    ? await response.json()
    : { message: await response.text() };

  if (!response.ok) {
    throw new Error(result.message || "Registration failed.");
  }

  return result;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  try {
    submitButton.disabled = true;
    submitButton.textContent = "Sending...";
    showStatus("Sending your registration...", "info");

    const result = await registerParticipant(getFormData());
    showStatus(result.message, "success");
    form.reset();
  } catch (error) {
    console.error(error);
    showStatus(error.message || "Registration failed.", "error");
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Register";
  }
});
