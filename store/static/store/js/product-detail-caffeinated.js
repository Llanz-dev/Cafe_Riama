let price = document.getElementById('product-price');
let cold_price = document.getElementById('cold-price');
let hot_price = document.getElementById('hot-price');

let hot_cold = document.getElementById('hot-cold');
let hot = document.getElementById('id_hot_or_cold_0');
let cold = document.getElementById('id_hot_or_cold_1');

hot.onclick = () => {
    document.getElementById('product-price').textContent = hot_price.textContent;
    hot_cold.textContent = 'Hot'
}

cold.onclick = () => {
    document.getElementById('product-price').textContent = cold_price.textContent;
    hot_cold.textContent = 'Cold'
}