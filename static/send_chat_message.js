$(document).ready(function () {
    $(document).on('submit', '#send', function (e) {
        e.preventDefault()
        $.ajax({
            type: 'POST',
            url: '/send_message',
            data: {
                sender: $('#sender').val(),
                receiver: $('#receiver').val(),
                message: $('#message').val(),
                receiverId: $('#receiverId').val(),
                senderId: $('#senderId').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (response) {
                // document.getElementById('display-comment').innerHTML = response
                //alert(response)

            },
            error: function (response) {
                //alert('an error occured')
            }
        })
        document.getElementById('message').value = ''
    })
})


$(document).ready(function () {
    setInterval(function () {

        $.ajax({
            type: 'GET',
            url: '/get_chat_message/' + $('#receiver').val(),
            success: function (response) {

                $('#display-comment').empty()
                for (var key in response.messages) {
                    if (response.messages[key].sender != $('#sender').val()) {
                        var temp = "<div class='border-t pt-4' style='margin-right:auto;width:fit-content;'><div class='flex'><div class='h-10 rounded-full relative flex-shrink-0'>"
                            + "</div><div class='text-gray-700 py-2 px-3 rounded-md bg-gray-100 h-full relative lg:ml-5 ml-2 lg:mr-20'>" +
                            "<p class='leading-6'></p>" + response.messages[key].message + "</ul></div></div ></div > "
                        $('#display-comment').append(temp)

                    } else {
                        var temp = "<div class='border-t pt-4' style='margin-left:auto;width:fit-content;'><div class='flex'><div class='w-10 h-10 rounded-full relative'></div><div style='background-color: pink;' class='text-gray-700 py-2 px-3 rounded-md bg-gray-100 h-full relative lg:ml-5 ml-2 lg:mr-20'>" +
                            " <p class='leading-6'></p>" + response.messages[key].message + "</ul></div></div ></div > "
                        $('#display-comment').append(temp)

                    }

                }
                function scrollToBottom() {
                    window.scrollTo(0, document.body.scrollHeight)

                }
                if (!document.body.classList.contains("active")) {
                    scrollToBottom();
                }
                document.body.onmouseenter = () => {
                    document.body.classList.add("active");
                }
                function endScroll() {
                    document.body.classList.add("active");
                }
                document.body.onscroll = () => {
                    document.body.classList.add("active");
                }
                document.body.onmouseleave = () => {
                    document.body.classList.remove("active");
                }

            },
            error: function (response) {
                //alert('an error occured')
            }
        });
    }, 100)
})

//     < textarea name = "message" style = "border-radius: 7%;" placeholder = "Type a message" autofocus required id = "message"
// oninput = "endScroll()" cols = "150" ></textarea >
//     <button type="submit">
//         <span style="color: white; font-size:large; padding-top:7px" class="fa fa-send" title="Chats"></span>
//     </button>