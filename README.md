
<p style="padding:10px 15px;color:#9c342e;background-color:#f7d9d7;border:1px solid #f2c4c2;">
<strong>Note:</strong> OpenSCAD 2015.03 introduced the text() function, so this project has become obsolete and is only kept for historical reasons.
</p>

##OpenSCAD Writer##

Write an (extrudable) 2D Text in [OpenSCAD](http://www.openscad.org/).
Supports spacing and kerning pairs.

Python script to convert ttf to Font Data included.

###Usage###
####Importing####
```
use </path/to/ttf-writer.scad>;
import </path/to/font_file.scad>;
```

####Syntax####
```
write( text, font , spacing = 0 , fallback_char = "?" );
```

```
linear_extrude( height = 10 )
	write( text, font , spacing = 0 , fallback_char = "?" );
```

The em square is considered 1000 OpenSCAD units (= mm) large, so in most cases you will 
need to scale down the extruded object to achieve a certain point size.

There is a method named `fontsize(size_in_points)` to ease that work. It will scale down 
along the X and Y coordinates leaving the Z axis alone.
Use it like this:

```
fontsize( size_in_points = 48 )
	linear_extrude( height = 10 )
		write( text, font , spacing = 0 , fallback_char = "?" );
```


#####write() Arguments#####
- `text`: String or Vector containing the characters as single elements. Use a vector if your text contains multibyte (utf-8) characters.
- `font`: The font vector. Should match the vector specified in yout font file.
- `spacing`: Letter Spacing in 1/1000 em
- `fallback_char`: Which character to write, if the actual char is not found in font definition

###Usage Examples###
####General usage####
```
// import writer
use <writer.scad>;
// import font
include <fonts/default_font.scad>;

write("Hello World",default_font);
// works

write("Hällo Wörld",default_font);
// String Contains Multibyte characters. Won't work ...

// do it ike this:
write(["H","ä","l","l","o"," ","W","ö","r","l","d"],default_font);

```
![](examples/hello-world.png)

###Converting fonts###

The converter script is located in `converter/ttf2scad.py`

TTX/FontTools python module is required. Grab it from 
[sourceforge](http://sourceforge.net/projects/fonttools/files/2.3/), and make sure to 
install version 2.3, as v2.4 contains a nasty bug.

Usage: `./ttf2scad.py -o /save-to-directory input-font-1.ttf [ input-font-2.ttf ... ]`

