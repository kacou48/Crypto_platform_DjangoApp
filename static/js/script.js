let menuBtn = document.querySelector('#menu-btn');
let navbar = document.querySelector('.header .flex .navbar');


menuBtn.onclick = () =>{
	menuBtn.classList.toggle('fa-times');
	navbar.classList.toggle('active');
}


//pour le login
document.addEventListener("click", e => {
	const isDropdownButton = e.target.matches("[data-dropdown-button]")
    if (!isDropdownButton && e.target.closest('[data-dropdown]') != null) return
    
    let currentDropdown
    if (isDropdownButton) {
    	currentDropdown = e.target.closest('[data-dropdown]')
    	currentDropdown.classList.toggle('active')
    }

document.querySelectorAll("[data-dropdown].active").forEach(dropdown => {
	if (dropdown === currentDropdown) return
	dropdown.classList.remove("active")
})
})