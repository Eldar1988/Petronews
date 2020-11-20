function ChangeName() {
    let csrf_token = $('.change-name-form [name="csrfmiddlewaretoken"]').val();
    let post_url = $(".change-name-form").attr("action");
    let first_name = $("#first-name").val();
    let last_name = $("#last_name").val();
    let professional = $("#professional").val();
    let company = $("#company").val();
    let bio = $("#bio").val();

    if (first_name.length < 1) {
        $("#first_name").addClass('is-invalid')
        return
    }
    if (last_name.length < 1) {
        $("#last_name").addClass('is-invalid')
        return
    }

    let data = {};
    data["csrfmiddlewaretoken"] = csrf_token;
    data.first_name = first_name;
    data.last_name = last_name;
    data.professional = professional;
    data.company = company;
    data.bio = bio;
    $.ajax({
        url: post_url,
        type: "POST",
        data: data,
        success: () => {
            // alert('Ваши личные данные успешно изменены.')
            $('#successModal').modal('show')

            $.ajax({
                type: "GET",
                success: (data) => {
                    $('.profile-info').empty();
                    $('.profile-info').append(
                        $(data).find('.profile-info').html()
                    );
                }
            })
        },
    });
}

function defaultBio(bio) {
    console.log(bio)
    if (bio != 'None') {
        $('#bio').val(`${bio}`);
    }
}

function newPub() {
    $('.publications-profile-list').css('display', 'none');
    $('.profile-new-pub').fadeIn();
}

function backFromNewPub() {
    $('.profile-new-pub').css('display', 'none');
    $('.publications-profile-list').fadeIn();
}

function delPublication(id) {
    let get_url = `/user/delete_publications/${id}`;
    let reload_url = $('#del-pub').attr('data-target')
    let confirmDelete = confirm("Подтвердите удаление публикации");

    if (confirmDelete) {
        $.ajax({
            type: "GET",
            url: get_url,
            success: () => {
                $("#profile-publications").load(`${reload_url} #profile-publications >*`);
            }
        })
    }
}


function delQuestion(id) {
    let get_url = `/user/delete_question/${id}`;
    let reload_url = $('#del-question').attr('data-target')
    let confirmDelete = confirm("Подтвердите удаление вопроса");

    if (confirmDelete) {
        $.ajax({
            type: "GET",
            url: get_url,
            success: () => {
                $("#profile-questions").load(`${reload_url} #profile-questions >*`);
            }
        })
    }
}


function publicInTg(id, tgUrl) {
    let csrf_token = $('.tg-form [name="csrfmiddlewaretoken"]').val();
    let post_url = $(".tg-form").attr("action");

    let data = {};
    data["csrfmiddlewaretoken"] = csrf_token;
    data.id = id;
    data.tg_url = tgUrl;

    console.log(id, tgUrl);

    $.ajax({
        url: post_url,
        type: "POST",
        data: data,
        success: () => {
              alert('Опубликовано в Telegram')
            $.ajax({
                type: "GET",
                success: (data) => {
                    $('.post-tg-cards').empty();
                    $('.post-tg-cards').append(
                        $(data).find('.post-tg-cards').html()
                    );
                }
            })
        }
    });
}
