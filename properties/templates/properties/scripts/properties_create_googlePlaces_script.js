// Google auto complete
function activatePlacesSearch(){
	var input = document.getElementById('address_search');
	var autocomplete = new google.maps.places.Autocomplete(input);
}
function geoCreate (){
    const fullAdrress = document.getElementById("address_search").value;
    console.log(fullAdrress);
  // GET AJAX request
  $.ajax({
      type: 'GET',
      url: "{% url 'properties:ajax_properties_geoCreate' %}",
      async: true,
      data: {"address":fullAdrress},
      success: function (response) {
          // Populate the fields if response is valid
          if(response){
              document.getElementById("id_address").setAttribute('value', response.address);
              document.getElementById("id_street_number").setAttribute('value', response.street_number);
              document.getElementById("id_geo_lat").setAttribute('value', response.geo_lat);
              document.getElementById("id_geo_lng").setAttribute('value', response.geo_lng);
              document.getElementById("id_postalcode").setAttribute('value', response.postalcode);
          }
      },
      error: function (response) {
          // Else log the issue
      }
  });
}
