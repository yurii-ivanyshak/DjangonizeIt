(function($) {
        $(function() {
		
$(document).ready(function(){

    // Slide effect
    var _parentSlide = 'div.slide-block';
    var _linkSlide = 'a.open-close';
    var _slideBlock = 'div.block';
    var _openClassS = 'slide-active';
    var _durationSlide = 500;
    
    $(_parentSlide).each(function(){
		if (!$(this).is('.'+_openClassS)) {
			$(this).find(_slideBlock).css('display','none');
		}
    });
    $(_linkSlide,_parentSlide).click(function(){
		if ($(this).parents(_parentSlide).is('.'+_openClassS)) {
			$(this).parents(_parentSlide).removeClass(_openClassS);
			$(this).parents(_parentSlide).find(_slideBlock).slideUp(_durationSlide);
		} else {
			$(this).parents(_parentSlide).addClass(_openClassS);
			$(this).parents(_parentSlide).find(_slideBlock).slideDown(_durationSlide);
		}
		return false;
    });
    
});

		
          });
    })(jQuery);     
