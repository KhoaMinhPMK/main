let stored_problems = [];
let messages_history = [];
function saveUserInfo(userId, userName) {
    localStorage.setItem("userId", userId);
    localStorage.setItem("userName", userName);
}

let message_queue = [];
let user_message_history = [];
let saveTimeout;
let lastUserMessage = ""; // To keep track of the last user message
let lastBotMessage = ""; // To keep track of the last bot message

// Function to mark a message as disliked and save it
function dislikeMessage(button) {
    const bot_reply = button.parentElement;
    bot_reply.classList.add("disliked");

    // Clear the timeout if a message is disliked
    clearTimeout(saveTimeout);

    // Save the disliked bot message along with the last user message immediately
    saveDislikedMessage(lastUserMessage, bot_reply.innerText);

    // Add your custom logic here, e.g., sending the dislike status to the server
    console.log("Disliked message:", bot_reply.innerHTML);
}

// Function to save disliked bot message along with the user's last message
function saveDislikedMessage(userMessage, botMessage) {
    const userId = localStorage.getItem('userId');
    const userName = localStorage.getItem('userName');

    user_message_history.push({
        user_id: userId,
        user_name: userName,
        user_message: userMessage,
        bot_message: botMessage,
        disliked: true
    });
    saveDislikedMessageHistory();
}

// Function to save user message and track bot responses
function saveUserMessage(message, botMessage) {
    if (message.length > 30) {
        const userId = localStorage.getItem('userId');
        const userName = localStorage.getItem('userName');

        console.log("Queueing user message:", message);
        
        lastBotMessage = botMessage; // Save the last bot message

        lastUserMessage = message; // Save the last user message

        message_queue.push({ user_id: userId, user_name: userName, user_message: message, bot_message: lastBotMessage });

        // Clear the previous timeout
        clearTimeout(saveTimeout);

        // Set a new timeout to save non-disliked messages after 60 seconds
        saveTimeout = setTimeout(() => {
            saveNonDislikedMessageHistory();
        }, 60000);
    }
}

// Function to save disliked message history
async function saveDislikedMessageHistory() {
    if (user_message_history.length > 0) {
        try {
            const payload = { user_message_history };
            console.log("Payload sent to server (disliked):", payload);

            const response = await fetch("https://fispage.com/math/php/log_chat_messages.php", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                console.log("User message history saved successfully.");
                user_message_history = [];
            } else {
                console.error("Failed to save user message history.");
            }
        } catch (error) {
            console.error("Error occurred while saving user message history:", error);
        }
    }
}

// Function to save non-disliked message history
async function saveNonDislikedMessageHistory() {
    if (message_queue.length > 0) {
        try {
            const payload = { user_message_history: message_queue };
            console.log("Payload sent to server (non-disliked):", payload);

            const response = await fetch("https://fispage.com/math/php/log_non_disliked_messages.php", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                console.log("Non-disliked user message history saved successfully.");
                message_queue = [];
            } else {
                console.error("Failed to save non-disliked user message history.");
            }
        } catch (error) {
            console.error("Error occurred while saving non-disliked user message history:", error);
        }
    }
}


// Function to handle user input and track the previous message
function handleUserInput(message) {
    console.log("Handling user input:", message);
    saveUserMessage(message); // Save the message to user_message_history
}

// Call this function to save bot responses
function handleBotResponse(message) {
    console.log("Handling bot response:", message);
    saveBotMessage(message); // Save the bot message to message_queue
}

// Call this function to save bot responses
function handleBotResponse(message) {
    console.log("Handling bot response:", message);
    saveBotMessage(message); // Save the bot message to message_queue
}


async function send_message() {
    const message_box = document.getElementById("message_box");
    const image_input = document.getElementById("image_input");
    const messages = document.getElementById("messages");
    const message_text = message_box.value.trim();
    const file = image_input.files[0];

    if (message_text === "" && !file) {
        return; // Không gửi khi không có tin nhắn văn bản hoặc ảnh
    }

    // Add user's message to the message box
    const user_message = document.createElement("div");
    user_message.classList.add("message", "user-message");

    if (message_text !== "") {
        user_message.textContent = message_text;
    } else {    
        user_message.textContent = "Image uploaded";
    }
    messages.appendChild(user_message);

    // Scroll to the bottom of the message list
    messages.scrollTop = messages.scrollHeight;

    // Lấy userId từ localStorage
    const userId = localStorage.getItem("userId");
    // const userId = 10101;
    let payload = {
        userId: userId // Thêm userId vào payload
    };

    if (message_text !== "") {
        payload.message = message_text;
    }

    if (file) {
        const reader = new FileReader();
        reader.onload = async function(e) {
            const image_data = e.target.result.split(',')[1]; // Remove the base64 header
            payload.image = image_data;

            // Send message to the API and handle the response
            await sendToAPI(payload, messages);
        };
        reader.readAsDataURL(file);
    } else {
        // Send message to the API and handle the response
        await sendToAPI(payload, messages);
    }

    // Clear the input box and image input after sending the message
    message_box.value = "";
    image_input.value = "";
}

async function sendToAPI(payload, messages) {
    try {
        const response = await fetch("https://main-sig4k6gkea-uc.a.run.app/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });
        

        if (response.ok) {
            const data = await response.json();
            if (data.problems) {
                stored_problems = data.problems; // Lưu trữ dữ liệu bài tập và lời giải
                renderProblems(messages);
            } else {
                const bot_reply = document.createElement("div");
                bot_reply.classList.add("message", "bot-message");

                // Kiểm tra nếu bot message chứa từ "Kết quả dự đoán:"
                if (data.response.includes("Kết quả dự đoán:")) {
                    bot_reply.innerHTML = `${data.response} 
                        <button class="dislike-button" onclick="dislikeMessage(this)">
                            <i class="fas fa-thumbs-down"></i>
                        </button>`;
                    saveUserMessage(payload.message, data.response);
                } else {
                    bot_reply.innerHTML = data.response;
                }

                messages.appendChild(bot_reply);
                messages_history.push(bot_reply.outerHTML);

                // Thêm sự kiện nhấp chuột phải và giữ ngón tay cho tin nhắn bot
                bot_reply.addEventListener('contextmenu', (event) => showContextMenu(event, bot_reply));
                bot_reply.addEventListener('touchstart', handleTouchStart, false);
                bot_reply.addEventListener('touchend', handleTouchEnd, false);
            }

            // Re-render MathJax after new content is added
            MathJax.typesetPromise();

            // Scroll to the bottom of the message list
            messages.scrollTop = messages.scrollHeight;
        } else {
            console.error("API request failed with status:", response.status);
        }
    } catch (error) {
        console.error("Error occurred while sending message to API:", error);
    }
}

function renderProblems(messages) {
    stored_problems.forEach((prob, index) => {
        const bot_reply = document.createElement("div");
        bot_reply.classList.add("message", "bot-message", "problem");

        const problem_text = document.createElement("div");
        problem_text.innerHTML = `<strong style="color: #4285f4;">Bài tập ${index + 1}:</strong><br>${prob.problem}`;

        bot_reply.appendChild(problem_text);

        const solution_checkbox = document.createElement("input");
        solution_checkbox.type = "checkbox";
        solution_checkbox.id = `show_solution_${index}`;
        solution_checkbox.dataset.index = index; // Lưu index vào data attribute để lấy lại sau này
        solution_checkbox.addEventListener("change", () => {
            renderSolution(messages);
        });
        const solution_label = document.createElement("label");
        solution_label.setAttribute("for", `show_solution_${index}`);
        solution_label.textContent = "Hiển thị lời giải";
        bot_reply.appendChild(solution_checkbox);
        bot_reply.appendChild(solution_label);

        const save_button = document.createElement("button");
        save_button.classList.add("save-button");
        save_button.innerHTML = '<i class="fas fa-save"></i>';
        save_button.onclick = () => saveMessage(save_button);
        bot_reply.appendChild(save_button);

        // Thêm icon dấu 3 chấm để mở context menu
        const menu_button = document.createElement("button");
        menu_button.classList.add("menu-button");
        menu_button.innerHTML = '<i class="fas fa-ellipsis-h"></i>';
        menu_button.onclick = (event) => showContextMenu(event, bot_reply);
        bot_reply.appendChild(menu_button);

        messages.appendChild(bot_reply);

        // Lưu trữ lịch sử tin nhắn
        messages_history.push(bot_reply.outerHTML);

        // Thêm sự kiện nhấp chuột phải và giữ ngón tay cho tin nhắn bài tập
        bot_reply.addEventListener('contextmenu', (event) => showContextMenu(event, bot_reply));
        bot_reply.addEventListener('touchstart', handleTouchStart, false);
        bot_reply.addEventListener('touchend', handleTouchEnd, false);
    });

    // Re-render MathJax after new content is added
    MathJax.typesetPromise();

    // Scroll to the bottom of the message list
    messages.scrollTop = messages.scrollHeight;
}

function renderSolution(messages) {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach((checkbox, checkboxIndex) => {
        const index = checkbox.dataset.index;
        const show_solution = checkbox.checked;

        const problem = stored_problems[index];

        // Locate the problem_node based on checkbox index
        const problem_node = Array.from(messages.children).find((child, childIndex) => {
            // Check if this child corresponds to the current problem node
            return child.textContent.includes(`Bài tập ${parseInt(index) + 1}:`);
        });

        console.log(`Problem node at index ${checkboxIndex * 2}:`, problem_node);

        if (!problem_node) {
            console.warn(`Problem node is undefined at index ${checkboxIndex * 2}`);
            return; // Skip to the next iteration if problem_node is undefined
        }

        let existing_solution_node = problem_node.nextSibling;
        console.log(`Existing solution node:`, existing_solution_node);

        if (show_solution) {
            if (!existing_solution_node || !existing_solution_node.classList.contains("solution")) {
                const solution_text = document.createElement("div");
                solution_text.classList.add("message", "bot-message", "solution");
                solution_text.innerHTML = `<strong>Lời giải ${parseInt(index) + 1}:</strong><br>${problem.solution} <button class="save-button" onclick="saveMessage(this)"><i class="fas fa-save"></i></button>`;

                // Thêm icon dấu 3 chấm để mở context menu
                const menu_button = document.createElement("button");
                menu_button.classList.add("menu-button");
                menu_button.innerHTML = '<i class="fas fa-ellipsis-v"></i>';
                menu_button.onclick = (event) => showContextMenu(event, solution_text);
                solution_text.appendChild(menu_button);

                messages.insertBefore(solution_text, problem_node.nextSibling);

                // Update the message history list
                messages_history.splice(parseInt(index) + 1, 0, solution_text.outerHTML);

                // Thêm sự kiện nhấp chuột phải và giữ ngón tay cho tin nhắn lời giải
                solution_text.addEventListener('contextmenu', (event) => showContextMenu(event, solution_text));
                solution_text.addEventListener('touchstart', handleTouchStart, false);
                solution_text.addEventListener('touchend', handleTouchEnd, false);
            }
        } else {
            while (existing_solution_node && existing_solution_node.classList.contains("solution")) {
                messages.removeChild(existing_solution_node);

                // Update the message history list
                messages_history.splice(parseInt(index) + 1, 1);

                existing_solution_node = problem_node.nextSibling; // Update existing_solution_node
            }
        }
    });

    // Re-render MathJax after new content is added
    MathJax.typesetPromise();

    // Scroll to the bottom of the message list
    messages.scrollTop = messages.scrollHeight;
}


function handleTouchStart(event) {
    this.touchStartTime = Date.now();
}

function handleTouchEnd(event) {
    const touchDuration = Date.now() - this.touchStartTime;
    if (touchDuration > 500) { // Nếu giữ ngón tay lâu hơn 500ms thì hiển thị menu tùy chọn
        showContextMenu(event, this);
    }
}
document.addEventListener('DOMContentLoaded', function() {
    const userId = localStorage.getItem("userId");
    const userName = localStorage.getItem("userName");
    
    console.log("User ID:", userId);
    console.log("User Name:", userName);
});

let hasShownAlert = false;
// Lưu dữ liệu tin nhắn vào cơ sở dữ liệu
function saveMessage(button) {
    const message = button.parentElement.cloneNode(true); // Clone the message element to manipulate

    // Remove unwanted elements
    const unwantedElements = message.querySelectorAll('.save-button, .menu-button, input[type="checkbox"], label');
    unwantedElements.forEach(element => element.remove());

    const messageContent = message.innerHTML.trim();  // Get the innerHTML of the modified message
    const userId = localStorage.getItem("userId");
    const userName = localStorage.getItem("userName");

    const data = {
        userId: userId,
        userName: userName,
        messageContent: messageContent
    };

    console.log(data);  // Check the data before sending

    fetch('https://fispage.com/math/php/save_message.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
            alert('Error saving message: ' + data.error);
        } else {
            if (!hasShownAlert) {
                alert('Messages saved successfully!');
                hasShownAlert = true;
            }
            cancelSelection(); // Hide toolbar and show input bar after saving
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred while saving the message.');
    });
}




function checkEnter(event) {
    if (event.key === "Enter") {
        send_message();
    }
}
const body = document.querySelector('body'),
      sidebar = body.querySelector('nav'),
      toggle = body.querySelector(".toggle"),
      searchBtn = body.querySelector(".search-box"),
      modeSwitch = body.querySelector(".toggle-switch"),
      modeText = body.querySelector(".mode-text"),
      bottomToolbar = document.getElementById("bottom-toolbar"),
      homeSection = document.querySelector(".home");

// Cập nhật vị trí bottom-toolbar khi sidebar thay đổi
const updateBottomToolbarPosition = () => {
    if (sidebar.classList.contains("close")) {
        homeSection.style.left = "78px";
        homeSection.style.width = "calc(100% - 78px)";
    } else {
        homeSection.style.left = "250px";
        homeSection.style.width = "calc(100% - 250px)";
    }
    bottomToolbar.style.left = "50%";  // Đảm bảo bottom-toolbar luôn nằm giữa
    bottomToolbar.style.transform = "translateX(-50%)";
};

toggle.addEventListener("click", () => {
    sidebar.classList.toggle("close");
    updateBottomToolbarPosition();
});

searchBtn.addEventListener("click", () => {
    sidebar.classList.remove("close");
    updateBottomToolbarPosition();
});

modeSwitch.addEventListener("click", () => {
    body.classList.toggle("dark");
    
    if (body.classList.contains("dark")) {
        modeText.innerText = "Light mode";
    } else {
        modeText.innerText = "Dark mode";
    }
});

document.addEventListener("DOMContentLoaded", () => {
    updateBottomToolbarPosition();  // Gọi khi tải trang
});


// --------------------------------------------------------------------------------------------------
// --------------------------------------------------------------------------------------------------
// Hàm để hiển thị menu tùy chọn tin nhắn
function isMobileDevice() {
    return (typeof window.orientation !== "undefined") || (navigator.userAgent.indexOf('IEMobile') !== -1);
}

function showContextMenu(event, messageElement) {
    event.preventDefault();
    event.stopPropagation();

    const menu = document.getElementById('message-context-menu');
    const clickX = event.clientX;
    const clickY = event.clientY;
    const screenWidth = window.innerWidth;
    const screenHeight = window.innerHeight;
    const menuWidth = menu.offsetWidth;
    const menuHeight = menu.offsetHeight;

    // Tính toán vị trí xuất hiện của menu
    let menuX = clickX;
    let menuY = clickY;

    // Điều chỉnh vị trí nếu menu vượt quá kích thước màn hình
    if ((clickX + menuWidth) > screenWidth) {
        menuX = screenWidth - menuWidth - 10; // 10 là khoảng cách đệm từ cạnh màn hình
    }
    if ((clickY + menuHeight) > screenHeight) {
        menuY = screenHeight - menuHeight - 10;
    }

    // Đặt vị trí của menu
    menu.style.display = 'block';
    menu.style.left = `${menuX}px`;
    menu.style.top = `${menuY}px`;

    // Đảm bảo rằng menu sẽ ẩn khi nhấp vào nơi khác
    document.addEventListener('click', function hideContextMenu() {
        menu.style.display = 'none';
        document.removeEventListener('click', hideContextMenu);
    });

    // Gán tin nhắn hiện tại để sử dụng trong các hành động menu
    menu.currentMessage = messageElement;
}
function showMenuNextToButton(event, buttonElement) {
    event.preventDefault();
    event.stopPropagation();

    const menu = document.getElementById('message-context-menu');
    const buttonRect = buttonElement.getBoundingClientRect();
    const menuWidth = menu.offsetWidth;
    const menuHeight = menu.offsetHeight;
    const screenWidth = window.innerWidth;
    const screenHeight = window.innerHeight;

    // Đặt vị trí của menu bên phải nút
    let menuLeft = buttonRect.right;
    let menuTop = buttonRect.top;

    // Điều chỉnh vị trí nếu menu vượt quá kích thước màn hình bên phải
    if ((menuLeft + menuWidth) > screenWidth) {
        menuLeft = buttonRect.left - menuWidth;
    }

    // Điều chỉnh vị trí nếu menu vượt quá kích thước màn hình bên dưới
    if ((menuTop + menuHeight) > screenHeight) {
        menuTop = screenHeight - menuHeight;
    }

    // Điều chỉnh vị trí nếu menu vượt quá kích thước màn hình bên trên
    if (menuTop < 0) {
        menuTop = 0;
    }

    menu.style.display = 'block';
    menu.style.left = `${menuLeft}px`;
    menu.style.top = `${menuTop}px`;

    // Đảm bảo rằng menu sẽ ẩn khi nhấp vào nơi khác
    document.addEventListener('click', function hideContextMenu() {
        menu.style.display = 'none';
        document.removeEventListener('click', hideContextMenu);
    });
}








// Các hàm cho các hành động của menu
function copyMessage() {
    const message = document.getElementById('message-context-menu').currentMessage;
    navigator.clipboard.writeText(message.textContent);
    alert('Copied tin nhắn!');
}

function pinMessage() {
    const message = document.getElementById('message-context-menu').currentMessage;
    // Logic để ghim tin nhắn
    alert('Ghim tin nhắn!');
}

function markMessage() {
    const message = document.getElementById('message-context-menu').currentMessage;
    // Logic để đánh dấu tin nhắn
    alert('Đánh dấu tin nhắn!');
}

function saveMessageToDevice() {
    const message = document.getElementById('message-context-menu').currentMessage;
    // Logic để lưu tin nhắn về máy
    alert('Lưu về máy!');
}
document.addEventListener("DOMContentLoaded", () => {
    selectingMultiple = false;
    const messages = document.getElementById("messages");
    const bottomToolbar = document.getElementById("bottom-toolbar");
    const inputContainer = document.querySelector(".input-container");
    const homeSection = document.querySelector(".home");
    messages.classList.remove("selecting");
    bottomToolbar.style.display = "none";

    // Cập nhật vị trí bottom-toolbar khi sidebar thay đổi
    const updateBottomToolbarPosition = () => {
        const sidebar = document.querySelector(".sidebar");
        const homeWidth = homeSection.offsetWidth;
        bottomToolbar.style.width = `${homeWidth * 0.7}px`;  // Cập nhật chiều rộng
        bottomToolbar.style.left = "50%";
        bottomToolbar.style.transform = "translateX(-50%)";
    };

    // Lắng nghe sự kiện thay đổi của sidebar
    const sidebarToggleBtn = document.querySelector(".sidebar-toggle");
    if (sidebarToggleBtn) {
        sidebarToggleBtn.addEventListener("click", () => {
            document.querySelector(".sidebar").classList.toggle("close");
            updateBottomToolbarPosition();
        });
    }

    window.addEventListener("resize", updateBottomToolbarPosition);  // Cập nhật khi thay đổi kích thước cửa sổ

    updateBottomToolbarPosition();  // Gọi khi tải trang
});

function selectMultipleMessages() {
    const messages = document.getElementById("messages");
    const inputContainer = document.querySelector(".input-container");
    const bottomToolbar = document.getElementById("bottom-toolbar");

    selectingMultiple = !selectingMultiple;

    if (selectingMultiple) {
        messages.classList.add("selecting");
        bottomToolbar.style.display = "flex";
        inputContainer.classList.add("hidden");
    } else {
        messages.classList.remove("selecting");
        bottomToolbar.style.display = "none";
        inputContainer.classList.remove("hidden");
        resetCheckboxes();
    }

    const allMessages = messages.querySelectorAll(".message.bot-message");
    allMessages.forEach(message => {
        let checkbox = message.querySelector(".message-checkbox");
        if (!checkbox) {
            checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.className = "message-checkbox";
            message.insertBefore(checkbox, message.firstChild);
        }
    });

    updateBottomToolbarPosition();  // Cập nhật vị trí khi hiển thị bottom-toolbar
}

function cancelSelection() {
    selectingMultiple = false;
    const messages = document.getElementById("messages");
    const bottomToolbar = document.getElementById("bottom-toolbar");
    const inputContainer = document.querySelector(".input-container");
    messages.classList.remove("selecting");
    bottomToolbar.style.display = "none";
    inputContainer.classList.remove("hidden");
    resetCheckboxes();
}



function viewDetails() {
    const message = document.getElementById('message-context-menu').currentMessage;
    // Logic để xem chi tiết tin nhắn
    alert('Xem chi tiết!');
}

function retractMessage() {
    const message = document.getElementById('message-context-menu').currentMessage;
    // Logic để thu hồi tin nhắn
    alert('Thu hồi tin nhắn!');
}

function deleteMessageForMe() {
    const message = document.getElementById('message-context-menu').currentMessage;
    message.remove();
    alert('Xóa tin nhắn ở phía tôi!');
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.bot-message').forEach(message => {
        message.addEventListener('contextmenu', (event) => showContextMenu(event, message));
        message.addEventListener('touchstart', handleTouchStart, false);
        message.addEventListener('touchend', handleTouchEnd, false);
    });
});

let touchTimer;

function handleTouchStart(event) {
    const messageElement = event.currentTarget;

    // Bắt đầu một bộ đếm thời gian khi người dùng chạm vào tin nhắn
    touchTimer = setTimeout(() => {
        showContextMenu(event, messageElement);
    }, 400); // 1 giây
}

function handleTouchEnd(event) {
    // Hủy bộ đếm thời gian nếu người dùng nhấc ngón tay trước khi hết thời gian
    clearTimeout(touchTimer);
}



function resetCheckboxes() {
    const checkboxes = document.querySelectorAll(".message-checkbox");
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
    });
}

function getSelectedMessages() {
    const selectedMessages = [];
    const checkboxes = document.querySelectorAll(".message-checkbox:checked");
    checkboxes.forEach(checkbox => {
        const message = checkbox.parentElement;
        selectedMessages.push(message);
    });
    return selectedMessages;
}

function copySelectedMessages() {
    const selectedMessages = getSelectedMessages();
    const messageContents = selectedMessages.map(message => message.textContent.trim()).join("\n");
    navigator.clipboard.writeText(messageContents).then(() => {
        alert("Copied selected messages to clipboard!");
    }).catch(err => {
        console.error("Could not copy text: ", err);
    });
}

function saveSelectedMessages() {
    const selectedMessages = getSelectedMessages();
    selectedMessages.forEach(message => saveMessage(message.querySelector(".save-button")));
}

function downloadSelectedMessages() {
    const selectedMessages = getSelectedMessages();
    const messageContents = selectedMessages.map(message => message.textContent.trim()).join("\n");
    const blob = new Blob([messageContents], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "selected_messages.txt";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}
document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM fully loaded and parsed");

    // Kiểm tra trạng thái đăng nhập
    var userName = localStorage.getItem('userName');
    console.log("Retrieved userName from localStorage:", userName);

    var userGreeting = document.getElementById('user-greeting');
    var userNameElement = document.getElementById('user-name');

    if (userName) {
        // Người dùng đã đăng nhập
        console.log("User is logged in, displaying greeting");
        userGreeting.classList.remove('d-none');
        userNameElement.textContent = userName;
    } else {
        // Người dùng chưa đăng nhập
        console.log("User is not logged in, hiding greeting");
        userGreeting.classList.add('d-none');
    }
});

// Hàm ẩn phần tử #user-greeting khi người dùng nhập tin nhắn
document.getElementById('message_box').addEventListener('input', function() {
    document.getElementById('user-greeting').classList.add('d-none');
});
document.getElementById("modelButton").addEventListener("click", function(event){
    event.preventDefault();
    var dropdown = document.getElementById("dropdownMenu");
    if (dropdown.style.display === "block") {
        dropdown.style.display = "none";
    } else {
        dropdown.style.display = "block";
    }
});

window.onclick = function(event) {
    if (!event.target.matches('#modelButton') && !event.target.closest('.nav-link')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.style.display === "block") {
                openDropdown.style.display = "none";
            }
        }
    }
}
