function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
    document.getElementById("myDropdown1").classList.toggle("show");
}

$(document).ready(function () {
    $(document).on('submit', '#send', function (e) {
        e.preventDefault()
        var formData = new FormData();
        formData.append('sender', $('#sender').val());
        formData.append('receiver', $('#receiver').val());
        formData.append('profile_image', $('#profile_image').val());
        formData.append('message', $('#message').val());
        formData.append('receiverId', $('#receiverId').val());
        formData.append('senderId', $('#senderId').val());

        // Append the file (make sure the input allows file uploads)
        if ($('#image')[0].files[0]) {
            formData.append('image', $('#image')[0].files[0]);
        }
        // Append the file (make sure the input allows file uploads)
        if ($('#video')[0].files[0]) {
            formData.append('video', $('#video')[0].files[0]);
        }

        // Add CSRF token (important!)
        formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
        $.ajax({
            type: 'POST',
            url: '/send_message',
            processData: false, // Important for file uploads
            contentType: false, // Important for file uploads
            data: formData,

            success: function (data) {
                //alert(data);
            },
            error: function (response) {
                //alert('An error occurred');
            }
        });
        document.getElementById('message').value = ''
        // Empty the file input field for image and video
        $('#image').val(''); // Clears the image file input
        $('#video').val(''); // Clears the video file input
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
                    // Check if the image exists and is not null or empty
                    var IfImage = response.messages[key].image;
                    var imageHTML = (IfImage && IfImage.includes('.')) ? "<img src='" + IfImage + "' />" : "";

                    var IfVideo = response.messages[key].video;
                    var videoExtensions = ['.mp4', '.webm', '.ogg']; // Valid video extensions
                    var videoHTML = (IfVideo && videoExtensions.some(ext => IfVideo.includes(ext)))
                        ? "<video controls><source src='" + IfVideo + "' type='video/mp4'></video>"
                        : "";

                    if (response.messages[key].sender != $('#sender').val()) {
                        var temp = "<div class='border-t pt-4' style='margin-right:auto;width:fit-content;'><div class='flex'><div class='h-10 rounded-full relative flex-shrink-0'>"
                            + "</div><div class='text-gray-700 py-2 px-3 rounded-md bg-gray-100 h-full relative lg:ml-5 ml-2 lg:mr-20'>" +
                            "<p class='leading-6'></p>" + response.messages[key].message + "</ul></div></div ></div > " + imageHTML + videoHTML;
                        $('#display-comment').append(temp)

                    } else {
                        var temp = "<div class='border-t pt-4' style='margin-left:auto;width:fit-content;'><div class='flex'><div class='w-10 h-10 rounded-full relative'></div><div style='background-color: pink;' class='text-gray-700 py-2 px-3 rounded-md bg-gray-100 h-full relative lg:ml-5 ml-2 lg:mr-20'>" +
                            " <p class='leading-6'></p>" + response.messages[key].message + "</ul></div></div ></div > " + imageHTML + videoHTML;
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