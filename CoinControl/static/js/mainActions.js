// If on homepage allow changing of user info
let modalBtn;
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname == '/') {
        document.querySelector('#userName').classList.add('cursor-pointer');
        document.querySelector('#userName').addEventListener('click', () => {
            modalBtn = document.querySelector('#userName')
            openModal('user')
        })
    } else {
        document.querySelector('#userName').classList.remove('cursor-pointer');
    }
});

// logout function
function logoutFunc() {
    let csrftoken = getToken('csrftoken');
    let url = '/logout';

    console.log('hello')

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            console.error('Logout failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Toggle menu
let menuOpen = false;
function toggleMenu() {
    const button = document.querySelector('#menuBtn');
    const btnRect = button.getBoundingClientRect();
    const menuBox = document.querySelector('#menuBox');
    
    if (window.location.pathname == '/') {
        button.classList.remove('rotate-45', 'font-[900]');
        
        if (button.classList.contains('menuBtnOn')) {
            button.classList.remove('menuBtnOn');
            button.classList.add('menuBtnOff');
        } else {
            button.classList.remove('menuBtnOff');
            button.classList.add('menuBtnOn');
        }
    
        if (menuBox.classList.contains('hidden')) {
            menuBox.classList.remove('hidden')
            menuBox.classList.add('w-44', 'h-10', 'max-h-80')
            menuBox.style.top = `${btnRect.bottom}px`;
            menuBox.style.left = `${btnRect.right - menuBox.getBoundingClientRect().width}px`;
            menuOpen = true;
        } else {
            menuBox.classList.add('hidden')
            menuOpen = false;
        }
    }
}

// check signup form
function checkSignup() {
    let csrftoken = getToken('csrftoken');
    let url = '/signup';
    let nextUrl = '/';
    let username = document.querySelector('#userNameSignup').value;
    let email = document.querySelector('#emailSignup').value;
    let password = document.querySelector('#passwordSignup').value;
    let confirmPassword = document.querySelector('#confirmPasswordSignup').value;
    let signupError = document.querySelector('#signupError');

    if (window.location.href.includes('next')) {
        nextUrl = window.location.href.split('next=')[1];
    }

    // regex for password (8 characters, one uppercase, one lowercase, one number and one special character)
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    
    if (username === '' || password === '' || confirmPassword === '' || email === '') {
        signupError.textContent = 'All fields are required';
        signupError.classList.remove('hidden');
        return;
    } else if (username.includes('@')) {
        signupError.textContent = 'Username cannot contain @';
        signupError.classList.remove('hidden');
        return;
    } else if (password !== confirmPassword) {
        signupError.textContent = 'Passwords do not match';
        signupError.classList.remove('hidden');
        return;
    } else if (!regex.test(password) || !regex.test(confirmPassword)) {
        signupError.textContent = 'Password must contain at least 8 characters, one uppercase, one lowercase, one number and one special character';
        signupError.classList.remove('hidden');
        return;
    } else {
        signupError.classList.add('hidden');
        
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ username: username, email: email, password: password, confirm_password: confirmPassword, next_url: nextUrl})
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            } else if (response.ok) {
                window.location.reload(); 
            } else {
                console.error('Signup failed');
            }
        })
        .catch(error => {
            console.error('ERROR:', error);
        });
    }
};

// login function
function loginFunc() {
    let csrftoken = getToken('csrftoken');
    let url = '/login';

    let usernameOrEmail = document.querySelector('#userNameOrEmailLogin').value;
    let password = document.querySelector('#passwordLogin').value;
    let nextUrl = '/';

    if (window.location.href.includes('next')) {
        nextUrl = window.location.href.split('next=')[1];
    }

    fetch (url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ username_or_email: usernameOrEmail, password: password, next_url: nextUrl})
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else if (response.ok) {
            window.location.reload(); 
        } else {
            console.error('Login failed');
        }
    })
    .catch(error => {
        console.error('ERROR:', error);
    });
};

// Open modal
let modalOpen = false;
function openModal(type) {
    modalOpen = true;
    document.getElementById("blurBackground").classList.remove("duration-300");
    document.querySelector("#modal").classList.remove("hidden");
    document.querySelector("#blurBackground").classList.add("blur-sm", "backdrop-blur-sm", "duration-700");
    
    if (type === 'user') {        
        document.querySelector('#updateUserBtn').setAttribute('onclick', `checkUpdateUser(${JSON.stringify(userInfo)})`)
        document.querySelector('#modalUser').classList.remove('hidden')
        
        document.querySelector('#userNameUser').value = userInfo.username
        document.querySelector('#emailUser').value = userInfo.email
        document.querySelector('#firstNameUser').value = userInfo.first_name
        document.querySelector('#lastNameUser').value = userInfo.last_name
    }
};

// show password fields
function showPasswordUpdate() {
    if (document.querySelector('#passwordUserBox').classList.contains('hidden')) {
        document.querySelector('#passwordUserBox').classList.remove('hidden')
        document.querySelector('#confirmPasswordUserBox').classList.remove('hidden')
    } else {
        document.querySelector('#passwordUserBox').classList.add('hidden')
        document.querySelector('#confirmPasswordUserBox').classList.add('hidden')
    }
};

// Close modal
function closeModal() {
    const selectFields = document.querySelectorAll('select');
    const inputFields = document.querySelectorAll('input');
    const textareaFields = document.querySelectorAll('textarea');
    selectFields.forEach(select => {
        select.value = select.querySelector('.hidden').value;
    });
    inputFields.forEach(input => {
        input.value = '';
    });
    textareaFields.forEach(textarea => {
        textarea.value = '';
    })
    
    document.getElementById("blurBackground").classList.remove("duration-700");
    document.getElementById("blurBackground").classList.add("duration-300");
    document.getElementById("modal").classList.add("hidden");
    document.getElementById("blurBackground").classList.remove("blur-sm", "backdrop-blur-sm");
    modalOpen = false;
};

function checkUpdateUser(userInfo) {
    let username = document.querySelector('#userNameUser').value;
    let email = document.querySelector('#emailUser').value;
    let firstName = document.querySelector('#firstNameUser').value;
    let lastName = document.querySelector('#lastNameUser').value;
    let password = document.querySelector('#passwordUser').value;
    let confirmPassword = document.querySelector('#confirmPasswordUser').value;
    let userError = document.querySelector('#userError');
    let userForm = document.querySelector('#userForm');
    let updateInfo = {
        username: username,
        email: email,
        first_name: firstName,
        last_name: lastName,
    }

    let isDifferent = false;
    for (let key in userInfo) {
        if (userInfo[key] !== updateInfo[key]) {
            isDifferent = true;
            break;
        }
    };

    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

    if (isDifferent || (password != '' && !document.querySelector('#passwordUserBox').classList.contains('hidden'))) {
        if (!document.querySelector('#passwordUserBox').classList.contains('hidden')) {
            if (password != '' && confirmPassword != '') {
                if (password !== confirmPassword) {
                    userError.textContent = 'Passwords do not match';
                    userError.classList.remove('hidden');
                    return;
                } else if (!regex.test(password) || !regex.test(confirmPassword)) {
                    userError.textContent = 'Password must contain at least 8 characters, one uppercase, one lowercase, one number and one special character';
                    userError.classList.remove('hidden');
                    return;
                } else {
                    userError.classList.add('hidden');
                    userForm.submit();
                }
            } else {
                userError.textContent = 'Both password fields are required';
                userError.classList.remove('hidden');
            }
        } else {
            userError.classList.add('hidden');
            userForm.submit();
        }
    } else {
        document.querySelector('#userError').classList.remove('hidden')
        document.querySelector('#userError').textContent = 'Please change at least one field'
    }
};

// delete user function
function deleteUserFunc() {
    let csrftoken = getToken('csrftoken');
    let url = '/delete_account';

    dialogClose();

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            console.error('Delete account failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
};

document.addEventListener('keydown', (e) => {
    const button = document.querySelector('#menuBtn');
    const menuBox = document.querySelector('#menuBox');
    if (e.key == 'Escape') {
        if (dialogIsOpen === false) {
            if (menuOpen === true) {
                // close menu when pressed Esc
                toggleMenu()
            } else if (modalOpen === true) {
                // close modal when pressed Esc
                closeModal()
            }
        } else {
            dialogBox.classList.remove('dialogAnimate');
            void dialogBox.offsetWidth; // Trigger reflow to restart the animation
            dialogBox.classList.add('dialogAnimate');
        }
    }
});

document.addEventListener('click', (e) => {
    const menuBtn = document.querySelector('#menuBtn');
    const menuBox = document.querySelector('#menuBox');
    const modalBox = document.querySelector('#modalBox');
    // close menu if clicked outside
    if (dialogIsOpen === false) {
        if (!menuBox.contains(e.target) && !menuBtn.contains(e.target) && menuOpen === true) {
            toggleMenu()
        } else if (!modalBox.contains(e.target) && !modalBtn.contains(e.target) && modalOpen === true) {
            closeModal()
        }
    } else {
        dialogBox.classList.remove('dialogAnimate');
        void dialogBox.offsetWidth; // Trigger reflow to restart the animation
        dialogBox.classList.add('dialogAnimate');
    }
});


// close the dialog box
let dialogIsOpen = false;
function dialogClose () {
    document.querySelector('#dialogButtons').innerHTML = '';
    document.querySelector('#dialogText').textContent = '';
    dialog.classList.add('hidden');
    dialogBox.classList.remove('dialogAnimate');
    dialogIsOpen = false;
}

// open the dialog box
function dialogOpen(type) {
    dialogIsOpen = true;
    const dialog = document.querySelector('#dialog')
    const dialogBox = document.querySelector('#dialogBox')
    if (type === 'deleteUser') {
        dialog.classList.remove('hidden');
        dialogBox.classList.add('dialogAnimate');
        document.querySelector('#dialogText').textContent = 'Are you sure you want to delete your account?';
        document.querySelector('#dialogButtons').innerHTML = `
        <button onclick='dialogClose()' class='bg-blue-500 text-white rounded-md p-2 hover:bg-opacity-80' id='dialogCancel'>Cancel</button>
        <button onclick='deleteUserFunc()' class='bg-red-500 text-white rounded-md p-2 hover:bg-opacity-80' id='dialogConfirm'>Delete account</button>
        `;
    }
}

function linkToFunc(location = '') {
    location = '/' + location;
    if (window.location.href.includes('next')) {
        let nextString = '?next=' + window.location.href.split('next=')[1];
        // window.location.href = window.location.href.replace(window.location.pathname.split('/')[1], location);
        window.location.href = location + nextString;
    } else {
        window.location.href = location;
    }
}

function togglePasswordVisibility(passwordInputId, iconContainerId) {
    const passwordInput = document.getElementById(passwordInputId); // Adjust ID as needed
    const iconContainer = document.getElementById(iconContainerId)

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        iconContainer.classList.remove('showing-eye-off');
        iconContainer.classList.add('showing-eye-on');
    } else {
        passwordInput.type = 'password';
        iconContainer.classList.remove('showing-eye-on');
        iconContainer.classList.add('showing-eye-off');
    }
};