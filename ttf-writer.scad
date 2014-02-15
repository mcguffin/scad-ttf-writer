

/*
_ascii = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~";
_ansi = "€ ‚ƒ„…†‡ˆ‰Š‹Œ Ž  ‘’“”•–—˜™š›œ žŸ ¡¢£¤¥¦§¨©«¬ ®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ";

*/
// to do: define fallback character

points_per_mm = 2.83464567;



module write(text, font , center=false , spacing = 0 , fallback_char = "?" ) {
	
	move = [0,0,0];//center ? [-textwidth( text, font, fallback_char = fallback_char ) * size[0]/2 , -font_height*size[1]/2 , -size[2]/2 ] : [0,0,0];
	translate(move)
		for ( i = [0:len(text)-1] ) {
			translate([charpos( text , i , font , pos = 0, spacing = spacing , fallback_char = fallback_char ),0,0])
				draw_char(text[i],font,fallback_char)
					if ( $children > 0 ) {
						children();
					} else {
						cube(size);
					}
		}
}

module draw_char( char , font ,fallback_char = "?" ) {
	struct = charstruct(char , font , fallback_char );
	polygon( points=struct[2],paths=struct[3] );
}

module fontsize( size_in_points ) {
	// font is 1000 mm
	// = 1000 * points_per_mm
	fscale = size_in_points / (1000 * points_per_mm);
	scale( [ fscale , fscale , 1 ] )
		children();
}


function charstruct( char , font , fallback_char = "?" ) 
	= ( (font[ search( [char] , font )[0] ] == undef) ? charstruct(fallback_char,font) : font[ search( [char] , font )[0] ] );
	
function charwidth( char , font, fallback_char = "?" ) 
	= charstruct( char , font , fallback_char )[1];
	
function charpos( text , index , font , pos = 0 , spacing = 0 , fallback_char = "?" ) 
	= ( index==0 
		? pos 
		: charpos( text , index-1 , font , pos + charwidth( text[index-1] , font, fallback_char ) , spacing , fallback_char ) 
			+ spacing 
			+ kerning( charstruct( text[index] , font , fallback_char ) , text[index-1] , fallback_char ) 
	); 

function kerning( currcharstruct , prevchar , fallback_char = "?" )
	= (currcharstruct[4][ search( prevchar , currcharstruct[4] )[0] ] == undef) 
		? 0 
		: currcharstruct[4][ search( prevchar , currcharstruct[4] )[0] ][1];

// return pixel width of text
function textwidth( text , font , width = 0 , index = 0 , spacing = 0 , fallback_char = "?" ) 
	= ( index==len(text) 
		? width 
		: textwidth( text , font , width + charwidth( text[index] , font , fallback_char ) , index+1 , spacing , fallback_char ) );
