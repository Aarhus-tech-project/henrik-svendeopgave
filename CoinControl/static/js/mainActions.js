// If on homepage allow changing of user info
let modalBtn;
document.addEventListener('DOMContentLoaded', () => {
    
    if (window.location.pathname == '/') {
        // Transaction click
        document.querySelector('#menuBox').classList.add('menuBoxOff')
        const transactionElms = document.querySelectorAll('.transaction');
        if (transactionElms.length > 0) {
            transactionElms.forEach(transaction => {
                let transactionId = transaction.getAttribute('id').split('transaction')[1];
                transaction.addEventListener('click', () => {
                    modalBtn = transaction.getAttribute('id');
                    document.querySelector('#deleteTransactionBtn').setAttribute('onclick', `dialogOpen("deleteTransaction", ${transactionId})`)
                    openModal('updateTransaction', transactionId)
                })
            });
        };
        
        // Username click
        const username = document.querySelector('#userName');
        username.classList.add('cursor-pointer', 'hover:opacity-70');
        username.setAttribute('onClick', "openModal('user')")
        username.addEventListener('click', () => {
            modalBtn = username.getAttribute('id');
        });

        if (transactions.length > 0) {
            transactions.forEach(transaction => {
                let transactionValue = parseFloat(transaction['value'].replace(',', '').replace(/^[^\d]+/, ''));
                let transactionDate = transaction['date']
                let dateObject = new Date(transactionDate); // Convert to Date object
                let currency = transaction['value'].replace(/[0-9.,-]+/g, '').trim();
                let value = document.querySelector(`#value${transaction['id']}`)

                if (transaction['negative'] == true) {
                    value.textContent = `${currency} -${transactionValue.toFixed(2)}`
                    value.classList.add('text-red-800')
                }else {
                    value.textContent = `${currency} ${transactionValue.toFixed(2)}`
                    value.classList.remove('text-red-800')
                }
                
                // Format the date to YYYY-MM-DD
                let year = dateObject.getFullYear();
                let month = ('0' + (dateObject.getMonth() + 1)).slice(-2);
                let day = ('0' + dateObject.getDate()).slice(-2);
                let formattedDate = `${year}-${month}-${day}`;

                transaction['value'] = transactionValue;
                transaction['date'] = formattedDate;
            })            
        }
    } else {
        document.querySelector('#userName').classList.remove('cursor-pointer', 'hover:opacity-70');
    }
});


// Get token
function getToken(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            };
        };
    };
    return cookieValue;
};

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
    menuBox.classList.add('menuBoxOff')
    
    if (window.location.pathname == '/') {
        button.classList.remove('rotate-45', 'font-[900]');
        
        if (button.classList.contains('menuBtnOn')) {
            button.classList.remove('menuBtnOn');
            menuBox.classList.remove('menuBoxOn')
            button.classList.add('menuBtnOff');
            menuBox.classList.add('menuBoxOff')
            menuOpen = false;
        } else {
            button.classList.remove('menuBtnOff');
            menuBox.classList.remove('menuBoxOff')
            button.classList.add('menuBtnOn');
            menuBox.classList.add('menuBoxOn')
            menuOpen = true;
        }
        
        if (menuBox.classList.contains('hidden')) {
            menuBox.classList.remove('hidden')
            menuBox.classList.add('w-44')
            menuBox.style.top = `${btnRect.bottom}px`;
            menuBox.style.left = `${btnRect.right - menuBox.getBoundingClientRect().width}px`;
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
function openModal(type, transactionId = null) {
    modalOpen = true;
    document.getElementById("blurBackground").classList.remove("duration-300");
    document.querySelector("#modal").classList.remove("hidden");
    document.querySelector("#blurBackground").classList.add("blur-sm", "backdrop-blur-sm", "duration-700");
    
    if (type === 'user') {
        document.querySelector('#updateUserBtn').setAttribute('onclick', `checkUpdateUser(${JSON.stringify(userInfo)})`);
        document.querySelector('#modalUser').classList.remove('hidden');
        document.querySelector('#modalTransaction').classList.add('hidden');
        document.querySelector('#modalUpdateTransaction').classList.add('hidden');
        
        document.querySelector('#userNameUser').value = userInfo.username;
        document.querySelector('#emailUser').value = userInfo.email;
        document.querySelector('#firstNameUser').value = userInfo.first_name;
        document.querySelector('#lastNameUser').value = userInfo.last_name;
    } else if (type === 'transaction') {
        document.querySelector('#modalTransaction').classList.remove('hidden');
        document.querySelector('#modalUser').classList.add('hidden');
        document.querySelector('#modalUpdateTransaction').classList.add('hidden');

        let dateObject = new Date();
        let year = dateObject.getFullYear();
        let month = ('0' + (dateObject.getMonth() + 1)).slice(-2);
        let day = ('0' + dateObject.getDate()).slice(-2);
        let formattedDate = `${year}-${month}-${day}`;

        document.querySelector('#dateTransaction').value = formattedDate
        document.querySelector('#currencyTransaction').value = 'DKK (default)'


    } else if (type === 'updateTransaction') {
        document.querySelector('#modalUpdateTransaction').classList.remove('hidden');
        document.querySelector('#modalUser').classList.add('hidden');
        document.querySelector('#modalTransaction').classList.add('hidden');
        
        transactions.forEach(transaction => {
            if (transaction['id'] == transactionId) {
                console.table(transaction)
                document.querySelector('#updateTransactionTitle').textContent = 'Update transaction ' + transactionId;

                document.querySelector('#dateUpdateTransaction').value = transaction['date']
                if (transaction['negative']) {
                    document.querySelector('#valueUpdateTransaction').value = `-${transaction['value'].toFixed(2)}`
                } else {
                    document.querySelector('#valueUpdateTransaction').value = transaction['value'].toFixed(2)
                }
                document.querySelector('#currencyUpdateTransaction').value = transaction['currency']
                if (transaction['recipient']) {
                    document.querySelector('#recipientUpdateTransaction').value = transaction['recipient']
                }
                if (transaction['account_alias']) {
                    document.querySelector('#accountUpdateTransaction').value = transaction['account_alias']
                } else {
                    document.querySelector('#accountUpdateTransaction').value = transaction['account_name']
                }
                document.querySelector('#notesUpdateTransaction').value = transaction['notes']
                document.querySelector('#updateTransactionBtn').setAttribute('onclick', `updateTransaction(${transactionId})`)

            }
        })
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

// add transaction function
function addTransaction() {
    let date = document.querySelector('#dateTransaction').value
    let value = document.querySelector('#valueTransaction').value
    let currency = document.querySelector('#currencyTransaction').value
    let recipient = document.querySelector('#recipientTransaction').value
    let account = document.querySelector('#accountTransaction').value
    let notes = document.querySelector('#notesTransaction').value
    let transactionError = document.querySelector('#transactionError')
    let csrftoken = getToken('csrftoken');
    let url = '/add_transaction'

    if (value == null || account == null) {
        transactionError.textContent = 'The value field and the account field has to be filled out';
        transactionError.classList.remove('hidden');
    } else {
        transactionError.textContent = '';
        transactionError.classList.add('hidden');

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({date: date, value: value, currency: currency, recipient: recipient, account: account, notes: notes})
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                console.error('Add transaction failed');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

// update transaction function
function updateTransaction(id) {
    let date = document.querySelector('#dateUpdateTransaction').value
    let value = document.querySelector('#valueUpdateTransaction').value
    let currency = document.querySelector('#currencyUpdateTransaction').value
    let recipient = document.querySelector('#recipientUpdateTransaction').value
    let account = document.querySelector('#accountUpdateTransaction').value
    let notes = document.querySelector('#notesUpdateTransaction').value
    let updateTransactionError = document.querySelector('#updateTransactionError')
    let csrftoken = getToken('csrftoken');
    let url = '/update_transaction'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({id: id, date: date, value: value, currency: currency, recipient: recipient, account: account, notes: notes})
    })
    .then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            console.error('Add transaction failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// delete user function
function deleteUserFunc() {
    let csrftoken = getToken('csrftoken');
    let url = '/delete_user';

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
            console.error('Delete user failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
};

// delete transaction function
function deleteTransactionFunc(id) {
    let csrftoken = getToken('csrftoken');
    let url = '/delete_transaction';

    dialogClose();

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({id: id})
    })
    .then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            console.error('Delete transaction failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
};

// delete account function
function deleteAccountFunc(id) {
    let csrftoken = getToken('csrftoken');
    let url = '/delete_account';

    dialogClose();

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({id: id})
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

// Esc
document.addEventListener('keydown', (e) => {
    let button = document.querySelector('#menuBtn');
    let menuBox = document.querySelector('#menuBox');
    let dialogBox = document.querySelector('#dialogBox');
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

// click outside
document.addEventListener('click', (e) => {
    let menuBtn = document.querySelector('#menuBtn');
    let modalBox = document.querySelector('#modalBox');
    let dialogBox = document.querySelector('#dialogBox');
    let btnModal = document.getElementById(modalBtn)

    // close menu if clicked outside
    if (dialogIsOpen === false) {
        if (!menuBtn.contains(e.target) && menuOpen === true) {
            toggleMenu()
        } else if (!modalBox.contains(e.target) && !btnModal.contains(e.target) && modalOpen === true) {
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
function dialogOpen(type, id=null) {
    dialogIsOpen = true;
    const dialog = document.querySelector('#dialog')
    const dialogBox = document.querySelector('#dialogBox')
    if (type === 'deleteUser') {
        dialog.classList.remove('hidden');
        dialogBox.classList.add('dialogAnimate');
        document.querySelector('#dialogText').textContent = 'Are you sure you want to delete your user?';
        document.querySelector('#dialogButtons').innerHTML = `
        <button onclick='dialogClose()' class='bg-blue-500 text-white rounded-md p-2 hover:bg-opacity-80' id='dialogCancel'>Cancel</button>
        <button onclick='deleteUserFunc()' class='bg-red-500 text-white rounded-md p-2 hover:bg-opacity-80' id='dialogConfirm'>Delete user</button>
        `;
    } else if (type === 'deleteTransaction') {
        dialog.classList.remove('hidden');
        dialogBox.classList.add('dialogAnimate');
        document.querySelector('#dialogText').textContent = 'Are you sure you want to delete your transaction?';
        document.querySelector('#dialogButtons').innerHTML = `
        <button onclick='dialogClose()' class='bg-blue-500 text-white rounded-md p-2 hover:bg-opacity-80' id='dialogCancel'>Cancel</button>
        <button onclick=deleteTransactionFunc(${id}) class='bg-red-500 text-white rounded-md p-2 hover:bg-opacity-80' id='dialogConfirm'>Delete transaction</button>
        `;
    } else if (type === 'deleteAccount') {
        dialog.classList.remove('hidden');
        dialogBox.classList.add('dialogAnimate');
        document.querySelector('#dialogText').textContent = 'Are you sure you want to delete your account?';
        document.querySelector('#dialogButtons').innerHTML = `
        <button onclick='dialogClose()' class='bg-blue-500 text-white rounded-md p-2 hover:bg-opacity-80' id='dialogCancel'>Cancel</button>
        <button onclick=deleteAccountFunc(${id}) class='bg-red-500 text-white rounded-md p-2 hover:bg-opacity-80' id='dialogConfirm'>Delete account</button>
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