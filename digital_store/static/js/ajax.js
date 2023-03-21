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
    delFromCart()
    acceptRejectProduct()
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
                    if (response.responseJSON.error == 'max_cart_size') {
                        swal({
                            title: 'Ошибка!',
                            text: `Максимальное число товара в корзине ${response.responseJSON.max_cart_size}. Оформите заказ, либо удалите лишние товары из корзины`,
                            icon: 'error',
                            button: 'Закрыть'
                          });
                    } else {
                        swal({
                            title: 'Ошибка!',
                            text: 'В магазине недостаточно товаров. Вы добавили максимум',
                            icon: 'error',
                            button: 'Закрыть'
                          });
                    }
                }
            })
        });
    });
}

function delFromCart() {
    $('.del-from-cart-form').each((index, el) => {
        $(el).on('submit', (e) => {
            e.preventDefault();
            const product_id = $(el).attr('id')
            const url = $(el).attr('action')
            const full_cart_price = $(".full-cart-price").first().text()
            const cart_count_items = $('.cart-size')

            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    'product_id': product_id,
                    'full_cart_price': full_cart_price,
                },
                success: function(response){
                    console.log('success')
                    $(`#card-${product_id}`).remove()
                    $('.cart-size').text(parseInt(cart_count_items.text())-1)
                    $(`.full-cart-price`).text(response.full_cart_price)
                    swal({
                        title: 'Успешно!',
                        text: `Вы удалили ${response.product_name} из корзины`,
                        icon: 'success',
                        confirmButtonText: 'Закрыть'
                      });
                },
                error: function(response){
                    console.log('error')
                }
            })
        });
    });
}


// function acceptRejectProduct() {
//     $('.change-product-status-form').each((index, el) => {
//         $(el).on('submit', (e) => {
//             e.preventDefault();
//             const product_id = $(el).attr('id')
//             const url = $(el).attr('action')

//             $.ajax({
//                 type: 'POST',
//                 url: url,
//                 data: {
//                     'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
//                     'product_id': product_id,
//                 },
//                 success: function(response){
//                     console.log(response.product_status)
//                     if (response.product_status === 'Accept') {
//                         $(el).find('.btn').removeClass('btn-outline-success').addClass('btn-outline-danger')
//                         $(el).find('.btn').text('Отклонить')
//                         $(`.get-status-display-${product_id}`).text('Одобрено')
//                     } else {
//                         $(el).find('.btn').removeClass('btn-outline-danger').addClass('btn-outline-success')
//                         $(el).find('.btn').text('Одобрить')
//                         $(`.get-status-display-${product_id}`).text('Отклонено')
//                     }
//                 },
//                 error: function(response){
//                     console.log('error')
//                 }
//             })
//         });
//     });
// }

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