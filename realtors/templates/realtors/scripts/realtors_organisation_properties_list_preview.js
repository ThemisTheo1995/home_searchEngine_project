function previewMode (pk, property_type){
    if (pk != ''){
        // GET AJAX request
        $.ajax({
            type: 'GET',
            url: "{% url 'organisation:ajax_realtors_org_rent_preview' %}",
            async: true,
            data: {"pk": pk},
            success: function (rent) {
                // Populate the fields if response is valid
                if(rent){
                    $('.previewPk').attr("href", "/properties/property/"+rent.pk);
                    $('.photo_main').attr("src", rent.photo_main);
                    $('.property_type').html(property_type);
                    $('.bedrooms').html(rent.bedrooms);
                    $('.bathrooms').html(rent.bathrooms);
                    $('.m2').html(rent.m2);
                    $('.short_description').html(rent.short_description);
                    $('.admin_1').html(rent.admin_1);
                    $('.address').html(rent.address);
                    $('.street_number').html(rent.street_number);
                    $('.currency').html("["+rent.currency+"]");
                    $('.admin_2').html(rent.admin_2);
                    $('.admin_3').html(rent.admin_3);
                    $('.country').html(rent.country);
                    $('.postalcode').html(rent.postalcode);
                    $('.price').html(rent.price);
                    $('.list_date').html(rent.list_date);
                }
                if ($('.rent_preview').is(":visible") && $('.preview_pk').val()==pk){
                    $('.rent_preview').addClass('hidden');
                }else{
                    $('.rent_preview').removeClass('hidden');
                }
                $('.preview_pk').attr('value', pk);
            },
            error: function (rent) {
                // Else log the issue
                console.log(rent)
            }
        });
    }
}