document.addEventListener("DOMContentLoaded", function() {
    // Initiate the map
  var markerSet = JSON.parse(document.getElementById('markerSet').textContent);
  if (markerSet != 'off'){
    /*
    * Leaflet.Sleep
    */

    /*
    * Default Button (touch devices only)
    */

  L.Control.SleepMapControl = L.Control.extend({

    initialize: function(opts){
      L.setOptions(this,opts);
    },
  
    options: {
      position: 'topright',
      prompt: 'disable map',
      styles: {
        'backgroundColor': 'white',
        'padding': '5px',
        'border': '2px solid gray'
      }
    },
  
    buildContainer: function(){
      var self = this;
      var container = L.DomUtil.create('p', 'sleep-button');
      var boundEvent = this._nonBoundEvent.bind(this);
      container.innerHTML = this.options.prompt;
      L.DomEvent.addListener(container, 'click', boundEvent);
      L.DomEvent.addListener(container, 'touchstart', boundEvent);
  
      Object.keys(this.options.styles).map(function(key) {
        container.style[key] = self.options.styles[key];
      });
  
      return (this._container = container);
    },
  
    onAdd: function () {
      return this._container || this.buildContainer();
    },
  
    _nonBoundEvent: function(e) {
      L.DomEvent.stop(e);
      if (this._map) this._map.sleep._sleepMap();
      return false;
    }
  
  });
  
  L.Control.sleepMapControl = function(){
    return new L.Control.SleepMapControl();
  };
  
  
  /*
   * The Sleep Handler
   */
  
  L.Map.mergeOptions({
    sleep: true,
    sleepTime: 750,
    wakeTime: 750,
    wakeMessageTouch: 'Touch to Wake',
    sleepNote: false,
    hoverToWake: true,
    sleepOpacity:1,
    sleepButton: L.Control.sleepMapControl
  });
  
  L.Map.Sleep = L.Handler.extend({
  
    addHooks: function () {
      var self = this;
      this.sleepNote = L.DomUtil.create('p', 'sleep-note', this._map._container);
      this._enterTimeout = null;
      this._exitTimeout = null;
  
      /*
       * If the device has only a touchscreen we will never get
       * a mouseout event, so we add an extra button to put the map
       * back to sleep manually.
       *
       * a custom control/button can be provided by the user
       * with the map's `sleepButton` option
       */
      this._sleepButton = this._map.options.sleepButton();
  
      if (this._map.tap) {
        this._map.addControl(this._sleepButton);
      }
  
      var mapStyle = this._map._container.style;
      mapStyle.WebkitTransition += 'opacity .5s';
      mapStyle.MozTransition += 'opacity .5s';
  
      this._setSleepNoteStyle();
      this._sleepMap();
    },
  
    removeHooks: function () {
      if (!this._map.scrollWheelZoom.enabled()){
        this._map.scrollWheelZoom.enable();
      }
      if (this._map.tap) {
        this._map.touchZoom.enable();
        this._map.dragging.enable();
        this._map.tap.enable();
      }
      L.DomUtil.setOpacity( this._map._container, 1);
      L.DomUtil.setOpacity( this.sleepNote, 0);
      this._removeSleepingListeners();
      this._removeAwakeListeners();
    },
  
    _setSleepNoteStyle: function() {
      var noteString = '';
      var style = this.sleepNote.style;
  
      if(this._map.tap) {
        noteString = this._map.options.wakeMessageTouch;
      } else if (this._map.options.wakeMessage) {
        noteString = this._map.options.wakeMessage;
      } else if (this._map.options.hoverToWake) {
        noteString = 'click or hover to wake';
      } else {
        noteString = 'click to wake';
      }
  
      if( this._map.options.sleepNote ){
        this.sleepNote.innerHTML = noteString;
        style.pointerEvents = 'none';
        style.maxWidth = '150px';
        style.transitionDuration = '.2s';
        style.zIndex = 5000;
        style.margin = 'auto';
        style.textAlign = 'center';
        style.borderRadius = '4px';
        style.top = '80%';
        style.position = 'relative';
        style.padding = '5px';
        style.border = 'solid 2px black';
        style.background = 'white';
  
        if(this._map.options.sleepNoteStyle) {
          var noteStyleOverrides = this._map.options.sleepNoteStyle;
          Object.keys(noteStyleOverrides).map(function(key) {
            style[key] = noteStyleOverrides[key];
          });
        }
      }
    },
  
    _wakeMap: function (e) {
      this._stopWaiting();
      this._map.scrollWheelZoom.enable();
      if (this._map.tap) {
        this._map.touchZoom.enable();
        this._map.dragging.enable();
        this._map.addControl(this._sleepButton);
      }
      L.DomUtil.setOpacity( this._map._container, 1);
      this.sleepNote.style.opacity = 0;
      this._addAwakeListeners();
    },
  
    _sleepMap: function () {
      this._stopWaiting();
      this._map.scrollWheelZoom.disable();
  
      if (this._map.tap) {
        this._map.touchZoom.disable();
        this._map.dragging.disable();
        this._map.tap.disable();
        this._map.removeControl(this._sleepButton);
      }
  
      L.DomUtil.setOpacity( this._map._container, this._map.options.sleepOpacity);
      this.sleepNote.style.opacity = this._map.options.sleepNoteStyle && this._map.options.sleepNoteStyle.opacity ? this._map.options.sleepNoteStyle.opacity : .6;
      this._addSleepingListeners();
    },
  
    _wakePending: function () {
      this._map.once('mousedown', this._wakeMap, this);
      if (this._map.options.hoverToWake){
        var self = this;
        this._map.once('mouseout', this._sleepMap, this);
        self._enterTimeout = setTimeout(function(){
            self._map.off('mouseout', self._sleepMap, self);
            self._wakeMap();
        } , self._map.options.wakeTime);
      }
    },
  
    _sleepPending: function () {
      var self = this;
      self._map.once('mouseover', self._wakeMap, self);
      self._exitTimeout = setTimeout(function(){
          self._map.off('mouseover', self._wakeMap, self);
          self._sleepMap();
      } , self._map.options.sleepTime);
    },
  
    _addSleepingListeners: function(){
      this._map.once('mouseover', this._wakePending, this);
      this._map.tap &&
        this._map.once('click', this._wakeMap, this);
      
    },
  
    _addAwakeListeners: function(){
      this._map.once('mouseout', this._sleepPending, this);
    },
  
    _removeSleepingListeners: function(){
      this._map.options.hoverToWake &&
        this._map.off('mouseover', this._wakePending, this);
      this._map.off('mousedown', this._wakeMap, this);
      this._map.tap &&
        this._map.off('click', this._wakeMap, this);
    },
  
    _removeAwakeListeners: function(){
      this._map.off('mouseout', this._sleepPending, this);
    },
  
    _stopWaiting: function () {
      this._removeSleepingListeners();
      this._removeAwakeListeners();
      var self = this;
      if(this._enterTimeout) clearTimeout(self._enterTimeout);
      if(this._exitTimeout) clearTimeout(self._exitTimeout);
      this._enterTimeout = null;
      this._exitTimeout = null;
    }
  });
  
  L.Map.addInitHook('addHandler', 'sleep', L.Map.Sleep);

/*
window.addEventListener('scroll', function() {
    var map = document.getElementById('rentMap');
    if (this.scrollTop > 100){
      map.classList.remove("rentMapTop");
      map.classList.add("rentMapBottom");
    }else {
      map.classList.add("rentMapBottom");
      map.classList.remove("rentMapTop");
    }
});
*/

  // Smooth transition on anchor click.
  function markerClick(e){
      const markerPk = this._icon.dataset.pk;
      document.getElementById(markerPk).scrollIntoView({
          behavior: 'smooth'
      });
  }

    console.log(markerSet);
  // SetView
  var map = L.map('map').setView([markerSet[0][1], markerSet[0][2]], 13);
  // Map init
  var gl = L.mapboxGL({
      attribution: "\u003ca href=\"https://www.maptiler.com/copyright/\" target=\"_blank\"\u003e\u0026copy; MapTiler\u003c/a\u003e \u003ca href=\"https://www.openstreetmap.org/copyright\" target=\"_blank\"\u003e\u0026copy; OpenStreetMap contributors\u003c/a\u003e",
      style: 'https://api.maptiler.com/maps/77c1d067-7f6c-43c7-81ca-46de586f5de3/style.json?key=f8KNCaKJy3aq9zRp2tSn'
  }).addTo(map); 

  // Markers
  for (var i = 0; i < markerSet.length; i++) {
          // Map configuration
          var yenesesMarker = L.icon({
              iconUrl: '/static/images/rec.svg',
              iconSize: [30, 30],
              iconAnchor: [15,30]
          });
          marker = new L.marker([markerSet[i][1],markerSet[i][2]], {icon: yenesesMarker}).
          bindTooltip(markerSet[i][0]+" "+markerSet[i][6]+"<br><b>"+markerSet[i][4]+markerSet[i][5]+"</b>").
          on('click',markerClick).
          //bindPopup('<a href=http://127.0.0.1:8000/properties/property/'+markerSet[i][3]+'/><b>'+markerSet[i][0]+'</b></a>'+'<br>'+markerSet[i][4]+markerSet[i][5]).openPopup().
          addTo(map);
          marker._icon.setAttribute("data-pk",markerSet[i][3]);
      }
}   
});
// Click on map icon
function markerOnMap(key){
    const marker = document.querySelector('img[data-pk="'+key+'"]');
    if (marker.classList.contains("markerActive")){
      marker.classList.remove("markerActive");
    }else{
      marker.classList.add("markerActive");
      setTimeout(function(){
          marker.classList.remove('markerActive');
      },5000);
    }
}
