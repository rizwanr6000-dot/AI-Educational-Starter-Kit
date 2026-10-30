const generateBtn = document.getElementById("generateBtn");
const copyBtn = document.getElementById("copyBtn");
const outputBox = document.getElementById("outputBox");

generateBtn.addEventListener("click", async () => {
  const content_type = document.getElementById("contentType").value;
  const tone = document.getElementById("tone").value;
  const topic = document.getElementById("topic").value.trim();
  const extra_instructions = document.getElementById("extra").value.trim();

  if (!topic) {
    outputBox.textContent = "Please enter a topic before generating.";
    return;
  }

  generateBtn.disabled = true;
  generateBtn.textContent = "Generating...";
  outputBox.textContent = "Working on it...";

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content_type, tone, topic, extra_instructions }),
    });

    const data = await response.json();

    if (!response.ok) {
      outputBox.textContent = `Error: ${data.error || "Something went wrong."}`;
    } else {
      outputBox.textContent = data.output;
    }
  } catch (err) {
    outputBox.textContent = `Request failed: ${err.message}`;
  } finally {
    generateBtn.disabled = false;
    generateBtn.textContent = "Generate";
  }
});

copyBtn.addEventListener("click", () => {
  navigator.clipboard.writeText(outputBox.textContent).then(() => {
    copyBtn.textContent = "Copied!";
    setTimeout(() => (copyBtn.textContent = "Copy"), 1500);
  });
});
