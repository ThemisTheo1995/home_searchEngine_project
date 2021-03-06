/*
* Filters module
*/
function resetFilter(){
	d = document.querySelectorAll('.form_group');
    for (var i = 0, len = d.length; i < len; i++) {
        d[i].value = '';
    }
	document.getElementById("search_bar").submit(); 
}

function sortFilter(){
	document.getElementById("search_bar").submit(); 
}

function featuresFilter(featList, feature){
	const features = document.getElementById(featList);
	if(features.value.includes(feature)){
		var featuresArray = features.value.split(',').map();

	}else{
		features.value += feature+',';
	}
}

function showHideFeatures(){
	const feat_container = document.getElementById('features-container');
	const feat_arrow_down = document.getElementById('features-arrow-down');
	const feat_arrow_up = document.getElementById('features-arrow-up');
	if (feat_container.classList.contains('hidden')){
		feat_container.classList.remove('hidden');
		feat_arrow_up.classList.remove('hidden');
		feat_arrow_down.classList.add('hidden');
	}else{
		feat_container.classList.add('hidden');
		feat_arrow_down.classList.remove('hidden');
		feat_arrow_up.classList.add('hidden');
	}
}

function searchBarClose(){
	const searchBar = document.getElementById('search_bar');
	const map = document.getElementById('rentMap');

	if (searchBar.classList.contains('hidden')){
		searchBar.classList.remove('hidden');
	}else{
		searchBar.classList.add('hidden');
	}
}

function showMap(mapFilter){
	var mapInput = document.getElementById(mapFilter);
	if (mapInput.value == '1'){
		mapInput.value = 'off';
	}else{
		mapInput.value='1';
	}
}

// Hide property function
function hideProperty(pk){
  const propertyContainer = document.getElementById('property_container'+pk);
  propertyContainer.setAttribute("class", "hidden");
}

// Social Media
function twitterSharer(){ 
    window.open("https://twitter.com/share?text={{user.username}}&url=http://127.0.0.1:8000{{request.get_full_path|urlencode}}"); 
  } 
function fbSharer(){ 
    window.open("https://www.facebook.com/sharer/sharer.php?u=http://127.0.0.1:8000{{request.get_full_path|urlencode}}"); 
  } 

// Save function
function saveProperty(pk){
    const detailsSave = document.getElementById('detailsSave'+pk);
    if (detailsSave.getAttribute("fill") == 'LightCoral'){
        detailsSave.setAttribute("fill", "Crimson");
    }
    else{
        detailsSave.setAttribute("fill", "LightCoral");
    }
}