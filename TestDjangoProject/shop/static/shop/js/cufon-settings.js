function initCufon() {
	Cufon.replace('#nav a em', { textShadow: '#000 0 1px 0', fontFamily: 'aurulent' });
	Cufon.replace('.category-holder .block a', { fontFamily: 'aurulent', hover: true });
	Cufon.replace('#footer .copy-holder .design', { textShadow: '#000 1px 0 0', fontFamily: 'aurulent' });
	Cufon.replace('.promo-box .btn-take', { fontFamily: 'aurulent', hover: true });
	Cufon.replace('.comment-box .name', { fontFamily: 'harabara', hover: true });
	Cufon.replace('#main h2, .welcome-box .text-box h2, #steps-slider .slides h2', { fontFamily: 'harabara', hover: true });
	Cufon.replace('#sidebar h3, #sidebar h4, #sidebar .clients-list .name, .portfolio-box .title, .product-box h4', { fontFamily: 'harabara', hover: true });
	Cufon.replace('.related-list a', {fontFamily: 'harabara',hover: true});
	Cufon.replace('.related-list a span:not(.clean)');
	Cufon.replace('.person-list .name', { fontFamily: 'harabara', hover: true });
	Cufon.replace('.gallery h3', { fontFamily: 'harabara', hover: true });
	Cufon.replace('.threecolumns h3', { textShadow: '#000 1px 1px 2px', fontFamily: 'harabara' });
	Cufon.replace('.welcome-box .text-box .more, .welcome-box .text-box .portfolio', { textShadow: '#000 -1px 1px 0', fontFamily: 'aurulent' });
}

(function($) {
        $(function() {

$(document).ready(function(){
	initCufon();
});

		
          });
    })(jQuery);     
