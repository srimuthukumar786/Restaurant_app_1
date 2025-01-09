var swiper = new Swiper(".mySwiper", {
    loop: true,
    autoplay: {
      delay: 4000, 
      disableOnInteraction: false, 
    },
    pagination: {
      el: ".swiper-pagination",
      dynamicBullets: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });


//   user profile

let subMenu=document.getElementById('subMenu')
		function toggleMenu(){
			subMenu.classList.toggle('open-menu')
			navbar.style.maxHeight="0px"
		}
		let navbar=document.getElementById('navbar')
			navbar.style.maxHeight="0px"
		function togglenav()
		{
			subMenu.classList.remove('open-menu')
			if(navbar.style.maxHeight == "0px"){
				navbar.style.maxHeight="500px"
			}
			else{
				navbar.style.maxHeight="0px"
			}
		};

// login

		function login(){
			let isValid=true
			document.getElementById("useremailerror").textContent="";
			document.getElementById("userpassworderror").textContent="";

		let useremail=document.getElementById("useremail").value;
		let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
		if(useremail ===""){
			document.getElementById("useremailerror").textContent="Enter you'r mail";
			isValid=false;
		}
		else if(!emailPattern.test(useremail)){
		document.getElementById('emailerror').textContent="Worng formet"
		isValid=false;
		}

		let password=document.getElementById("userpassword").value;
		if(password === ""){
		document.getElementById("userpassworderror").textContent="Enter Password";
		isValid=false;
		}
		else if(password.length <6){
		document.getElementById("userpassworderror").textContent="Enter Minimum 6 charactors";
		isValid=false;
		}
		return isValid
		}

		// registraction

		function test(){
			let isValid=true
			document.getElementById('nameerroe').textContent=''
			document.getElementById('nameerroe2').textContent=''
			document.getElementById('emailerror').textContent=''
			document.getElementById('phoneerror').textContent=''
			document.getElementById('passworderror').textContent=''
			document.getElementById('conformpassworderror').textContent=''
	
			let name=document.getElementById('name').value
			if(name === ''){
				document.getElementById('nameerroe').textContent="First name must be required"
				isValid=false;
			}
			let name2=document.getElementById('name2').value
			if(name2 === ''){
				document.getElementById('nameerroe2').textContent="Last name must be required"
				isValid=false;
			}
			let email=document.getElementById('email').value
			let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
			if(email ===''){
				document.getElementById('emailerror').textContent="Enter you'r email"
				isValid=false;
			}
			else if(!emailPattern.test(email)){
				document.getElementById('emailerror').textContent="Wrong format"
				isValid=false;
			}

			let phone = document.getElementById('phone').value
			if(phone ===''){
				document.getElementById('phoneerror').textContent = 'Phone Number is Required'
				isValid=false;
			}
			else if(phone.length() < 10){
				document.getElementById('phoneerror').textContent = 'Phone Number must be 10 digits'
				isValid=false;
			}
	
			let password=document.getElementById('password').value
			if(password === ''){
				document.getElementById('passworderror').textContent="Password must Need"
				isValid=false
			}
			else if(password < 6){
				document.getElementById('passworderror').textContent="Password Need minimum 6 charector"
				isValid=false
			}
			let conformpassword=document.getElementById('conformpassword').value
			if(conformpassword === ''){
			document.getElementById('conformpassworderror').textContent='Re enter your password'
			isValid=false
			}
			else if (conformpassword !== password){
			document.getElementById('conformpassworderror').textContent='Password not Same'
			isValid=false
			}
			return isValid
		}

// Book a table

function booktable(){
	let isValid=true
	document.getElementById("tableNameError").value="";
	document.getElementById("tableNameError2").value="";
	document.getElementById("tableEmailError").value="";
	document.getElementById("phonenumberError").value="";
	
	let name=document.getElementById('tableName').value
		if(name === ''){
			document.getElementById('tableNameError').textContent="First name must be required"
			isValid=false;
		}
		let name2=document.getElementById('tableName2').value
		if(name2 === ''){
			document.getElementById('tableNameError2').textContent="Last name must be required"
			isValid=false;
		}
		let email=document.getElementById('tableEmail').value
		let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
		if(email ===''){
			document.getElementById('tableEmailError').textContent="Enter you'r email"
			isValid=false;
		}
		else if(!emailPattern.test(email)){
			document.getElementById('tableEmailError').textContent="Worng formet"
			isValid=false;
		}

		let phonenumber=document.getElementById("phonenumber").value
		if(phonenumber === ""){
			document.getElementById('phonenumberError').textContent="Enter Your Number";
			isValid=false;

		}
		let date=document.getElementById("date").value
		if(date === ""){
			document.getElementById('dateError').textContent="Enter Date & time";
			isValid=false;

		}

		return isValid   
}

// reviews
   