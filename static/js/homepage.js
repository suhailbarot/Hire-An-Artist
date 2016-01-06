$(document).ready(function() {

    $('.carousel').carousel({interval: 4321});

    $('#toggle').click(function(){
    	if($('#nameform').css('display')=='none'){
            $('#toggle').text('');
$('#categoryform').fadeToggle(100,function() {
    $('#nameform').fadeToggle(100, function(){
         $('#toggle').text('Search By Category?');
    });
})};
   if($('#categoryform').css('display')=='none'){
       $('#toggle').text('');
$('#nameform').fadeToggle(100, function(){
    $('#categoryform').fadeToggle(100,function(){
        $('#toggle').text('Search By Name?');
    });
})};
    });

  var slider = document.getElementById('slider');
  noUiSlider.create(slider, {
	start: [10000, 100000],
	connect: true,
	range: {
		'min': 2000,
		'max': 200000
	},
	step: 1000
});
            $('#id_budget_min').val(slider.noUiSlider.get()[0]);
            $('#id_budget_max').val(slider.noUiSlider.get()[1]);
            $('#budgetmin').text("Rs. " + Math.ceil($('#id_budget_min').val()));
            $('#budgetmax').text("Rs. " + Math.ceil($('#id_budget_max').val()));
slider.noUiSlider.on('slide', function(){
$('#id_budget_min').val(slider.noUiSlider.get()[0]);
            $('#id_budget_max').val(slider.noUiSlider.get()[1]);
            $('#budgetmin').text("Rs. " + Math.ceil($('#id_budget_min').val()));
            $('#budgetmax').text("Rs. " + Math.ceil($('#id_budget_max').val()));

        });
slider.noUiSlider.on('change', function(){
$('#id_budget_min').val(slider.noUiSlider.get()[0]);
            $('#id_budget_max').val(slider.noUiSlider.get()[1]);
            $('#dropdownMenu1').text("Rs. " + Math.ceil($('#id_budget_min').val()) +" -  " + Math.ceil($('#id_budget_max').val()));

        });
$('#dropdownMenu1').text("Budget");


    $("#nameform input").autocomplete({
          source : function(request, response){
              $.ajax({
                  url: '/api/listing_name',
                  data: {
                      term: request.term
                  },
                  success: function(data) {
                      data = JSON.parse(data);
                      if(data.length == 0)
                      {
                          data.push({
                              slug:"0",
                              label:"No listings found."
                          });
                      }
                      response(data);
                  }
              });
          },
          minLength: 2,
          select: function(e,ui){
              if(ui.item.slug == '0') {
                  e.preventDefault();
              }
              else {
                  window.location = ui.item.slug;
              }
              return false;
          }
      });

    $("#cityinput").autocomplete({
          source : function(request,response) {
              var results = $.ui.autocomplete.filter(cityList, request.term);
              if (!results.length) {
                results = ['Sorry, we are not present in your city'];
            }
            response(results);
          },
          minLength: 2,
          select: function(e,ui){
              if(ui.item.label == 'Sorry, we are not present in your city') {
                  e.preventDefault();
              }
              else {
                  window.location = "/set_city?city=" + ui.item.label.toLowerCase();
              }

          }
      });

});