console.log('Hello')

function getData(url) {
    $.get(
        url,
    )
}

function addComment(name, id) {
    console.log(name, id)
    document.getElementById("parent").value = id;
    $("#comment").val(`${name}, `)
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


async function addQuestion() {
    console.log('r')
    let csrf_token = $('.add-question-form [name="csrfmiddlewaretoken"]').val();
    let post_url = $(".add-question-form").attr("action");
    let title = $('#q-title').val();
    let body = $('#q-body').val();

    if (title.length < 5) {
        $('#q-title').addClass('is-invalid')
        return
    }
    let data = {};
    data["csrfmiddlewaretoken"] = csrf_token;
    data.title = title;
    data.body = body;
    let reload_url = $('#del-question').attr('data-target')
    $.ajax({
        url: post_url,
        type: "POST",
        data: data,
        success: () => {
            $('.add-question-form').css('display', 'none');
            $('#q-button').css('display', 'none');
            $('#q-alert').fadeIn();

            $("#profile-questions").load(`${reload_url} #profile-questions >*`);

            $.ajax({
                type: "GET",
                success: (data) => {
                    $('.content').empty();
                    $('.content').append(
                        $(data).find('.content').html()
                    );
                }
            })
        },
    });
}

function AjaxAddAnswer() {
    let csrf_token = $('.answer-form [name="csrfmiddlewaretoken"]').val();
    let post_url = $(".answer-form").attr("action");
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
        success: (response) => {
            if (response === 'double') {
                $('#d-notice').fadeIn();
            }
            if (response === 'success') {
                $('#d-notice').css('display', 'none');
                $('#notice').fadeIn();
                $('#comment').val('')
            }
            $.ajax({
                type: "GET",
                success: (data) => {
                    $('.answers-cards').empty();
                    $('.answers-cards').append(
                        $(data).find('.answers-cards').html()
                    );
                }
            })
        },
    });
}


// const anchors = document.querySelectorAll('a[href*="#"]')
const anchors = document.querySelectorAll('.scroll-to')

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

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})