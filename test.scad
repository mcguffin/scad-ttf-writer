use <ttf-writer.scad>;
include <fonts/cuprum-bold.scad>;
 
// simple ascii
text1 = ["T","a","g","o","r","g"];
font1 = cuprum_bold;

 
//scale([0.01,0.01,0.01])
fontsize(72)
	linear_extrude(height=3)
		write(text1,font1,spacing=-100);
/*
//*/ 
