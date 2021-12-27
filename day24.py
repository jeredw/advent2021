A=[12,11,12,-3,10,-9,10,-7,-11,-4,14,11,-8,-10]
B=[1,1,1,26,1,26,1,26,26,26,1,1,26,26]
C=[7,15,2,15,14,2,15,1,15,15,12,2,13,13]

def f(s):
  x = z = 0
  for i in range(len(s)):
    x = (z % 26) + A[i]
    z //= B[i]
    if x != s[i]:
      z = z*26 + (s[i] + C[i])
  return z

#print(f([9,9,9,9,9,9,1,1,1,1,1,1]))