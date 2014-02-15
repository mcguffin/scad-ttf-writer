from fontTools.pens.basePen import BasePen
from bezier.geometry import CubicBezier

class SCADPen(BasePen):
	"""Test class that prints PostScript to stdout."""
	
	points = []
	paths = []
	
	def __init__(self, glyphSet , segment_length = 10 , scale = 1 ):
		BasePen.__init__(self, glyphSet)
		self.segment_length = segment_length
		self.scale = scale
		self.clear();
		
	def clear(self):
		self.points = []
		self.paths = []
	
	def _moveTo(self, pt):
		self.points.append([pt[0]*self.scale,pt[1]*self.scale])
		self.paths.append([])
		self.paths[len(self.paths)-1].append( len(self.points)-1 )
		
	def _lineTo(self, pt):
		self.points.append([pt[0]*self.scale,pt[1]*self.scale])
		self.paths[len(self.paths)-1].append(len(self.points)-1)
		
	def _curveToOne(self, bcp1, bcp2, pt):
		# split curve into n segments ... 
		last = self.points[-1]
		curve = CubicBezier.fromCoords( last[0] , last[1] , bcp1[0]*self.scale,bcp1[1]*self.scale , bcp2[0]*self.scale,bcp2[1]*self.scale , pt[0]*self.scale,pt[1]*self.scale)
		for line in curve.tolines(self.segment_length):
			self.points.append([line.pn.x,line.pn.y])
			self.paths[len(self.paths)-1].append(len(self.points)-1)
		

	def _closePath(self):
		pass
	
	def get_scad_polygon(self):
		if len(self.paths) > 1:
			return 'polygon( points=' + repr(self.points) + ', paths=' + repr(self.paths) + ', convexity=' + str(len(self.paths)*2) + ');'
		return 'polygon( points=' + repr(self.points) + ', convexity=4);'
