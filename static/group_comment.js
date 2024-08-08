$(document).ready(function () {
    $(document).on('submit', '#group', function (e) {
        e.preventDefault()
        $.ajax({
            type: 'POST',
            url: '/group_chat_comment',
            data: {
                sender: $('#sender').val(),
                comment: $('#comment').val(),
                profile_image: $('#profile_image').val(),
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
        document.getElementById('comment').value = ''
    })
})