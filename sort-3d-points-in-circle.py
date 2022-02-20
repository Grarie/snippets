
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(19680801)

def normalized(a, axis=-1, order=2):
	# https://stackoverflow.com/questions/21030391/how-to-normalize-a-numpy-array-to-a-unit-vector
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)


def vectors_sine_sign(a, B, c, n):
	# returns sine of the angle between the 3D vectors CA and CB with
	# n beeing the normal pointing "up"
	# there is no check, that the points are coplanar and that
	# n is indeed the normal to the spanned plane
	# We don't normalize the vectors, as the *actual* sine is not needed, just the sign
    return np.dot(np.cross(a - c, B - c), n)

def cosine_with(A,b):
	return np.dot( normalized(A), normalized(b)[0] )

def angular_pnt_sort(points, axis=np.array([0,0,0]), normal=np.array([0, 0, 1]), pivot=0):
	# sorts the given coplanar points in a circle
	# axis is the center around which to sort, pivot is a reference vector, normal is the normal to the plane spanned by the points
	# use sine to divide the points in 180° before and after
	angls = vectors_sine_sign(points[pivot], points, axis, normal)
	before = points[ 0>angls ]
	after = points[ 0<=angls ]
	# now we can use the cosinus-values to sort 
	cosins_before = cosine_with(before-axis, points[pivot]-axis)
	cosins_after = cosine_with(after-axis, points[pivot]-axis)
	before = before[np.argsort(cosins_before)]
	after = after[np.argsort(-cosins_after)]
	return np.concatenate( (before,	after) )


# slow resursive method with too much "array creation"
# first try as a proof of concept
def sorted(points, axis=np.array([0,0,0]), normal=np.array([0, 0, 1]), pivot=0):
	if len(points)>1:
		angls = np.array([angl(points[pivot], pnt, axis, normal) for pnt in points])
		if (0>angls).any():
			minpos = np.argmin(angls[0>angls])
		else:
			minpos = None
		if (0<angls).any():
			maxpos = np.argmax(angls[0<angls])
		else:
			maxpos=None
		before = points[ 0>angls ]
		after = points[ 0<angls ]
		return np.concatenate( (
			sorted(before, pivot=minpos)
			,
			[points[pivot] ],	
			sorted(after, pivot=maxpos)
			))
	else:
		return points


def normalize(pnt):
	norm = np.sqrt((pnt**2).sum())
	if norm == 0: 
    	return pnt
    else:
    	return pnt/norm
	

def randrange(n, vmin, vmax):
    """
    Helper function to make an array of random numbers having shape (n, )
    with each number distributed Uniform(vmin, vmax).
    """
    return (vmax - vmin)*np.random.rand(n) + vmin


def scatter(axis, points):
	axis.scatter(points[:,0],points[:,1],points[:,2])


# try it out

n = 10
#points = np.array([randrange(n, 0, 1) for _ in range(3)])
points = np.array([randrange(n, -10, 10), randrange(n, -10, 10), [0 for _ in range(n) ]]).T
points = np.insert(points, 0, -points[0], axis=0)
points = angular_pnt_sort(points)


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

scatter(ax, points)


for i, (x,y,z) in enumerate(points):
    label = i
    ax.text(x, y, z, label)

ax.scatter(0,0,0)
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(-10, 10)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()

