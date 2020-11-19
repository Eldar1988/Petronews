function ChangeName() {
    let csrf_token = $('.change-name-form [name="csrfmiddlewaretoken"]').val();
    let post_url = $(".change-name-form").attr("action");
    let first_name = $("#first-name").val();
    let last_name = $("#last_name").val();
    let professional = $("#professional").val();
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
    $('#bio').val(`${bio}`)
}

function newPub() {
    $('.publications-profile-list').css('display', 'none')
    $('.profile-new-pub').fadeIn()
}

function backFromNewPub() {
    $('.profile-new-pub').css('display', 'none')
    $('.publications-profile-list').fadeIn()
}