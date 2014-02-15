#!/usr/local/bin/python

import sys,os,getopt,re
from fontTools import ttLib,version
from scadwriter.scadpen import SCADPen



#font = ttLib.TTFont('../ttf/VT323-Regular.ttf')
#font = ttLib.TTFont('../ttf/Ubuntu-Regulars.ttf')

class font_processor:
	def __init__( self , font_file):
		try:
			self.font = font = ttLib.TTFont( font_file )
		except IOError as e:
			print 'no such file'
			return
		try:
			self.name = self.font['name'].getName(1, 1, 0).string
		except AttributeError:
			self.name = font_file.match('/([a-z0-9-_]+)\.(t|otf)$/')[1]
		try:
			self.family_name = self.font['name'].getName(2, 1, 0).string
		except AttributeError:
			self.family_name = ''
		self.upm = font['head'].unitsPerEm
		self.build_umap()
		self.build_kerning()
	
	def build_kerning( self ):
		self.kerning = kerning = {}
		try:
			self.font['kern']
		except:
			return # no kearning no cry
		for kernTable in self.font['kern'].kernTables:
			for pair in kernTable.kernTable:
				left,right = pair
				value = kernTable.kernTable[pair]
				try:
					uleft = self.umap[left]
					uright = self.umap[right]
				except KeyError:
					continue
				
				try:
					kerning[uright]
				except KeyError:
					kerning[uright] = []
					
				kerning[uright].append((uleft,value))
			break
	
	def build_umap( self ):
		self.cmap = {}
		for table in self.font['cmap'].tables:
			# prefer type 6!
			if len(table.cmap) > len(self.cmap) :
				print table
				self.cmap = table.cmap
		sys.exit(1)

		self.umap = {v:k for k, v in self.cmap.items()}
	
	def _getunichar(self,uni):
		char = unichr(uni)
		if char in ['"','\\']:
			char = '\\'+char
		return char
	
	def process(self , outdir = None , min_segment_length = 10 ):
		print 'Processing', self.name, self.family_name
		try:
			self.umap
		except AttributeError:
			self.build_umap()
		
		basename = re.sub('[^a-z0-9_]','','_'.join([self.name,self.family_name]).strip('_').lower())
		
		outfile = os.path.realpath(outdir + '/' + basename.replace('_','-') + '.scad')
		
		# determine good output folder
		
		scad_varname = basename
		handle = open(outfile,'wb')
		
		# start font definition
		scad = u"""
/*
 * use it like this:
 * <code>
 * include <%s>;
 * write("Hello World",$%s);
 * </code>
 */
%s = [
""" % (outfile,scad_varname,scad_varname)
		scale = 1000.0/self.upm
		glyphs = self.font.getGlyphSet()
		pen = SCADPen(glyphs , min_segment_length , scale )
		handle.write( scad.encode('utf8') )
		
		for key in self.umap:
			char = self._getunichar(self.umap[key])
			
			try:
				kern = self.kerning[self.umap[key]]
			except KeyError:
				kern = []
			
			glyphs[key].draw( pen )
			
			# start character definition
			scad = u"""	
		[
		"%s", // %s
		%d,
		%s, // points
		%s, // polygons
		[""" % ( char , hex(self.umap[key]) , glyphs[key].width*scale , repr(pen.points) , repr(pen.paths)  )
			
			
			# append kerning here
			for unikern,kernvalue in kern:
				scad = scad + u'["%s",%d]' % (self._getunichar(unikern),kernvalue*scale)
				if (unikern,kernvalue) != kern[-1]:
					scad = scad + u", "
			scad = scad + """] // kerning
	]""" 
			handle.write( scad.encode('utf8') )
			if key != self.umap.keys()[-1]:
				handle.write( ',' )
			pen.clear()
		
		
		handle.write( '''
];''' )
		handle.close()

# proc = font_processor( '../ttf/VT323-Regular.ttf' )

opts,args = getopt.getopt(sys.argv[1:],'o:')

outpath = os.path.expanduser('~');
seglength = 10

for opt,arg in opts:
	if opt == '-o':
		outpath = arg
		if not os.path.exists(outpath):
			print "can't use '%s' as output directory" % arg
			sys.exit(2)
	if opt == '-a':
		seglength = arg

for file in args:
	if os.path.isfile(file):
		proc = font_processor( file )
		proc.process( outpath , seglength )
	else:
		print "Not a file: %s" % file


