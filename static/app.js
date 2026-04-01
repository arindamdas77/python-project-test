const form = document.getElementById("submission-form");
const statusMessage = document.getElementById("status-message");

const gradients = [
  "linear-gradient(135deg, #ffd6a5, #caffbf)",
  "linear-gradient(135deg, #a0c4ff, #bdb2ff)",
  "linear-gradient(135deg, #9bf6ff, #fdffb6)",
  "linear-gradient(135deg, #ffadad, #ffd6a5)",
  "linear-gradient(135deg, #b8f2e6, #aed9e0)"
];

let gradientIndex = 0;

setInterval(() => {
  gradientIndex = (gradientIndex + 1) % gradients.length;
  document.body.style.background = gradients[gradientIndex];
}, 3000);

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const submitButton = form.querySelector("button");
  const formData = new FormData(form);
  const payload = Object.fromEntries(formData.entries());

  submitButton.disabled = true;
  statusMessage.textContent = "Submitting...";
  statusMessage.className = "status";

  try {
    const response = await fetch("/api/submissions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Unable to save submission.");
    }

    form.reset();
    statusMessage.textContent = data.message;
    statusMessage.className = "status success";
  } catch (error) {
    statusMessage.textContent = error.message;
    statusMessage.className = "status error";
  } finally {
    submitButton.disabled = false;
  }
});
