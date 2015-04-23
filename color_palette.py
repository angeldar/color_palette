from PIL import Image, ImageDraw, ImageColor
from math import sqrt
from random import randint

THUMBNAIL_SIZE = 200

def get_pixel_color(rgb_img, i, j):
	colors = rgb_img.getpixel((i, j))
	return colors

def draw_sample(top_colors, k):
	im = Image.new('RGB', (200, k * 100), (255, 255, 255))
	dr = ImageDraw.Draw(im)
	for i in range(0, k):
		dr.rectangle(((0, i * 100),(200, 100 + i * 100)), fill = top_colors[i])
	im.save("palette.png")

def get_pixels(img):
	rgb_im = img
	width, height = rgb_im.size
	pixels = []
	for i in xrange(0, width):
		for j in xrange(0, height):
			pixels.append(get_pixel_color(rgb_im, i, j))
	return pixels

def get_random_point(from_val = 0, to_val = 255):
	return (randint(from_val, to_val),
		randint(from_val, to_val), randint(from_val, to_val))

def dist(p1, p2):
	return sqrt(sum([(p1[i] - p2[i])**2 for i in xrange(len(p1))]))

def resize(img, size = 200):
	img.thumbnail((200, 200))
	return img

def find_closest(point, points_arr):
	idx = 0
	min_dist = dist(point, points_arr[0])
	for i in range(1, len(points_arr)):
		curr_dist = dist(point, points_arr[i])
		if curr_dist < min_dist:
			min_dist = curr_dist
			idx = i
	return idx, points_arr[idx]

def find_closest_point(point, points_arr):
	idx, closest_point = find_closest(point, points_arr)
	return closest_point

def find_closest_point_idx(point, points_arr):
	idx, closest_point = find_closest(point, points_arr)
	return idx

def center_cluster(old_cluster, points):
	new_cluster = [0, 0, 0]
	for point in points:
		for coord in range(len(point)):
			new_cluster[coord] += point[coord]
	new_cluster = map(lambda x: x / (len(points) + 1.0), new_cluster)
	return new_cluster

def dist_btw_clusters(clustA, clustB):
	return sum([dist(clustA[i], clustB[i]) for i in
		range(len(clustA))]) / len(clustA)

def to_int(val):
	return int(round(val))

def kmeans(points, k = 6):
	clusters = [get_random_point() for i in range(k)]
	iter = 0
	max_iter = 10
	diff = 3

	while True:
		closest = [[] for i in xrange(k)]
		for point in points:
			closest_idx = find_closest_point_idx(point, clusters)
			closest[closest_idx].append(point)
		old_clusters = clusters[:]
		for i in range(k):
			clusters[i] = center_cluster(clusters[i], closest[i])
		iter += 1
		if dist_btw_clusters(old_clusters, clusters) < diff or iter > max_iter:
			break

	return map(lambda p: (to_int(p[0]), to_int(p[1]), to_int(p[2])), clusters)

def get_palette_from_img(img, k):
	img = resize(img, THUMBNAIL_SIZE)
	points = get_pixels(img)
	clusters = kmeans(points, k)
	clusters = map(lambda p: find_closest_point(p, points), clusters)
	return clusters
	
def get_palette_from_path(path, k):
	img = Image.open(path)
	return get_palette_from_img(img, k)

if __name__ == '__main__':
	k = 6
	im =Image.open("woman1.jpg")
	palette = get_palette_from_img(im, k)
	draw_sample(sorted(palette), k)