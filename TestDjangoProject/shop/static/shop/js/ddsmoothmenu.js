(function($) {
        $(function() {

$(document).ready(function () {	
	
	$('#nav li').hover(
		function () {
			//show its submenu
			$('.drop', this).slideDown(150);
		}, 
		function () {
			//hide its submenu
			$('.drop', this).slideUp(50);		
		}
	);
	$('#nav ul li').hover(
		function () {
			//show its submenu
			$('.drop2', this).slideDown(150);
		}, 
		function () {
			//hide its submenu
			$('.drop2', this).slideUp(50);		
		}
	);
	
});

		
          });
    })(jQuery);     

