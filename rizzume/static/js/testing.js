function inputRetainer() {
    if (typeof(Storage) !== "undefined") {
        var inputs = document.querySelectorAll(".form-control");
        inputs.forEach(function(input) {
            var nameAttribute = input.getAttribute("name");
            // Save input values to localStorage on input event
            input.addEventListener("input", function() {
                localStorage.setItem(nameAttribute, this.value);
            });
            // Populate input fields with localStorage values on page load
            var storedValue = localStorage.getItem(nameAttribute);
            if (storedValue !== null) {
                input.value = storedValue;
            }
        });
    } else {
        document.getElementById("result").innerHTML = "Sorry, your browser does not support web storage...";
    }
  }
  
  document.addEventListener("DOMContentLoaded", function() {
    inputRetainer();
  });
  