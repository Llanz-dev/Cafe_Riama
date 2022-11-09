let office_button = document.getElementById('office-button');
let home_button = document.getElementById('home-button');
let office_input = document.getElementById('office-input') ;
let home_input = document.getElementById('home-input');

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

