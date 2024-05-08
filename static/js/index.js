document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("sentiment-form");
  const messageHistory = document.getElementById("message-history");
  const maxMessages = 10; // Change this to set the maximum number of messages

  // Function to load messages from local storage
  function loadMessages() {
    const messages = JSON.parse(localStorage.getItem("messages")) || [];
    messages.forEach((item) => {
      const listItem = createMessageItem(item.message, item.timestamp);
      messageHistory.appendChild(listItem);
    });
  }

  // Load messages when the page is loaded
  loadMessages();

  // Function to create a list item for a message
  function createMessageItem(message, timestamp) {
    const listItem = document.createElement("li");
    listItem.className = "list-group-item d-flex justify-content-between";

    const messageDiv = document.createElement("div");
    messageDiv.textContent = message;

    const timestampDiv = document.createElement("div");
    timestampDiv.textContent = new Date(timestamp).toLocaleString();

    listItem.appendChild(messageDiv);
    listItem.appendChild(timestampDiv);

    return listItem;
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent form submission

    const msgInput = document.getElementById("msg");
    const message = msgInput.value.trim(); // Get the trimmed message value

    if (message !== "") {
      // Only add message if it's not empty
      const timestamp = Date.now(); // Get current timestamp

      const listItem = createMessageItem(message, timestamp);
      messageHistory.appendChild(listItem);

      // Remove the oldest message if the maximum limit is reached
      if (messageHistory.children.length > maxMessages) {
        messageHistory.removeChild(messageHistory.children[0]); // Remove the first (oldest) message
      }

      // Store messages in local storage
      const messages = Array.from(messageHistory.children).map((child) => {
        return {
          message: child.children[0].textContent,
          timestamp: new Date(child.children[1].textContent).getTime(),
        };
      });
      localStorage.setItem("messages", JSON.stringify(messages));

      // Clear the input field after adding the message
      msgInput.value = "";
    }
  });
});

function handleSubmit(event) {
  event.preventDefault();
  let message = document.getElementById("msg").value.trim();
  if (message) {
    analyzeSentiment(message);
  }
}

function analyzeSentiment(message) {
  fetch("/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ msg: message }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data.sentiment);
      updatePage(data.sentiment);
    })
    .catch((error) => console.error("Error:", error));
}

function updatePage(sentiment) {
  let body = document.querySelector("body");
  let icon = document.querySelector('link[rel="icon"]');

  switch (sentiment) {
    case "positive":
      body.classList.remove("bg-dark", "bg-danger");
      body.classList.add("bg-success");
      icon.href = "/static/assets/favicon1.ico";
      break;
    case "negative":
      body.classList.remove("bg-dark", "bg-success");
      body.classList.add("bg-danger");
      icon.href = "/static/assets/favicon2.ico";
      break;
    default:
      body.classList.remove("bg-danger", "bg-success");
      body.classList.add("bg-dark");
      icon.href = "/static/assets/favicon0.ico";
      break;
  }
}

document
  .getElementById("sentiment-form")
  .addEventListener("submit", handleSubmit);
