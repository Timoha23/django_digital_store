$(document).ready(function() {
    // ПЛЮС МИНУС В КОРЗИНЕ
    $('.add-count-form').submit(function(e){
        e.preventDefault()
        const obj_id = $(this).attr('id')
        const url = $(this).attr('action')
        const count_items = $(`.count-items${ obj_id }`).text()
        console.log(count_items)

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'object_id': obj_id,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'full_cart_price': $(`.full-cart-price`).first().text(),
            },
            success: function(response) {
                if(response.maximum_count) {
                    $(`.add-count-btn${ obj_id }`).attr("disabled", true)
                } else {
                    $(`.add-count-btn${ obj_id }`).attr("disabled", false)
                }
                $(`.remove-count-btn${ obj_id }`).attr("disabled", false)
                $(`.count-items${ obj_id }`).text(response.count_items)
                $(`.full-price${ obj_id }`).text(response.full_price)
                $(`.full-cart-price`).text(response.full_cart_price)    
            },
            error: function(response) {
                console.log('error')
            }
        });
    });

    $('.remove-count-form').submit(function(e){
        e.preventDefault()
        const obj_id = $(this).attr('id')
        const url = $(this).attr('action')
        const count_items = $(`.count-items${ obj_id }`).text()
        console.log(count_items)

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'object_id': obj_id,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'full_cart_price': $(".full-cart-price").first().text(),
            },
            success: function(response) {
                if(response.minimum_count) {
                    $(`.remove-count-btn${ obj_id }`).attr("disabled", true)
                } else {
                    $(`.remove-count-btn${ obj_id }`).attr("disabled", false)
                }
                $(`.add-count-btn${ obj_id }`).attr("disabled", false)
                $(`.count-items${ obj_id }`).text(response.count_items)
                $(`.full-price${ obj_id }`).text(response.full_price)
                $(`.full-cart-price`).text(response.full_cart_price)
            },
            error: function(response) {
                console.log('error')
            }
        });
    });

    addRemoveFavorite()

    addToCart()
}); 


function addRemoveFavorite() {
    $('.favorite-form').each((index, el) => {
        $(el).on('submit', (e) => {
            e.preventDefault();
            const product_id = $(el).attr('id')
            const url = $(el).attr('action')

            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    'product_id': product_id,
                },

                success: function(response) {
                    if (response.is_favorite) {
                        $(el).find('.favorite-btn-wrap').empty()
                        $(el).find('.favorite-btn-wrap').html(`
                            <button style="position: relative" type="submit" class="btn btn-danger btn-sm me-1 mb-2" data-mdb-toggle="tooltip" title="В избранном">
                                <i class="fa-solid fa-heart"></i>
                            </button>
                        `)
                    } else {
                        $(el).find('.favorite-btn-wrap').empty()
                        $(el).find('.favorite-btn-wrap').html(`
                            <button style="position: relative" type="submit" class="btn btn-outline-danger btn-sm me-1 mb-2" data-mdb-toggle="tooltip" title="В избранное">
                                <i class="fa-regular fa-heart"></i>
                            </button>
                        `)
                    }
                },
                error: function(response) {
                    console.log('error')
                }
            })
        });
    });
}

function addToCart() {
    $('.add-to-cart-form').each((index, el) => {
        $(el).on('submit', (e) => {
            e.preventDefault();
            const product_id = $(el).attr('id')
            const url = $(el).attr('action')

            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    'product_id': product_id,
                },
                success: function(response) {
                    $(el).find('.btn').removeClass('btn-outline-success').addClass('btn-success')
                    swal({
                        title: 'Успешно!',
                        text: `Вы добавили ${response.product_name} в корзину`,
                        icon: 'success',
                        confirmButtonText: 'Закрыть'
                      });
                },
                error: function(response) {
                    swal({
                        title: 'Ошибка!',
                        text: 'В магазине недостаточно товаров. Вы добавили максимум',
                        icon: 'error',
                        confirmButtonText: 'Закрыть'
                      });
                }
            })
        });
    });
}

// $(document).ready(function(){
//     $("#change_count_minus").click(function(){
//         var data = {
//             count_items: $("#count_items").text(),
//             object_id: $("#count_items").attr('object_id'),
//             action: 'minus',
//             csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken").val(),
//         }
//         $.ajax({
//             url: "change_count_items/",
//             type: 'POST',
//             data: data,
//             success: function(response) {
//                 console.log(data)
//                 $("#count_items").text(response.count_items)
//                 $("#full_price").text(response.full_price)
//             },
//             error: function(response) {
//                 console.log('error')
//             }
//         });
//     });

// });

// $(document).ready(function(){
//     $("#change_count_plus").click(function(){

//         console.log(sss)
//         var data = {
//             count_items: $("#count_items").text(),
//             object_id: $("#count_items").attr('object_id'),
//             action: 'plus',

//             full_cart_price: $("#full-cart-price").text(),
//             csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken").val(),
//         }
//         $.ajax({
//             url: "change_count_items/",
//             type: 'POST',
//             data: data,
//             success: function(response) {
//                 console.log(data)
//                 $("#count_items").text(response.count_items)
//                 $("#full_price").text(response.full_price)
//                 $("#full-cart-price").text(response.full_cart_price)
//             },
//             error: function(response) {
//                 console.log('error')
//             }
//         });
//     });

// });