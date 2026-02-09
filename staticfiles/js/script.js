/* Change product image */
function changeImage(el) {
  const mainImg = document.getElementById('mainProductImage');
  mainImg.src = el.src;

  document.querySelectorAll('.thumb').forEach(img => {
    img.classList.remove('active');
  });

  el.classList.add('active');
}

/* ===============================
   STOCK + QUANTITY LOGIC
================================ */

let selectedStock = 0;

/* Show stock when size is clicked */
function showStock(element) {
  selectedStock = parseInt(element.getAttribute("data-stock"));
  const stockText = document.getElementById("stock-text");
  const qtyInput = document.getElementById("quantity");
  const warning = document.getElementById("qty-warning");

  qtyInput.value = 1;
  warning.innerHTML = "";

  if (selectedStock > 0) {
    stockText.innerHTML = `
      <span class="badge bg-success px-3 py-2">
        ${selectedStock} in stock
      </span>
    `;
    enableButtons();
  } else {
    stockText.innerHTML = `
      <span class="badge bg-danger px-3 py-2">
        Out of stock
      </span>
    `;
    disableButtons();
  }
}

/* Increase / Decrease quantity */
function changeQty(value) {
  const qtyInput = document.getElementById("quantity");
  const warning = document.getElementById("qty-warning");
  let current = parseInt(qtyInput.value);

  let newQty = current + value;

  if (newQty < 1) newQty = 1;

  if (newQty > selectedStock) {
    newQty = selectedStock;
    warning.innerHTML = `⚠ Only ${selectedStock} item(s) available`;
    disableButtons();
  } else {
    warning.innerHTML = "";
    enableButtons();
  }

  qtyInput.value = newQty;
}

/* Disable cart buttons */
function disableButtons() {
  document.getElementById("add-to-cart-btn").disabled = true;
  document.getElementById("buy-now-btn").disabled = true;
}

/* Enable cart buttons */
function enableButtons() {
  document.getElementById("add-to-cart-btn").disabled = false;
  document.getElementById("buy-now-btn").disabled = false;
}

/* Disable buttons on page load */
document.addEventListener("DOMContentLoaded", function () {
  disableButtons();
});
