let url = $('#course_url').val();

$('document').ready(function () {
        console.log(sessionStorage.getItem('usd'))
        if (sessionStorage.getItem('usd') === null) {
            $.ajax(
                {
                    url: 'https://free.currconv.com/api/v7/convert?q=USD_KZT,EUR_KZT&compact=ultra&apiKey=1b6d8d3daf7ed8ff160d',
                    type: 'get',
                    dataType: 'jsonp',

                    success: function (data) {
                        sessionStorage.setItem('usd', data.USD_KZT);
                        sessionStorage.setItem('eur', data.EUR_KZT);
                        let new_course = {};
                        new_course.usd = sessionStorage.getItem('usd')
                        new_course.eur = sessionStorage.getItem('eur')
                        $.ajax(
                            {
                                url: 'https://free.currconv.com/api/v7/convert?q=RUB_KZT&compact=ultra&apiKey=1b6d8d3daf7ed8ff160d',
                                type: 'get',
                                dataType: 'jsonp',
                                success: function (data) {
                                    sessionStorage.setItem('rub', data.RUB_KZT);
                                    new_course.rub = sessionStorage.getItem('rub')
                                    $.ajax({
                                        url: `info/set_course/usd${new_course.usd}/eur${new_course.eur}/rub${new_course.rub}`,
                                        success: function () {
                                            $('#usd_kzt').val(sessionStorage.getItem('usd'));
                                            $('#eur-kzt').val(sessionStorage.getItem('eur'));
                                            $('#rub-kzt').val(sessionStorage.getItem('rub'));
                                        }
                                    })
                                }
                            }
                        )
                    }
                }
            )
        }

    }
)
