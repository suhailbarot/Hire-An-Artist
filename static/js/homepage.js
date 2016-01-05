$(document).ready(function() {

      $("#cityinput").autocomplete({
          source : cityList,
          minLength: 2,
          open: function () {
        autoComplete.zIndex(dlg.zIndex()+1);
    },
          select: function(e,ui){
              window.location = "/set_city?city=" + ui.item.label.toLowerCase() + "&next={{ request.path }}"
          }
      });

    $('.carousel').carousel({interval: 4321});

    $('#toggle').click(function(){
    	if($('#nameform').css('display')=='none'){
            $('#toggle').text('');
$('#categoryform').fadeToggle(200,function() {
    $('#nameform').fadeToggle(200, function(){
         $('#toggle').text('Search By Category?');
    });
})};
   if($('#categoryform').css('display')=='none'){
       $('#toggle').text('');
$('#nameform').fadeToggle(200, function(){
    $('#categoryform').fadeToggle(200,function(){
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

});