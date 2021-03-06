document.addEventListener("DOMContentLoaded", function() {
  // Map configuration
  var lat = parseFloat("{{rent.geo_lat}}").toFixed(10);
  var lng = parseFloat("{{rent.geo_lng}}").toFixed(10);
  var yenesesMarker = L.icon({
      iconUrl: '/static/images/rec.svg',
      iconSize: [25, 25],
      iconAnchor: [12.5,25]

  });
    var map= L.map('map{{rent.id}}').setView([lat, lng], 13);
    L.marker([lat, lng], {icon: yenesesMarker}).addTo(map).openPopup();
    var gl = L.mapboxGL({
        attribution: "\u003ca href=\"https://www.maptiler.com/copyright/\" target=\"_blank\"\u003e\u0026copy; MapTiler\u003c/a\u003e \u003ca href=\"https://www.openstreetmap.org/copyright\" target=\"_blank\"\u003e\u0026copy; OpenStreetMap contributors\u003c/a\u003e",
        style: 'https://api.maptiler.com/maps/77c1d067-7f6c-43c7-81ca-46de586f5de3/style.json?key=f8KNCaKJy3aq9zRp2tSn'
    }).addTo(map); 
});
// Social
function twitterSharer(){ 
    window.open("https://twitter.com/share?text={{user.username}}&url=http://127.0.0.1:8000{{request.get_full_path|urlencode}}"); 
} 
function fbSharer(){ 
    window.open("https://www.facebook.com/sharer/sharer.php?u=http://127.0.0.1:8000{{request.get_full_path|urlencode}}"); 
} 
function saveProperty(){
    const detailsSave = document.getElementById('detailsSave');
    if (detailsSave.getAttribute("fill") == 'LightCoral'){
        detailsSave.setAttribute("fill", "Crimson");
    }
    else{
        detailsSave.setAttribute("fill", "LightCoral");
    }
}
