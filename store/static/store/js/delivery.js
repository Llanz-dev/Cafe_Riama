let office_button = document.getElementById('office-button');
let home_button = document.getElementById('home-button');
let office_input = document.getElementById('office-input') ;
let home_input = document.getElementById('home-input');
let districts = document.getElementById('id_districts');
let sub_total = document.getElementById('sub_total');
let delivery_fee_amount = 70
districts.onclick = () => {
    const total = document.getElementById('total');
    const delivery_fee = document.getElementById('delivery_fee');
    if (districts.value === 'Arevalo') {
        delivery_fee.textContent = 70;   
    }
    if (districts.value === 'City Proper') {
        delivery_fee.textContent = 60;
    }
    if (districts.value === 'Jaro') {
            delivery_fee.textContent = 50;    
    }
    if (districts.value === 'La Paz') {
            delivery_fee.textContent = 60;    
    }
    if (districts.value === 'Lapuz') {
        delivery_fee.textContent = 80;
    }
    if (districts.value === 'Mandurriao') {
        delivery_fee.textContent = 40;
    }
    if (districts.value === 'Molo') {
        delivery_fee.textContent = 70;
    } 
    total.textContent = (parseInt(sub_total.textContent.replace(/,/g,"")) + parseInt(delivery_fee.textContent.replace(/,/g,""))).toLocaleString()
}

office_button.onclick = (e) => {
    e.preventDefault();
    office_button.classList.add('deliver-collection-click');
    home_button.classList.remove('deliver-collection-click'); 
    office_input.checked = true;
    home_input.checked = false;    
}

home_button.onclick = (e) => {
    e.preventDefault();
    home_button.classList.add('deliver-collection-click');
    office_button.classList.remove('deliver-collection-click');
    office_input.checked = false;
    home_input.checked = true; 
}

