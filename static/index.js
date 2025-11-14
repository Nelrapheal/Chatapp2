let expression = "";

function press(key) {
  if(key === "=") {
    fetch('/calculate', {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({expression: expression})
    })
    .then(res => res.json())
    .then(data => {
      document.getElementById("text").value = data.result;
      expression = data.result.toString();
    })
  } else {
    expression += key;
    document.getElementById("text").value = expression
  }
  }

function clearbtn() {
  expression = "";
  document.getElementById("text").value = "";
}