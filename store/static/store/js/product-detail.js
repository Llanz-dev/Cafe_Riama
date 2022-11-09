let price = document.getElementById('price');
let cold_price = document.getElementById('cold-price');

let hot_cold = document.getElementById('hot-cold');
let hot = document.getElementById('hot');
let cold = document.getElementById('cold');
console.log('Cold price:', cold_price.textContent);

hot.onclick = () => {
    document.getElementById('product-price').textContent = price.textContent;
    hot_cold.textContent = 'hot'
}

cold.onclick = () => {
    document.getElementById('product-price').textContent = cold_price.textContent;
    hot_cold.textContent = 'cold'
}