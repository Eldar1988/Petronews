console.log('Hello')

function getData(url) {
    $.get(
        url,
    )
}

function addComment(name, id) {
    document.getElementById("parent").value = id;
    document.getElementById("comment").innerText = `${name}, `;
}

async function AjaxAddComment() {
    let csrf_token = $('.comment-form [name="csrfmiddlewaretoken"]').val();
    let post_url = $(".comment-form").attr("action");
    let name = $("#name").val()
    let email = $("#email").val()
    let text = $("#comment").val();
    let parent = $("#parent").val();
    if (name.length < 2) {
        $("#name").addClass('is-invalid')
        return
    }
    if (email.length < 5) {
        $("#email").addClass('is-invalid')
        return
    }
    if (text.length < 1) {
        $("#comment").addClass('is-invalid')
        return
    }
    $('#notice').fadeOut();
    let data = {};
    data["csrfmiddlewaretoken"] = csrf_token;
    data.name = name;
    data.email = email;
    data.text = text;
    data.parent = parent;
    $.ajax({
        url: post_url,
        type: "POST",
        data: data,
        success: () => {
            $('#notice').fadeIn();
            $('#comment').val('');
            $.ajax({
                type: "GET",
                success: (data) => {
                    $('#comments-list').empty();
                    $('#comments-list').append(
                        $(data).find('#comments-list').html()
                    );
                }
            })
        },
    });
}


const anchors = document.querySelectorAll('a[href*="#"]')

for (let anchor of anchors) {
    anchor.addEventListener('click', function (e) {
        e.preventDefault()

        const blockID = anchor.getAttribute('href').substr(1)

        document.getElementById(blockID).scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        })
    })
}