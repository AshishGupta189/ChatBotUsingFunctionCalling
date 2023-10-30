document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const userInputElement = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const url='http://127.0.0.1:5000/getWeather';

    let typingMessageElement = null;


    sendButton.addEventListener("click", function () {
        const userMessage = userInputElement.value;
        if (userMessage) {
            appendUserMessage(userMessage);
            userInputElement.value = "";
            simulateAssistantTyping();
            callAssistantAPI(userMessage);
        }
    });

    async function callAssistantAPI(userMessage) {
        try{
            console.log("here");
            const response=await fetch(url,{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({userMessage}),
            })
            console.log("m1");
            if(response.ok){
                const data=await response.json();
                console.log(data)
                removeTypingMessage();
                simulateAssistantResponse(data['assistant_reply'])
            }else{
                console.log("error")
            }

        }catch(error){
            console.log(error)
        }
        
    }

    function removeTypingMessage() {
        if (typingMessageElement) {
            chatBox.removeChild(typingMessageElement);
            typingMessageElement = null;
        }
    }
                
    function appendUserMessage(message) {
        const messageElement = createMessageElement(message, "user-message");
        chatBox.appendChild(messageElement);
    }

    function simulateAssistantTyping() {
        const typingMessage = createTypingMessage();
        chatBox.appendChild(typingMessage);
    }

        function simulateAssistantResponse(assistantReply) {
            console.log("function called response");
                const responseMessage = createAssistantMessage("Assistant: " + assistantReply);        
        }


    function createTypingMessage() {
        typingMessageElement= createMessageElement("Assistant is typing...", "assistant-message message-text typing");
        return typingMessageElement;
    }

    function createAssistantMessage(message) {
        console.log("function called message");
        const messageElement= createMessageElement(message, "assistant-message");
        chatBox.appendChild(messageElement);
    }

    function createMessageElement(message, className) {
        console.log("function called");
        const messageElement = document.createElement("div");
        const classNames = className.split(" "); // Split the class name by space
        classNames.forEach(name => {
            messageElement.classList.add(name); // Add each class separately
        });
        console.log("function called");
        messageElement.innerHTML = `<span class="message-text">${message}</span>`;
        return messageElement;
    }

});

