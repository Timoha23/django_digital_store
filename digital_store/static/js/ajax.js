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

    // ДОБАВЛЕНИЕ В ИЗБРАННОЕ
    $('.favorite-form').submit(function(e){
        e.preventDefault()
        const product_id = $(this).attr('id')
        const url = $(this).attr('action')
        const button = $(`.favorite-btn${ product_id }`)
        const heart = $(`.i${ product_id }`)
        
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'product_id': product_id,
            },
            success: function(response) {
                if(button.attr('id') === '1') {
                    button.removeClass('btn-danger').addClass('btn-outline-danger')
                    heart.removeClass('fa-solid').addClass('fa-regular')
                    console.log(heart)
                    // button.attr('id') = '2'
                } else {
                    console.log('2')
                    button.removeClass('btn-outline-danger').addClass('btn-danger')
                    heart.removeClass('fa-regular').addClass('fa-solid')
                    // button.attr('id') = '1'
                }
            },
            error: function(response) {
                console.log('error', response)
            }
        })
    });
}); 

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