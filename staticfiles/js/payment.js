document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("payment-form");
  form.addEventListener("submit", function(e) {
    // Basic client-side validation example:
    const cardNumber = document.getElementById("cardnumber").value;
    const expiry = document.getElementById("expiry").value;
    const cvv = document.getElementById("cvv").value;

    if (cardNumber.length !== 16 || isNaN(cardNumber)) {
      alert("Please enter a valid 16-digit card number.");
      e.preventDefault();
      return;
    }
    if (!/^\d{2}\/\d{2}$/.test(expiry)) {
      alert("Please enter a valid expiry date in MM/YY format.");
      e.preventDefault();
      return;
    }
    if (cvv.length !== 3 || isNaN(cvv)) {
      alert("Please enter a valid 3-digit CVV.");
      e.preventDefault();
      return;
    }
    // Optionally: show a "Processing..." message here
  });
});
