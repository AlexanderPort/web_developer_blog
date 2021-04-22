vec1=[3,6,5,16,45,2,4]
vec2=[2,3]
print([[x**y] for x in vec1 if x < 6 for y in vec2])