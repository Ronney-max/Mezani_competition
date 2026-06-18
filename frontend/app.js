const form = document.getElementById("registrationForm");
const submitButton = document.getElementById("submitButton");
const formStatus = document.getElementById("formStatus");

function showStatus(message, type = "info") {
  formStatus.textContent = message;
  formStatus.className = `form-status ${type}`;
}

async function submitToFormspree() {
  const response = await fetch(form.action, {
    method: "POST",
    headers: {
      "Accept": "application/json",
    },
    body: new FormData(form),
  });

  const contentType = response.headers.get("content-type") || "";
  const result = contentType.includes("application/json")
    ? await response.json()
    : { message: await response.text() };

  if (!response.ok) {
    const errorMessage = result.errors?.[0]?.message || result.message || "Registration failed.";
    throw new Error(errorMessage);
  }

  return result;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  try {
    if (form.action.includes("YOUR_FORM_ID")) {
      throw new Error("Replace YOUR_FORM_ID with your real Formspree form ID.");
    }

    submitButton.disabled = true;
    submitButton.textContent = "Sending...";
    showStatus("Sending your registration...", "info");

    await submitToFormspree();
    showStatus("Registration submitted successfully.", "success");
    form.reset();
  } catch (error) {
    console.error(error);
    showStatus(error.message || "Registration failed.", "error");
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Register";
  }
});
