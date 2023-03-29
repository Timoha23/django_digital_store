$(document).ready(function() {

    addCountItemsCart()
    removeCountItemsCart()
    addRemoveFavorite()
    addToCart()
    delFromCart()
    showBoughtItems()
    makeRemoveModeratorStatus()
}); 

function addCountItemsCart() {
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
}

function removeCountItemsCart() {
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
}

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

function showBoughtItems() {
    $('.show-items').each((index, el) => {
        $(el).on('click', (e) => {
            const obj_id = $(el).attr('id')
            if ($(`.items-${obj_id}`).attr('hidden')) {
                $(`.items-${obj_id}`).removeAttr('hidden')
            } else {
                $(`.items-${obj_id}`).attr('hidden', true)
            }
        });
    });
}

function makeRemoveModeratorStatus() {
    $('.make-remove-form').each((index, el) => {
        $(el).on('submit', (e) => {
            e.preventDefault();
            const user_id = $(el).attr('id')
            const url = $(el).attr('action')

            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    'user_id': user_id,
                },

                success: function(response) {
                    const btn = $(el).find('.btn')
                    if (response.is_moderator) {
                        btn.removeClass('btn-outline-success').addClass('btn-outline-danger')
                        btn.text('Убрать из модераторов')
                    } else {
                        btn.removeClass('btn-outline-danger').addClass('btn-outline-success')
                        btn.text('Сделать модератором')
                    }
                },
                error: function(response) {
                    console.log('bad')
                }
            })
        })
    });
}
